from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from src.data.database import connect_to_production_db
from src.middleware.jwt_middleware import middleware_jwt
from src.routers import GET_all_movies, PUT_charge, GET_movie_by_id, POST_movies_by_cat, PUT_rent_movie, \
    PUT_return_movie, POST_login

connect_to_production_db()

app = FastAPI()

app.include_router(GET_all_movies.router)
app.include_router(GET_movie_by_id.router)
app.include_router(POST_movies_by_cat.router)
app.include_router(PUT_rent_movie.router)
app.include_router(PUT_return_movie.router)
app.include_router(PUT_charge.router)
app.include_router(POST_login.router)


@app.middleware("http")
async def middleware_jwt_(req: Request, call_next) -> Response:
    return await middleware_jwt(req, call_next)


# Run the server and visit http://127.0.0.1:8000/docs# to test the endpoints.
