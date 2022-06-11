from unittest import TestCase

from mongoengine import disconnect
from pymongo.mongo_client import MongoClient

from data.database import connect, DBName


class Test(TestCase):
    def test_connect(self):
        cl = connect(db=DBName.test)
        self.assertIsInstance(cl, MongoClient)
        disconnect()
