from db.crud import get_all_movies
from routers._base import router
import endpoint_paths


@router.get(path=endpoint_paths.ALL_MOVIES.relative)
async def all_movies():
    return get_all_movies()
