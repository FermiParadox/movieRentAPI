from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any
from fastapi import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.data.models import Movie, User
from src.data.schema import MovieCategories, MovieIDList


def get_all_movies() -> dict:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    movies = Movie.objects()
    m: Movie
    return {m.id_: m.title for m in movies}


def movies_by_category(categories: MovieCategories) -> MovieIDList:
    movies = Movie.objects(categories__in=categories.categories)
    return [m.title for m in movies]


def movie_db_obj_by_id(movie_id: int) -> Movie:
    return Movie.objects(id_=movie_id).first()


def movie_by_id(movie_id: int) -> dict:
    m = movie_db_obj_by_id(movie_id)
    raise_http_if_id_doesnt_exist(match=m)
    return {'title': m.title, 'id_': m.id_, 'categories': m.categories, 'details': m.details}


def user_by_id(user_id) -> User:
    return User.objects(id_=user_id).first()


class RentedMovieModifier:
    def rent_movie_str(self, movie_id, date: str) -> str:
        return f'{movie_id}{RentedMovieDecoder.STR_SEPARATOR}{date}'

    def add_rented(self, user: User, movie_id) -> bool:
        date = RentDaysHandler().current_date_str()
        s = self.rent_movie_str(movie_id=movie_id, date=date)
        return user.update(add_to_set__rented_movies=s)

    def delete_rented(self, user: User, movie_id) -> bool:
        rented_movies = user.rented_movies
        str_to_remove = f'{movie_id}{RentedMovieDecoder.STR_SEPARATOR}'
        new_rented_movies = [i for i in rented_movies if not i.startswith(str_to_remove)]
        modification = user.update(set__rented_movies=new_rented_movies)
        return modification


class RentedMovieHandler:
    def rent_movie(self, movie_id: int, user_id: str) -> Response:
        return self._rent_movie(movie_id=movie_id, user_id=user_id, modifier=RentedMovieModifier())

    def _rent_movie(self, movie_id: int, user_id: str, modifier: RentedMovieModifier):
        u = user_by_id(user_id=user_id)
        raise_http_if_id_doesnt_exist(match=u)

        m = movie_by_id(movie_id=movie_id)
        raise_http_if_id_doesnt_exist(match=m)

        modified = modifier.add_rented(user=u, movie_id=movie_id)
        return self.rent_response(modified=modified, movie_id=movie_id)

    def return_movie(self, movie_id, user_id):
        return self._return_movie(movie_id=movie_id, user_id=user_id, modifier=RentedMovieModifier())

    def _return_movie(self, movie_id, user_id, modifier: RentedMovieModifier):
        u = user_by_id(user_id=user_id)
        raise_http_if_id_doesnt_exist(match=u)

        m = movie_db_obj_by_id(movie_id=movie_id)
        raise_http_if_id_doesnt_exist(match=m)

        modified = modifier.delete_rented(user=u, movie_id=movie_id)
        return self.return_response(modified=modified, user_id=user_id, movie_id=movie_id)

    @staticmethod
    def rent_response(modified: bool, movie_id: int) -> Response:
        if modified:
            return Response(status_code=201, content=f'Movie ID {movie_id} rented.')
        else:
            return Response(status_code=400, content=f'Renting movie ID {movie_id} failed.')

    def return_response(self, modified: bool, user_id: int, movie_id: int) -> Response:
        if modified:
            self.pay_cost(user_id=user_id)
            return Response(status_code=201, content=f'Movie ID {movie_id} return.')
        else:
            return Response(status_code=400, content=f'Returning movie ID {movie_id} failed.')

    def pay_cost(self, user_id):
        print('pay_cost not implemented')


def raise_http_if_id_doesnt_exist(match: Any):
    if not match:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"No match found.")


def cost_by_rented_id(movie_id, user_id):
    raise NotImplementedError


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


@dataclass
class MovieIDDatePair:
    movie_id: str
    start_date: str


class RentedMovieDecoder:
    STR_SEPARATOR = ':'

    def decode(self, movie_id_date_str: str):
        movie_id, date = movie_id_date_str.split(self.STR_SEPARATOR)
        return MovieIDDatePair(movie_id=movie_id, start_date=date)


class TransactionHandler:
    def apply_cost(self, user: User, start_day: str) -> None:
        days = RentDaysHandler().charged_days(start_day=start_day)
        movie_cost = RentedMovieCost().cost(days_used=days)
        user.update(dec__balance=movie_cost)
