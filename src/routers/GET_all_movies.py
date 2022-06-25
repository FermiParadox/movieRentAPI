from starlette.responses import JSONResponse, Response

from src.routers._base import router
from src.routers import endpoint_paths
import src.data.crud


@router.get(path=_endpoint_paths.ALL_MOVIES.fastapi_format)
async def all_movies() -> Response:
    return JSONResponse(content=src.data.crud.get_all_movies())
