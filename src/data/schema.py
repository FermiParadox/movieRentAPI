from pydantic import BaseModel
from pydantic.schema import List, Literal
from pydantic.types import conint

from src.data._base import MOVIE_CATEGORIES

_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)


# TODO use in crud
class Movie(BaseModel):
    id_: ConstrainedIntMongo
    title: str
    categories: List
    details: str


MovieIDList = List[int]


class MovieCategories(BaseModel):
    categories: List[Literal[MOVIE_CATEGORIES]]


class UserID(BaseModel):
    id_: ConstrainedIntMongo
