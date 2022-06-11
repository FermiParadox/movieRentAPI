from enum import Enum
from mongoengine import connect
from pymongo.mongo_client import MongoClient

from secret_handler import mongo_db_link


class DBName(str, Enum):
    production = 'movies_renting'
    test = 'test'


def connection(db: DBName) -> MongoClient:
    # https://docs.mongoengine.org/guide/connecting.html#connect-with-keyword-attributes
    return connect(host=mongo_db_link(), db=db)
