from src.data.schema import Login
from src.routers._base import router
from src.routers import _endpoint_paths
import src.data.crud


@router.post(path=_endpoint_paths.LOGIN.fastapi_format)
async def post_login(login_info: Login):
    return src.data.crud.login(name=login_info.name,
                               passphrase=login_info.passphrase)
