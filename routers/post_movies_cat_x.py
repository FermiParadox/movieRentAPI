from data.crud import post_movies_of_categories_x
from data.schema import MovieCategories
from routers._base import router
from routers import _endpoint_paths


@router.post(path=_endpoint_paths.MOVIES_BY_CAT.relative)
async def movies_of_categories_x(categories: MovieCategories):
    return post_movies_of_categories_x(categories)
