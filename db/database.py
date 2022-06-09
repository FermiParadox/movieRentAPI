from pydantic.types import conint
from mongoengine import connect

from secret_handler import mongo_db_link


client = connect(host=mongo_db_link())


_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)
