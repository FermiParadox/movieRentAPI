from fastapi import FastAPI

from data.database import connect_to_production_db
from routers import GET_all_movies, GET_movie_by_id, POST_movies_by_cat, PUT_rent_movie

connect_to_production_db()

app = FastAPI()
app.include_router(GET_all_movies.router)
app.include_router(GET_movie_by_id.router)
app.include_router(POST_movies_by_cat.router)
app.include_router(PUT_rent_movie.router)

# Visit http://127.0.0.1:8000/docs# to test the endpoints.
