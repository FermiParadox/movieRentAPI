import pymongo as pymongo
from pydantic.types import conint

from secret_handler import mongo_db_link


client = pymongo.MongoClient(mongo_db_link())
db = client.test


_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)
