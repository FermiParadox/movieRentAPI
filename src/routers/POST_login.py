from starlette.responses import JSONResponse, Response

from src.data.schema import Login
from src.routers._base import router
from src.routers import _endpoint_paths
import src.data.crud


@router.post(path=_endpoint_paths.LOGIN.fastapi_format)
async def post_login(login_info: Login) -> Response:
    content = src.data.crud.login(user_id=login_info.user_id, passphrase_hash=login_info.passphrase_hash)
    return JSONResponse(content=content)
