from fastapi import FastAPI

app = FastAPI()


@app.get("/all_movies")
async def all_movies():
    return {"message": "all_movies not implemented"}
