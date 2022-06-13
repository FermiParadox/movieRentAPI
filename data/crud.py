from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from data.models import Movie
from data.schema import MovieCategories, MovieIDList


async def get_all_movies() -> dict:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    movies = Movie.objects()
    m: Movie
    return {m.id_: m.title for m in movies}


async def movies_by_category(categories: MovieCategories) -> MovieIDList:
    movies = Movie.objects(categories__in=categories.categories)
    return [m.title for m in movies]


async def movie_by_id(movie_id: int):
    movies_list = Movie.objects(id_=movie_id)
    raise_http_if_id_doesnt_exist(matches=movies_list)
    m: Movie
    m = movies_list[0]
    return {'title': m.title, 'id_': m.id_, 'categories': m.categories, 'details': m.details}


def raise_http_if_id_doesnt_exist(matches: list):
    if not matches:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"This ID doesn't exist.")


async def rent_movie(movie_id: int, user_id: str):
    return
