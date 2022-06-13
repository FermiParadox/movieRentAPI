from routers._base import router
from routers import _endpoint_paths
import data.crud


@router.get(path=_endpoint_paths.ALL_MOVIES.fastapi_format)
async def all_movies():
    return await data.crud.get_all_movies()
