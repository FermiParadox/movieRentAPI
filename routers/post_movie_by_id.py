import data.crud
from routers._base import router
from routers import _endpoint_paths


@router.post(path=_endpoint_paths.MOVIE_BY_ID.fastapi_format)
async def movie_by_id(movie_id: int):
    return data.crud.movie_by_id(movie_id)
