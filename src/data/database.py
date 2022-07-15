import motor.motor_asyncio

from src.secret_handler import MongoDBLink


def db_connection():
    link = MongoDBLink().link
    client = motor.motor_asyncio.AsyncIOMotorClient(link)
    return client.movies_renting


db = db_connection()
db_movies = db["movie"]
db_users = db["user"]
