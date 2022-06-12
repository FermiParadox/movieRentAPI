from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from data.models import Movie
from data.schema import MovieCategories, MovieIDList


def get_all_movies() -> dict:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    m: Movie
    return {m.id_: m.title for m in Movie.objects()}


def post_movies_of_categories_x(categories: MovieCategories) -> MovieIDList:
    return [m.title for m in Movie.objects(categories__in=categories.categories)]


def movie_by_id(movie_id: int):
    movies_list = Movie.objects(id_=movie_id)
    raise_http_if_empty(movies_list=movies_list)
    m: Movie
    m = Movie.objects(id_=movie_id)[0]
    return {'title': m.title, 'id_': m.id_, 'categories': m.categories, 'details': m.details}


def raise_http_if_empty(movies_list: MovieIDList):
    if not movies_list:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"This movie ID doesn't exist.")



async def rent_movie(movie_id: int, user_id: int):
    return
