from starlette.responses import JSONResponse, Response

from src.routers._base import router
from src.routers import endpoint_paths
from src.data.crud import get_all_movies


@router.get(path=endpoint_paths.ALL_MOVIES.fastapi_format)
async def all_movies() -> Response:
    return JSONResponse(content=get_all_movies())
