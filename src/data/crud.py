from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any, NoReturn, Union, Literal
from fastapi import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.data.models import Movie, User
from src.data.schema import MovieCategories
from src.middleware.jwt_middleware import signed_jwt_token
from src.utils import IntStrType, OptionalRaise


# ----------------------------------------------------------------------------------------
def get_all_movies() -> dict:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    movies = Movie.objects()
    m: Movie
    return {m.id_: m.title for m in movies}


# ----------------------------------------------------------------------------------------
def movies_by_category(categories: MovieCategories) -> dict:
    movies = Movie.objects(categories__in=categories.categories)
    return {m.id_: m.title for m in movies}


# ----------------------------------------------------------------------------------------
def movie_in_db(movie_id: int) -> Movie:
    return Movie.objects(id_=movie_id).first()


def get_movie_or_raise_http(movie_id: int) -> Movie:
    movie = movie_in_db(movie_id)
    raise_http_if_x_doesnt_exist(x=movie, msg=f'Movie ID {movie_id}')
    return movie


# ----------------------------------------------------------------------------------------
def cost_by_rented_id(movie_id: IntStrType, user_id: IntStrType) -> dict:
    cost = RentedMovieCost().cost_of_movie(movie_id=movie_id, user_id=user_id)
    return {'cost_in_cents': cost}


# ----------------------------------------------------------------------------------------
def login(user_id: str, passphrase_hash: str) -> dict:
    raise_if_user_pass_no_match(user_id=user_id, passphrase_hash=passphrase_hash)
    return {"token": signed_jwt_token()}


def raise_if_user_pass_no_match(user_id: str, passphrase_hash: str) -> OptionalRaise:
    user = user_in_db(user_id)
    if not user.passphrase_hash == passphrase_hash:
        raise http_422_no_match_exception(msg='User ID or passphrase_hash are wrong.')


# ========================================================================================
def user_in_db(user_id: IntStrType) -> User:
    return User.objects(id_=user_id).first()


def get_user_or_raise_http(user_id: IntStrType) -> Union[User, NoReturn]:
    user = user_in_db(user_id=user_id)
    raise_http_if_x_doesnt_exist(x=user, msg=f'User ID {user_id}')
    return user


class RentedMovieDBModifier:
    def add_movie(self, user: User, movie_id: IntStrType) -> bool:
        date = RentDaysHandler().current_date_str()
        rented_str = self._rented_movie_str(movie_id=movie_id, date=date)
        return user.update(add_to_set__rented_movies=rented_str)

    def delete_movie(self, user: User, movie_id: IntStrType) -> bool:
        rented_movies = user.rented_movies
        str_to_remove = f'{movie_id}{RentedMovieDecoder.STR_SEPARATOR}'
        new_rented_movies = [i for i in rented_movies if not i.startswith(str_to_remove)]
        return self._replace_movies(user=user, movies=new_rented_movies)

    def _rented_movie_str(self, movie_id: IntStrType, date: str) -> str:
        return f'{movie_id}{RentedMovieDecoder.STR_SEPARATOR}{date}'

    def _replace_movies(self, user: User, movies: list) -> bool:
        return user.update(set__rented_movies=movies)


class RentedMovieHandler:
    def rent_movie(self, movie_id: int, user_id: str) -> Response:
        return self._rent_movie(movie_id=movie_id, user_id=user_id, rented_db_mod=RentedMovieDBModifier())

    def return_movie(self, movie_id: IntStrType, user_id: IntStrType) -> Response:
        return self._return_movie(movie_id=movie_id, user_id=user_id, rented_db_mod=RentedMovieDBModifier())

    def _rent_movie(self, movie_id: int, user_id: str,
                    rented_db_mod: RentedMovieDBModifier) -> Response:

        user = get_user_or_raise_http(user_id=user_id)
        _ = get_movie_or_raise_http(movie_id=movie_id)

        modified = rented_db_mod.add_movie(user=user, movie_id=movie_id)
        return self._rent_response(modified=modified, movie_id=movie_id)

    def _return_movie(self, movie_id: IntStrType, user_id: IntStrType,
                      rented_db_mod: RentedMovieDBModifier) -> Response:

        user = get_user_or_raise_http(user_id=user_id)
        _ = get_movie_or_raise_http(movie_id=movie_id)

        cost = RentedMovieCost().cost_of_movie(movie_id=movie_id, user_id=user_id)
        TransactionHandler().apply_cost(user=user, movie_cost=cost)
        modified = rented_db_mod.delete_movie(user=user, movie_id=movie_id)
        return self._return_response(modified=modified, movie_id=movie_id)

    def _return_or_rent_response(self, modified: bool, movie_id: int,
                                 type_: Literal['rent', 'return']) -> Response:

        success_msg = f"Movie ID {movie_id} {type_}ed."
        failure_msg = f"{type_.capitalize()}ing movie ID {movie_id} failed."
        if modified:
            return Response(status_code=201, content=success_msg)
        else:
            return Response(status_code=400, content=failure_msg)

    def _rent_response(self, modified: bool, movie_id: int) -> Response:
        return self._return_or_rent_response(modified, movie_id, type_='rent')

    def _return_response(self, modified: bool, movie_id: int) -> Response:
        return self._return_or_rent_response(modified, movie_id, type_='return')


class RentedMovieCost:
    # CPU + time for memory tradeoff.
    # Can't tell if worth it unless tested.
    # "[Complex and not obviously needed] premature optimization is the root of all evil"
    @lru_cache
    def cost(self, days_used: int) -> int:
        # TODO refactor magic number 3 + break method
        if days_used <= 3:
            return days_used * CostPerDay.up_to_3days

        cost_3days = 3 * CostPerDay.up_to_3days
        cost_following_days = (days_used - 3) * CostPerDay.above_3days

        return cost_3days + cost_following_days

    def cost_of_movie(self, user_id: int, movie_id: int) -> Union[int, NoReturn]:
        user = user_in_db(user_id=user_id)
        for encoded_str in user.rented_movies:
            movie_id_date_pair = RentedMovieDecoder().decoded_pair(encoded_str)
            m_id = int(movie_id_date_pair.movie_id)
            if m_id == movie_id:
                start_date = movie_id_date_pair.start_date
                days = RentDaysHandler().charged_days(start_day=start_date)
                movie_cost = RentedMovieCost().cost(days_used=days)
                return movie_cost
        raise http_422_no_match_exception(msg=f'Movie ID {movie_id} not found in rented.')


class RentDaysHandler:
    def decoded_rent_date(self, stored_str: str) -> datetime:
        return datetime.strptime(stored_str, '%Y-%m-%d')

    def current_date(self) -> datetime:
        return datetime.today()

    def current_date_str(self) -> str:
        return self.current_date().strftime('%Y-%m-%d')

    def _days(self, start_day: str) -> int:
        start_date = self.decoded_rent_date(stored_str=start_day)
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


class RentedMovieDecoder:
    STR_SEPARATOR = ':'

    def decoded_pair(self, movie_id_date_str: str) -> MovieIDDatePair:
        movie_id, date = movie_id_date_str.split(self.STR_SEPARATOR)
        return MovieIDDatePair(movie_id=movie_id, start_date=date)


class TransactionHandler:
    def apply_cost(self, user: User, movie_cost: int) -> None:
        user.update(__raw__={"$inc": {"balance": -movie_cost}})


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
