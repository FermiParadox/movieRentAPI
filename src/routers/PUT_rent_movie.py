from src.data.schema import UserID
from src.routers import _endpoint_paths
from src.routers._base import router
import src.data.crud


@router.put(path=_endpoint_paths.RENT.fastapi_format)
async def put_rent_movie(movie_id: int, user_id: UserID):
    return src.data.crud.RentedMovieHandler().rent_movie(movie_id=movie_id, user_id=user_id.id_)
