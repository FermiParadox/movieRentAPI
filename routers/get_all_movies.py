from fastapi import APIRouter

from db.crud import get_all_movies
from endpoint_paths import ALL_MOVIES

router = APIRouter()


@router.get(path=ALL_MOVIES.relative)
async def all_movies():
    return get_all_movies()
