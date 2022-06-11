from unittest import TestCase

from mongoengine import disconnect
from pymongo.mongo_client import MongoClient

from data.database import connect, DBName, connect_to_production_db


class Test(TestCase):
    def test_connect(self):
        disconnect()
        cl = connect(db=DBName.test)
        self.assertIsInstance(cl, MongoClient)
        disconnect()

    def test_connection_to_production(self):
        disconnect()
        cl = connect_to_production_db()
        self.assertIsInstance(cl, MongoClient)
        disconnect()
