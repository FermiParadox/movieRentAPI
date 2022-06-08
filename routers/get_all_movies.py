from typing import List
from fastapi import APIRouter

from endpoint_paths import ALL_MOVIES

router = APIRouter()


@router.get(path=ALL_MOVIES.relative, response_model=List[str])
async def all_movies() -> List[str]:
    return ['movie1', 'movie2', 'movie3', 'movie4']
