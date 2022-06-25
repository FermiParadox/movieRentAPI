from starlette.responses import Response, JSONResponse

from src.data.schema import MovieCategories
from src.routers._base import router
from src.routers import endpoint_paths
import src.data.crud


@router.post(path=endpoint_paths.MOVIES_BY_CAT.fastapi_format)
async def post_movies_by_category(categories: MovieCategories) -> Response:
    return JSONResponse(src.data.crud.movies_by_category(categories))
