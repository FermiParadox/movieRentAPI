from datetime import datetime
from enum import Enum


class Category(str, Enum):
    comedy = 'comedy'
    romance = 'romance'
    documentary = 'documentary'
    action = 'action'


MOVIE_CATEGORIES = tuple(i for i in Category.__members__)


def current_date():
    return datetime.today().strftime('%Y-%m-%d')
