from fastapi import FastAPI
import uvicorn

from routers import get_all_movies
from routers import post_movies_cat_x

app = FastAPI()
app.include_router(get_all_movies.router)
app.include_router(post_movies_cat_x.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # Visit http://127.0.0.1:8000/docs# to test the endpoints.
