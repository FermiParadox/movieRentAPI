from src.routers._base import router
from src.routers import _endpoint_paths
import src.data.crud


@router.get(path=_endpoint_paths.MOVIE_BY_ID.fastapi_format)
async def movie_by_id(movie_id: int):
    return src.data.crud.movie_by_id(movie_id)
