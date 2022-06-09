from unittest import TestCase

from secret_handler import PASS_ENV_VAR, password, _create_mongodb_link, mongo_db_link

"""To ensure those tests run normally, set the environment var for this file as well.
See https://stackoverflow.com/a/42708480.
"""


class TestPasswordExtraction(TestCase):
    def test_password_non_empty(self):
        print('Ignore this warning:')
        p = password(env_var='non_existent_key_40896903')
        self.assertTrue(p)

    def test_password_doesnt_raise(self):
        p = password(PASS_ENV_VAR)
        self.assertTrue(p)


class TestMongoDBLinkCreation(TestCase):
    def test_create_mongodb_link_contains_password(self):
        password_ = '12atu4Wr'
        link = _create_mongodb_link(password_=password_)
        self.assertIn(password_, link)

    def test_final_mongodb_link_contains_password(self):
        p = password(PASS_ENV_VAR)
        link = mongo_db_link()
        self.assertIn(p, link)
