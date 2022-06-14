from src.data.schema import UserID
from src.routers._base import router
from src.routers import _endpoint_paths
import src.data.crud


@router.put(path=_endpoint_paths.RENT_COST_BY_MOVIE_ID.fastapi_format)
async def put_cost_by_rented_id(movie_id: int, user_id: UserID):
    return src.data.crud.cost_by_rented_id(movie_id=movie_id, user_id=user_id.id_)
