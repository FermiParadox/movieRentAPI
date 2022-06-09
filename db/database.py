import pymongo as pymongo
from pydantic.types import conint

from secret_handler import MONGODB_LINK

client = pymongo.MongoClient(MONGODB_LINK)
db = client.test

_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)
