from unittest import TestCase

from mongoengine import disconnect
from pymongo.mongo_client import MongoClient

from data.database import connection, DBName


class Test(TestCase):
    def test_client(self):
        cl = connection(db=DBName.test)
        self.assertIsInstance(cl, MongoClient)
        disconnect()
