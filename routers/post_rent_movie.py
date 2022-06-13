from starlette.requests import Request

from routers import _endpoint_paths
from routers._base import router
from data.crud import rent_movie


@router.post(path=_endpoint_paths.RENT.fastapi_format)
async def post_rent_movie(movie_id: int, req: Request):
    params = req.query_params
    return await rent_movie(movie_id=movie_id, user_id=params['user_id'])
