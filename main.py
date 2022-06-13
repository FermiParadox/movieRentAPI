from fastapi import FastAPI

from data.database import connect_to_production_db
from routers import get_all_movies, post_movie_by_id, post_movies_cat_x, post_rent_movie

connect_to_production_db()

app = FastAPI()
app.include_router(get_all_movies.router)
app.include_router(post_movies_cat_x.router)
app.include_router(post_movie_by_id.router)
app.include_router(post_rent_movie.router)

# Visit http://127.0.0.1:8000/docs# to test the endpoints.
