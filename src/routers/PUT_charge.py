from starlette.responses import Response, JSONResponse

from src.data.schema import UserID
from src.routers._base import router
from src.routers import endpoint_paths
from src.data.crud import cost_by_rented_id


@router.put(path=endpoint_paths.RENT_COST_BY_MOVIE_ID.fastapi_format)
async def put_cost_by_rented_id(movie_id: int, user_id: UserID) -> Response:
    content = await cost_by_rented_id(movie_id=movie_id, user_id=user_id.id_)
    return JSONResponse(content=content)
