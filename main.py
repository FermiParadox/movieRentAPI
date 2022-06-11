from fastapi import FastAPI

from data.database import connect_to_production_db
from routers import get_all_movies
from routers import post_movies_cat_x

connect_to_production_db()

app = FastAPI()
app.include_router(get_all_movies.router)
app.include_router(post_movies_cat_x.router)

# Visit http://127.0.0.1:8000/docs# to test the endpoints.
