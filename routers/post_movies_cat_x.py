from db.crud import post_movies_of_categories_x
from db.schema import MoviesOfCategoriesX
from routers._base import router
import endpoint_paths


@router.post(path=endpoint_paths.ALL_MOVIES.relative)
async def movies_of_categories_x(categories: MoviesOfCategoriesX):
    return post_movies_of_categories_x(categories)
