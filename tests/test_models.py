from unittest import TestCase

from mongoengine import ValidationError

from db.models import Movie, ALL_CATEGORIES

ALL_CATEGORIES_AS_LIST = list(ALL_CATEGORIES)


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
        m = Movie(id_=1, title='Random title', categories=ALL_CATEGORIES_AS_LIST)
        m.validate()
