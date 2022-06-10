from db.crud import post_movies_of_categories_x
from db.schema import MovieCategories
from routers._base import router
import endpoint_paths


@router.post(path=endpoint_paths.MOVIES_BY_CAT.relative)
async def movies_of_categories_x(categories: MovieCategories):
    return post_movies_of_categories_x(categories)
