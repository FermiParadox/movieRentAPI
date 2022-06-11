from enum import Enum
import mongoengine
from pymongo.mongo_client import MongoClient

from secret_handler import mongo_db_link


class DBName(str, Enum):
    production = 'movies_renting'
    test = 'test'


def connect(db: DBName) -> MongoClient:
    # https://docs.mongoengine.org/guide/connecting.html#connect-with-keyword-attributes
    return mongoengine.connect(host=mongo_db_link(), db=db)
