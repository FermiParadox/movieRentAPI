from pydantic import BaseModel
from pydantic.schema import List
from pydantic.types import conint

_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)


class Movie(BaseModel):
    id_: ConstrainedIntMongo
    title: str
    categories: List


MovieList = List[Movie]


class MoviesOfCategoriesX(BaseModel):
    categories: MovieList
