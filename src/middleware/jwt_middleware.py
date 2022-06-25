from datetime import datetime, timedelta
from typing import Iterable, Dict

from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.responses import Response
import jwt  # requires PyJWT, despite not mentioning it

from config import JWT_MIDDLEWARE_ACTIVE, JWT_ALGORITHM, JWT_PRIVATE_KEY, JWT_DURATION_HOURS, JWT_SECRET_MESSAGE
from src.routers.endpoint_paths import EndpointPath, ALL_MOVIES, \
    MOVIES_BY_CAT, MOVIE_BY_ID, LOGIN, ALL_ENDPOINTS
from src.middleware._base import ProtectedPaths

HEADER_NAME_OF_TOKEN = "token"


async def middleware_jwt(req: Request, call_next) -> Response:
    if not JWT_MIDDLEWARE_ACTIVE:
        return await call_next(req)

    if not is_protected_path(req, paths_protected=JWT_PROTECTED_PATHS):
        return await call_next(req)

    headers = req.headers
    if token_header_not_found(headers=headers):
        return Response(status_code=401, content="No 'token' key in headers.")

    token = headers[HEADER_NAME_OF_TOKEN]
    try:
        decoded_token = jwt.decode(token, key=JWT_PRIVATE_KEY, algorithms=JWT_ALGORITHM)
        if token_is_valid(decoded_token=decoded_token):
            return await call_next(req)
    except jwt.PyJWTError:
        pass
    return Response(status_code=401, content='Token failed.')


def token_header_not_found(headers: Headers) -> bool:
    return HEADER_NAME_OF_TOKEN not in headers


def is_protected_path(req: Request, paths_protected: Iterable[EndpointPath]) -> bool:
    for p in paths_protected:
        if endpoint_path_matches(p, req=req):
            return True
    return False


def endpoint_path_matches(path: EndpointPath, req: Request) -> bool:
    """Compare requested path with stored endpoint path.

    If this is matched:
    > http://127.0.0.1:8000/get-senior

    then this is matched as well:
    http://127.0.0.1:8000/get-senior?seniorId=5
    """
    requested_path = str(req.url)
    p = str(req.base_url).rstrip('/') + path.stripped_relative
    return requested_path.startswith(p)


def token_is_valid(decoded_token: Dict) -> bool:
    return decoded_token["user_id"] == JWT_SECRET_MESSAGE


def signed_jwt_token(duration_h: float = JWT_DURATION_HOURS) -> str:
    expiration = datetime.utcnow() + timedelta(hours=duration_h)
    payload = {"user_id": 'some_stored_value_server-side', "exp": expiration}
    # (function output can be tested here: https://jwt.io/ ; displays local time)
    return jwt.encode(payload=payload, key=JWT_PRIVATE_KEY, algorithm=JWT_ALGORITHM)


JWT_IGNORED_PATHS = frozenset({ALL_MOVIES, MOVIES_BY_CAT, MOVIE_BY_ID, LOGIN})
JWT_PROTECTED_PATHS = ProtectedPaths(all_paths=ALL_ENDPOINTS, ignored=JWT_IGNORED_PATHS).protected
