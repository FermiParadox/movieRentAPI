from unittest import TestCase

from mongoengine import disconnect
from pymongo.mongo_client import MongoClient

from data.database import client, DBName


class Test(TestCase):
    def test_client(self):
        cl = client(db=DBName.test)
        self.assertIsInstance(cl, MongoClient)
        disconnect()
