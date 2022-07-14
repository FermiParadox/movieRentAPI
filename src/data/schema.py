from pydantic import BaseModel, Field
from pydantic.schema import Literal
from pydantic.types import conint, constr, conlist
from typing import List

from src.data._base import MOVIE_CATEGORIES, Category

_MONGODB_INT_UPPER_LIM = 2 ** 31
ConstrainedIntMongo = conint(gt=0, lt=_MONGODB_INT_UPPER_LIM)

MovieCategoryType = List[Literal[MOVIE_CATEGORIES]]


class Movie(BaseModel):
    id_: ConstrainedIntMongo
    title: str
    categories: MovieCategoryType
    details: str


class User(BaseModel):
    id_: ConstrainedIntMongo = Field()
    name: str
    # DO NOT use this in production. Follow best practises when handling passwords.
    passphrase_hash: constr(max_length=50)
    balance: conint(gt=0, le=100000)
    rented_movies: conlist(Category, unique_items=True)  # ['<movie_id>:<date>', ]


class MovieCategories(BaseModel):
    categories: MovieCategoryType


class UserID(BaseModel):
    id_: ConstrainedIntMongo


class Login(BaseModel):
    user_id: str
    passphrase_hash: str
