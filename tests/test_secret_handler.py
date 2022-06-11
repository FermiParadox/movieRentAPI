from unittest import TestCase, mock

from secret_handler import mongo_db_link, _warn_no_secrets_file, warn_and_import_from_config


class TestMongoDBLink(TestCase):
    def test_warn_no_secrets_file_indeed_warns(self):
        with self.assertWarns(Warning):
            _warn_no_secrets_file()

    def test_mongo_db_link_non_empty(self):
        link = mongo_db_link()
        self.assertNotEqual('', link)
        self.assertIsInstance(link, str)

    def test_warn_and_import_from_config(self):
        with self.assertWarns(Warning):
            link = warn_and_import_from_config()
            self.assertNotEqual('', link)
            self.assertIsInstance(link, str)
