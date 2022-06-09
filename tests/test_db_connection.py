from unittest import TestCase
from pymongo.mongo_client import MongoClient

from db.database import client


class Test(TestCase):
    def test_client(self):
        cl = client()
        self.assertIsInstance(cl, MongoClient)
