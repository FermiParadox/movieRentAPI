from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any, NoReturn, Union, Literal, Dict
from fastapi import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.data.models import Movie, User
from src.data.schema import MovieCategories
from src.middleware.jwt_middleware import signed_jwt_token
from src.utils import IntStr, OptionalRaise


# ----------------------------------------------------------------------------------------
def get_all_movies() -> Dict[int, str]:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    movies = Movie.objects()
    m: Movie
    return {m.id_: m.title for m in movies}


# ----------------------------------------------------------------------------------------
def movies_by_category(categories: MovieCategories) -> Dict[int, str]:
    movies = Movie.objects(categories__in=categories.categories)
    return {m.id_: m.title for m in movies}


# ----------------------------------------------------------------------------------------
@dataclass
class MovieInDB:
    movie_id: IntStr

    def get(self) -> Movie:
        return Movie.objects(id_=self.movie_id).first()

    def check_exists_and_get(self) -> OptionalRaise:
        movie = self.get()
        raise_http_if_x_doesnt_exist(x=movie, msg=f'Movie ID {self.movie_id}')
        return movie


# ----------------------------------------------------------------------------------------
def cost_by_rented_id(movie_id: IntStr, user_id: IntStr) -> Dict[str, int]:
    user = UserInDB(user_id=user_id).check_exists_and_get()
    cost = RentedMovieCost().cost_of_movie(movie_id=movie_id, user=user)
    return {'cost_in_cents': cost}


# ----------------------------------------------------------------------------------------
class Authenticator:
    def login(self, user_id: str, passphrase_hash: str) -> Dict[str, str]:
        self.raise_if_user_pass_no_match(user_id=user_id, passphrase_hash=passphrase_hash)
        return {"token": signed_jwt_token()}

    def raise_if_user_pass_no_match(self, user_id: str, passphrase_hash: str) -> OptionalRaise:
        user = UserInDB(user_id=user_id).check_exists_and_get()
        if not user.passphrase_hash == passphrase_hash:
            raise http_422_no_match_exception(msg='User ID or passphrase_hash are wrong.')


# ========================================================================================
@dataclass
class UserInDB:
    user_id: IntStr

    def user(self) -> User:
        return User.objects(id_=self.user_id).first()

    def check_exists_and_get(self) -> Union[User, NoReturn]:
        user = self.user()
        raise_http_if_x_doesnt_exist(x=user, msg=f'User ID {self.user_id}')
        return user


class ITransactionHandler(ABC):
    @abstractmethod
    def apply_cost(self, user: User, cost: int) -> None:
        pass


class TransactionHandler(ITransactionHandler):
    def apply_cost(self, user: User, cost: int) -> None:
        user.update(__raw__={"$inc": {"balance": -cost}})


class IRentedMovieDBModifier(ABC):
    @abstractmethod
    def add(self, user: User, movie_id: IntStr) -> bool:
        """Add a rented movie to the DB"""

    @abstractmethod
    def delete(self, user: User, movie_id: IntStr) -> bool:
        """Remove a rented movie from the DB"""


class RentedMovieDBModifier(IRentedMovieDBModifier):
    def add(self, user: User, movie_id: IntStr) -> bool:
        date = RentDays().current_date_str()
        rented_str = RentedMovieDateEncoder().encoded_pair(movie_id=movie_id, date=date)
        return self._add_one(user=user, rented_str=rented_str)

    def delete(self, user: User, movie_id: IntStr) -> bool:
        rented_movies = user.rented_movies
        str_to_remove = f'{movie_id}{RentedMovieDateEncoder.STR_SEPARATOR}'
        new_list = [i for i in rented_movies if not i.startswith(str_to_remove)]
        return self._update_rented(user=user, movies=new_list)

    def _add_one(self, user: User, rented_str: str) -> bool:
        return user.update(add_to_set__rented_movies=rented_str)

    def _update_rented(self, user: User, movies: list) -> bool:
        return user.update(set__rented_movies=movies)


class MovieHandlingResponse:
    def rent(self, modified: bool, movie_id: int) -> Response:
        return self._return_or_rent(modified, movie_id, type_='rent')

    def return_(self, modified: bool, movie_id: int) -> Response:
        return self._return_or_rent(modified, movie_id, type_='return')

    def _return_or_rent(self, modified: bool, movie_id: int,
                        type_: Literal['rent', 'return']) -> Response:

        success_msg = f"Movie ID {movie_id} {type_}ed."
        failure_msg = f"{type_.capitalize()}ing movie ID {movie_id} failed."
        if modified:
            return Response(status_code=201, content=success_msg)
        else:
            return Response(status_code=400, content=failure_msg)


class RentingHandler:
    def _modify_db_and_respond(self, movie_id: int, user: User,
                               db_modifier: IRentedMovieDBModifier) -> Response:
        modified = db_modifier.add(user=user, movie_id=movie_id)
        return MovieHandlingResponse().rent(modified=modified, movie_id=movie_id)

    def _check_movie_exists(self, movie_id: int):
        return MovieInDB(movie_id).check_exists_and_get()

    def rent_movie(self, movie_id: int, user_id: str) -> Response:
        user = UserInDB(user_id).check_exists_and_get()
        self._check_movie_exists(movie_id)
        return self._modify_db_and_respond(movie_id=movie_id, user=user,
                                           db_modifier=RentedMovieDBModifier())


class ReturningHandler:
    def _pay_movie(self, movie_id: IntStr, user: User, transaction_handler: ITransactionHandler):
        cost = RentedMovieCost().cost_of_movie(movie_id=movie_id, user=user)
        transaction_handler.apply_cost(user=user, cost=cost)

    def _modify_db_and_respond(self, movie_id: IntStr, user: User,
                               db_modifier: IRentedMovieDBModifier) -> Response:

        modified = db_modifier.delete(user=user, movie_id=movie_id)
        return MovieHandlingResponse().return_(modified=modified, movie_id=movie_id)

    def return_movie(self, movie_id: IntStr, user_id: IntStr) -> Response:
        user = UserInDB(user_id).check_exists_and_get()
        MovieInDB(movie_id).check_exists_and_get()

        self._pay_movie(movie_id=movie_id, user=user, transaction_handler=TransactionHandler())

        return self._modify_db_and_respond(movie_id=movie_id, user=user,
                                           db_modifier=RentedMovieDBModifier())


class RentedMovieCost:
    def _cost_up_to_3(self, days_used: Literal[1, 2, 3]) -> int:
        return days_used * CostPerDay.up_to_3days

    def _cost_3days_or_more(self, days_used: int) -> int:
        cost_3days = 3 * CostPerDay.up_to_3days
        cost_following_days = (days_used - 3) * CostPerDay.above_3days
        return cost_3days + cost_following_days

    # CPU + time for memory tradeoff.
    # Can't tell if worth it unless tested.
    # "[Complex and not obviously needed] premature optimization is the root of all evil"
    @lru_cache
    def cost(self, days_used: int) -> int:
        # TODO refactor magic number 3
        if days_used <= 3:
            return self._cost_up_to_3(days_used)
        return self._cost_3days_or_more(days_used)

    def cost_of_movie(self, user: User, movie_id: int) -> Union[int, NoReturn]:
        for encoded_str in user.rented_movies:
            movie_id_date_pair = RentedMovieDateEncoder().decoded_pair(encoded_str)
            m_id = int(movie_id_date_pair.movie_id)
            if m_id == movie_id:
                start_date_str = movie_id_date_pair.start_date
                days_used = RentDays().charged_days(start_day=start_date_str)
                movie_cost = RentedMovieCost().cost(days_used=days_used)
                return movie_cost
        raise http_422_no_match_exception(msg=f'Movie ID {movie_id} not found in rented.')


class RentDays:
    def current_date(self) -> datetime:
        return datetime.today()

    def current_date_str(self) -> str:
        return self.current_date().strftime('%Y-%m-%d')

    def _days(self, start_day: str) -> int:
        start_date = RentedMovieDateEncoder().date(date_str=start_day)
        end_date = self.current_date()
        date_diff = end_date - start_date
        return date_diff.days

    def charged_days(self, start_day: str) -> int:
        """If they watch a movie and return it within a few hours
        they should still be charged."""
        return self._days(start_day) + 1


@dataclass(frozen=True)
class MovieIDDatePair:
    movie_id: str
    start_date: str


class RentedMovieDateEncoder:
    STR_SEPARATOR = ':'

    def decoded_pair(self, movie_id_date_str: str) -> MovieIDDatePair:
        movie_id, date = movie_id_date_str.split(self.STR_SEPARATOR)
        return MovieIDDatePair(movie_id=movie_id, start_date=date)

    def encoded_pair(self, movie_id: IntStr, date: str) -> str:
        return f'{movie_id}{RentedMovieDateEncoder.STR_SEPARATOR}{date}'

    def date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, '%Y-%m-%d')


class CostPerDay(int, Enum):
    """Cost in cents.
    """
    up_to_3days = 1_00
    above_3days = 50


# ----------------------------------------------------------------------------------------
def http_422_no_match_exception(msg="No match found.") -> NoReturn:
    return HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                         detail=msg)


def raise_http_if_x_doesnt_exist(x: Any, msg: str) -> OptionalRaise:
    if not x:
        raise http_422_no_match_exception(msg=f'"{msg} match not found."')
