from data.database import connect_to_production_db
from data.models import Movie
from data.schema import MovieCategories, MovieIDList

connect_to_production_db()


def get_all_movies() -> MovieIDList:
    return [t.title for t in Movie.objects()]


def post_movies_of_categories_x(categories: MovieCategories) -> MovieIDList:
    return []
