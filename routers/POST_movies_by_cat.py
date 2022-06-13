from data.schema import MovieCategories
from routers._base import router
from routers import _endpoint_paths
import data.crud


@router.post(path=_endpoint_paths.MOVIES_BY_CAT.fastapi_format)
async def post_movies_by_category(categories: MovieCategories):
    return data.crud.movies_by_category(categories)
