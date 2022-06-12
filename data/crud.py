from data.models import Movie
from data.schema import MovieCategories, MovieIDList


def get_all_movies() -> MovieIDList:
    # Looks rather expensive.
    # Perhaps create mongoDB document containing only movie title + ID.
    # Besides, movies will not be updated too often.
    return [m.title for m in Movie.objects()]


def post_movies_of_categories_x(categories: MovieCategories) -> MovieIDList:
    return []
