from enum import Enum


class Category(str, Enum):
    comedy = 'comedy'
    romance = 'romance'
    documentary = 'documentary'
    action = 'action'


MOVIE_CATEGORIES = tuple(i for i in Category.__members__)
