from pydantic import BaseModel
from pydantic.schema import List, Literal, Tuple
from pydantic.types import conint

from db._base import MOVIE_CATEGORIES

_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)


class Movie(BaseModel):
    id_: ConstrainedIntMongo
    title: str
    categories: List


MovieIDList = List[int]


class MovieCategories(BaseModel):
    categories: List[Literal[MOVIE_CATEGORIES]]
