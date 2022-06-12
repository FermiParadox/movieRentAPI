from data.crud import get_all_movies
from routers._base import router
from routers import _endpoint_paths


@router.get(path=_endpoint_paths.ALL_MOVIES.fastapi_format)
async def all_movies():
    return await get_all_movies()
