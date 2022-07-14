from starlette.responses import JSONResponse, Response

from src.routers._base import router
from src.routers import endpoint_paths
from src.data.crud import MovieInDB


@router.get(path=endpoint_paths.MOVIE_BY_ID.fastapi_format)
async def get_movie_by_id(movie_id: int) -> Response:
    movie = await MovieInDB(movie_id).check_exists_and_get()
    movie_data = {'title': movie['title'],
                  'id_': movie['id_'],
                  'categories': movie['categories'],
                  'details': movie['details']}
    return JSONResponse(content=movie_data)
