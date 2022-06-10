from typing import List
from mongoengine import Document, StringField, IntField, DictField, ListField, ValidationError

from db._base import ALL_CATEGORIES


class User(Document):
    id = IntField(min_value=1, unique=True, required=True)
    name = StringField(max_length=50, required=True)
    # DO NOT store passwords; it's not safe.
    passphrase_hash = StringField(min_length=12, max_length=70)
    balance = IntField(min_value=0, max_value=1000, default=0)
    rented_movies = DictField()


# ---------------------------------------------------------------------------
def validate_movie_categories(categories: List) -> None:
    disallowed_categories = set(categories) - ALL_CATEGORIES
    if disallowed_categories:
        raise ValidationError(f'The following categories are not allowed: {disallowed_categories}')


class Movie(Document):
    id_ = IntField(min_value=1, unique=True, required=True)
    title = StringField(max_length=50, required=True)
    categories = ListField(validation=validate_movie_categories, required=True)


MovieList = List[Movie]
