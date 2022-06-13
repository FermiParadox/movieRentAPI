from typing import Any

from fastapi import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from data._base import current_date
from data.models import Movie, User
from data.schema import MovieCategories, MovieIDList


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


def movie_by_id(movie_id: int) -> dict:
    m: Movie
    m = Movie.objects(id_=movie_id).first()
    raise_http_if_id_doesnt_exist(match=m)
    return {'title': m.title, 'id_': m.id_, 'categories': m.categories, 'details': m.details}


def user_by_id(user_id) -> User:
    return User.objects(id_=user_id).first()


class RentedMovieModifier:
    def rent_movie_str(self, movie_id, date: str) -> str:
        return f'{movie_id}:{date}'

    def add_rented(self, user: User, movie_id) -> bool:
        date = current_date()
        s = self.rent_movie_str(movie_id=movie_id, date=date)
        return user.update(add_to_set__rented_movies=s)


class RentedMovieHandler:
    def rent_movie(self, movie_id: int, user_id: str) -> Response:
        return self._rent_movie(movie_id=movie_id, user_id=user_id, modifier=RentedMovieModifier())

    def _rent_movie(self, movie_id: int, user_id: str, modifier: RentedMovieModifier):
        u = user_by_id(user_id=user_id)
        raise_http_if_id_doesnt_exist(match=u)

        m = movie_by_id(movie_id=movie_id)
        raise_http_if_id_doesnt_exist(match=m)

        modified = modifier.add_rented(user=u, movie_id=movie_id)
        self.start_charging(user_id=user_id)
        return self.rent_response(modified=modified, movie_id=movie_id)

    def start_charging(self, user_id):
        print(f'"start_charging" Not implemented ')

    @staticmethod
    def rent_response(modified: bool, movie_id: int) -> Response:
        if modified:
            return Response(status_code=201, content=f'Movie ID {movie_id} rented.')
        else:
            return Response(status_code=400, content=f'Renting movie ID {movie_id} failed.')

    @staticmethod
    def return_response(modified: bool, movie_id: int) -> Response:
        if modified:
            return Response(status_code=201, content=f'Movie ID {movie_id} return.')
        else:
            return Response(status_code=400, content=f'Returning movie ID {movie_id} failed.')


def raise_http_if_id_doesnt_exist(match: Any):
    if not match:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"No match found.")
