from starlette.responses import JSONResponse, Response

from src.routers._base import router
from src.routers import _endpoint_paths
import src.data.crud


@router.get(path=_endpoint_paths.MOVIE_BY_ID.fastapi_format)
async def get_movie_by_id(movie_id: int) -> Response:
    return JSONResponse(content=src.data.crud.movie_by_id(movie_id))
