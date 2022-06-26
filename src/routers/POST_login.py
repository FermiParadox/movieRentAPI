from starlette.responses import JSONResponse, Response

from src.data.schema import Login
from src.routers._base import router
from src.routers import endpoint_paths
from src.data.crud import Authenticator


@router.post(path=endpoint_paths.LOGIN.fastapi_format)
async def post_login(login_info: Login) -> Response:
    user_id = login_info.user_id
    passphrase_hash = login_info.passphrase_hash
    content = Authenticator().login(user_id=user_id, passphrase_hash=passphrase_hash)
    return JSONResponse(content=content)
