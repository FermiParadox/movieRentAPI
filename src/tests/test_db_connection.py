from unittest import TestCase

from mongoengine import disconnect
from pymongo.mongo_client import MongoClient

from src.data.database import connect, DBName, connect_to_production_db
from src.secret_handler import MongoDBLink


class Test(TestCase):
    def test_connect(self):
        disconnect()
        cl = connect(db=DBName.test, link=MongoDBLink().link())
        self.assertIsInstance(cl, MongoClient)
        disconnect()

    def test_connection_to_production(self):
        disconnect()
        cl = connect_to_production_db()
        self.assertIsInstance(cl, MongoClient)
        disconnect()
