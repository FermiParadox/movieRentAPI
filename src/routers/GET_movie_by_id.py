from starlette.responses import JSONResponse, Response

from src.routers._base import router
from src.routers import endpoint_paths
import src.data.crud


@router.get(path=endpoint_paths.MOVIE_BY_ID.fastapi_format)
async def get_movie_by_id(movie_id: int) -> Response:
    movie = src.data.crud.get_movie_or_raise_http(movie_id)
    movie_data = {'title': movie.title,
                  'id_': movie.id_,
                  'categories': movie.categories,
                  'details': movie.details}
    return JSONResponse(content=movie_data)
