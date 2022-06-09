from db.crud import get_all_movies
from endpoint_paths import ALL_MOVIES
from routers._base import router


@router.get(path=ALL_MOVIES.relative)
async def all_movies():
    return get_all_movies()
