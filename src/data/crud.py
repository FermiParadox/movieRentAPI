from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any
from fastapi import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.data.models import Movie, User
from src.data.schema import MovieCategories
from src.middleware.jwt_middleware import signed_jwt_token
from src.utils import IntStrType


def get_all_movies() -> dict:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    movies = Movie.objects()
    m: Movie
    return {m.id_: m.title for m in movies}


def movies_by_category(categories: MovieCategories) -> dict:
    movies = Movie.objects(categories__in=categories.categories)
    return {m.id_: m.title for m in movies}


def movie_db_obj_by_id(movie_id: int) -> Movie:
    return Movie.objects(id_=movie_id).first()


def movie_by_id(movie_id: int) -> dict:
    m = movie_db_obj_by_id(movie_id)
    raise_http_if_x_doesnt_exist(x=m, msg=f'Movie ID {movie_id}')
    return {'title': m.title, 'id_': m.id_, 'categories': m.categories, 'details': m.details}


def user_by_id(user_id: IntStrType) -> User:
    return User.objects(id_=user_id).first()


def cost_by_rented_id(movie_id: IntStrType, user_id: IntStrType) -> dict:
    cost = RentedMovieCost().cost_of_movie(movie_id=movie_id, user_id=user_id)
    return {'cost_in_cents': cost}


def login(user_id: str, passphrase_hash: str):
    raise_if_user_pass_no_match(user_id=user_id, passphrase_hash=passphrase_hash)
    return {"token": signed_jwt_token()}


def raise_if_user_pass_no_match(user_id: str, passphrase_hash: str):
    u = user_by_id(user_id)
    if not u.passphrase_hash == passphrase_hash:
        raise http_422_no_match_exception(msg='User ID or passphrase_hash are wrong.')


class RentedMovieModifier:
    def rented_movie_str(self, movie_id: IntStrType, date: str) -> str:
        return f'{movie_id}{RentedMovieDecoder.STR_SEPARATOR}{date}'

    def add_rented(self, user: User, movie_id: IntStrType) -> bool:
        date = RentDaysHandler().current_date_str()
        s = self.rented_movie_str(movie_id=movie_id, date=date)
        return user.update(add_to_set__rented_movies=s)

    def store_rented_movies(self, user: User, movies: list) -> bool:
        return user.update(set__rented_movies=movies)

    def delete_rented(self, user: User, movie_id: IntStrType) -> bool:
        rented_movies = user.rented_movies
        str_to_remove = f'{movie_id}{RentedMovieDecoder.STR_SEPARATOR}'
        new_rented_movies = [i for i in rented_movies if not i.startswith(str_to_remove)]
        return self.store_rented_movies(user=user, movies=new_rented_movies)


class RentedMovieHandler:
    def rent_movie(self, movie_id: int, user_id: str) -> Response:
        return self._rent_movie(movie_id=movie_id, user_id=user_id, modifier=RentedMovieModifier())

    def _rent_movie(self, movie_id: int, user_id: str, modifier: RentedMovieModifier):
        u = user_by_id(user_id=user_id)
        raise_http_if_x_doesnt_exist(x=u, msg=f'User ID {user_id}')

        m = movie_by_id(movie_id=movie_id)
        raise_http_if_x_doesnt_exist(x=m, msg=f'Movie ID {movie_id}')

        modified = modifier.add_rented(user=u, movie_id=movie_id)
        return self.rent_response(modified=modified, movie_id=movie_id)

    def return_movie(self, movie_id: IntStrType, user_id: IntStrType):
        return self._return_movie(movie_id=movie_id, user_id=user_id, modifier=RentedMovieModifier())

    def _return_movie(self, movie_id: IntStrType, user_id: IntStrType, modifier: RentedMovieModifier):
        u = user_by_id(user_id=user_id)
        raise_http_if_x_doesnt_exist(x=u, msg=f'User ID {user_id}')

        m = movie_db_obj_by_id(movie_id=movie_id)
        raise_http_if_x_doesnt_exist(x=m, msg=f'Movie ID {movie_id}')

        cost = RentedMovieCost().cost_of_movie(movie_id=movie_id, user_id=user_id)
        TransactionHandler().apply_cost(user=u, movie_cost=cost)
        modified = modifier.delete_rented(user=u, movie_id=movie_id)
        return self.return_response(modified=modified, movie_id=movie_id)

    @staticmethod
    def rent_response(modified: bool, movie_id: int) -> Response:
        if modified:
            return Response(status_code=201, content=f'Movie ID {movie_id} rented.')
        else:
            return Response(status_code=400, content=f'Renting movie ID {movie_id} failed.')

    def return_response(self, modified: bool, movie_id: int) -> Response:
        if modified:
            return Response(status_code=201, content=f'Movie ID {movie_id} returned.')
        else:
            return Response(status_code=400, content=f'Returning movie ID {movie_id} failed.')


class CostPerDay(int, Enum):
    """Cost in cents.
    """
    up_to_3days = 1_00
    above_3days = 50


class RentedMovieCost:
    @lru_cache
    def cost(self, days_used: int):
        # TODO refactor magic number 3 + break method
        if days_used <= 3:
            return days_used * CostPerDay.up_to_3days

        cost_3days = 3 * CostPerDay.up_to_3days
        cost_following_days = (days_used - 3) * CostPerDay.above_3days

        return cost_3days + cost_following_days

    def cost_of_movie(self, user_id: int, movie_id: int) -> int:
        u = user_by_id(user_id=user_id)
        for encoded_str in u.rented_movies:
            movie_id_date_pair = RentedMovieDecoder().decoded_pair(encoded_str)
            m_id = int(movie_id_date_pair.movie_id)
            if m_id == movie_id:
                start_date = movie_id_date_pair.start_date
                days = RentDaysHandler().charged_days(start_day=start_date)
                movie_cost = RentedMovieCost().cost(days_used=days)
                return movie_cost
        raise http_422_no_match_exception(msg=f'Movie ID {movie_id} not found in rented.')


class RentDaysHandler:
    def decoded_rent_date(self, stored_str: str):
        return datetime.strptime(stored_str, '%Y-%m-%d')

    def current_date(self):
        return datetime.today()

    def current_date_str(self):
        return self.current_date().strftime('%Y-%m-%d')

    def _days(self, start_day: str):
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

    def decoded_pair(self, movie_id_date_str: str):
        movie_id, date = movie_id_date_str.split(self.STR_SEPARATOR)
        return MovieIDDatePair(movie_id=movie_id, start_date=date)


class TransactionHandler:
    def apply_cost(self, user: User, movie_cost: int) -> None:
        user.update(__raw__={"$inc": {"balance": -movie_cost}})


def http_422_no_match_exception(msg="No match found."):
    return HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                         detail=msg)


def raise_http_if_x_doesnt_exist(x: Any, msg: str):
    if not x:
        raise http_422_no_match_exception(msg=f'"{msg} match not found."')
