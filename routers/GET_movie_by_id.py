from routers._base import router
from routers import _endpoint_paths
import data.crud


@router.get(path=_endpoint_paths.MOVIE_BY_ID.fastapi_format)
async def movie_by_id(movie_id: int):
    return await data.crud.movie_by_id(movie_id)
