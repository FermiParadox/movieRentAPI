from mongoengine import connect
from pymongo.mongo_client import MongoClient

from secret_handler import mongo_db_link


def client() -> MongoClient:
    return connect(host=mongo_db_link())
