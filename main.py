from fastapi import FastAPI

from routers import get_all_movies


app = FastAPI()

app.include_router(get_all_movies.router)
