from unittest import TestCase

from mongoengine import disconnect
from pymongo.mongo_client import MongoClient

from src.data.database import db_connection
from src.secret_handler import MongoDBLink


class Test(TestCase):
    def test_connect(self):
        disconnect()
        cl = client(db_type=DBType.test, link=MongoDBLink().link())
        self.assertIsInstance(cl, MongoClient)
        disconnect()

    def test_connection_to_production(self):
        disconnect()
        cl = db_connection()
        self.assertIsInstance(cl, MongoClient)
        disconnect()
