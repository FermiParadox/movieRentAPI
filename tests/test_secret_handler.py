from unittest import TestCase

from secret_handler import _create_mongodb_link


# NOTE: testing _password creation fails due to None value from here.
#   Will implement later.

class Test(TestCase):
    def test_mongodb_link_contains_password(self):
        password = '12atu4Wr'
        link = _create_mongodb_link(password=password)
        self.assertIn(password, link)
