from fastapi import FastAPI

from endpoint_paths import ALL_MOVIES

app = FastAPI()


@app.get(ALL_MOVIES.relative)
async def all_movies():
    return {"message": "all_movies not implemented"}
