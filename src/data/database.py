from enum import Enum
import mongoengine
from pymongo.mongo_client import MongoClient

from src.secret_handler import MongoDBLink


class DBName(str, Enum):
    production = 'movies_renting'
    test = 'test'


def connect(db: DBName, link: str) -> MongoClient:
    # https://docs.mongoengine.org/guide/connecting.html#connect-with-keyword-attributes
    return mongoengine.connect(host=link, db=db)


def connect_to_production_db() -> MongoClient:
    return connect(db=DBName.production, link=MongoDBLink().link())
