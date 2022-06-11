from unittest import TestCase

from secret_handler import mongo_db_link, _warn_no_secrets_file

"""To ensure those tests run normally, set the environment var for this file as well.
See https://stackoverflow.com/a/42708480.
"""


class TestPasswordExtraction(TestCase):
    def test_warn_no_secrets_file_indeed_warns(self):
        with self.assertWarns(Warning):
            _warn_no_secrets_file()


class TestMongoDBLink(TestCase):
    def test_mongo_db_link_non_empty(self):
        link = mongo_db_link()
        self.assertNotEqual('', link)
