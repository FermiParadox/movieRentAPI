from unittest import TestCase

from src.data.database import db_connection, db_movies, db_users
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


class TestDatabase(TestCase):
    def test_connection(self):
        self.assertIsInstance(db_connection(), AsyncIOMotorDatabase)

    def test_movies(self):
        self.assertIsInstance(db_movies, AsyncIOMotorCollection)

    def test_users(self):
        self.assertIsInstance(db_users, AsyncIOMotorCollection)
