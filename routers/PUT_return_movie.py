from data.schema import UserID
from routers import _endpoint_paths
from routers._base import router
import data.crud


@router.put(path=_endpoint_paths.RETURN.fastapi_format)
async def post_return_movie(movie_id: int, user_id: UserID):
    return data.crud.RentedMovieHandler().return_movie(movie_id=movie_id, user_id=user_id.id_)
