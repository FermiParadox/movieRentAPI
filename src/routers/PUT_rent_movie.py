from starlette.responses import Response

from src.data.schema import UserID
from src.routers import endpoint_paths
from src.routers._base import router
from src.data.crud import RentingHandler


@router.put(path=endpoint_paths.RENT.fastapi_format)
async def put_rent_movie(movie_id: int, user_id: UserID) -> Response:
    return await RentingHandler().rent_movie(movie_id=movie_id, user_id=user_id.id_)
