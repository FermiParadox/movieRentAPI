from unittest import TestCase

from mongoengine import ValidationError

from src.data._base import MOVIE_CATEGORIES
from src.data.models import Movie, User

ALL_CATEGORIES_AS_LIST = list(MOVIE_CATEGORIES)

MOCK_USER = User(id_=69182, name='Random Name', passphrase_hash='asdJUU7JNG2', balance=90000)
MOCK_MOVIE = Movie(id_=1, title='Random title', categories=ALL_CATEGORIES_AS_LIST)


class TestMovie(TestCase):
    def test_1disallowed_category_raises(self):
        with self.assertRaises(ValidationError):
            m = Movie(id_=1, title='Random title', categories=['non existent cat'])
            m.validate()

    def test_allowed_plus_disallowed_category_raises(self):
        with self.assertRaises(ValidationError):
            m = Movie(id_=1, title='Random title', categories=['as224'] + ALL_CATEGORIES_AS_LIST)
            m.validate()

    def test_allowed_categories_dont_raise(self):
        MOCK_MOVIE.validate()


class TestUser(TestCase):
    def test_allowed_params_dont_raise(self):
        MOCK_USER.validate()
