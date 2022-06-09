from unittest import TestCase

from secret_handler import password, _create_mongodb_link


class TestPasswordExtraction(TestCase):
    def test_password_raises_when_empty(self):
        with self.assertRaises(ValueError):
            password(env_var='MONGODB_MOVIES_USER0_PASS')
    # NOTE: testing _password creation fails due to None value when calling from here.
    #   Will implement later.


class TestMongoDBLinkCreation(TestCase):
    def test_mongodb_link_contains_password(self):
        password_ = '12atu4Wr'
        link = _create_mongodb_link(password_=password_)
        self.assertIn(password_, link)
