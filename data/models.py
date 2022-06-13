from typing import List, NoReturn
from mongoengine import Document, StringField, IntField, ListField, ValidationError

from data._base import MOVIE_CATEGORIES


class User(Document):
    id_ = IntField(min_value=1, unique=True, required=True)
    name = StringField(max_length=50, required=True)
    # DO NOT use this in production. Follow best practises when handling passwords.
    passphrase_hash = StringField(min_length=1, max_length=70)
    balance = IntField(min_value=0, max_value=1000, default=0)
    rented_movies = ListField()     # ['<movie_id>:<date>', ]


# ---------------------------------------------------------------------------
def validate_movie_categories(categories: List) -> NoReturn:
    disallowed_categories = set(categories) - set(MOVIE_CATEGORIES)
    if disallowed_categories:
        raise ValidationError(f'The following categories are not allowed: {disallowed_categories}')


class Movie(Document):
    id_ = IntField(min_value=1, unique=True, required=True)
    title = StringField(max_length=50, required=True)
    categories = ListField(validation=validate_movie_categories, required=True)
    details = StringField(max_length=500)
