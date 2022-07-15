from unittest import IsolatedAsyncioTestCase

from mongoengine import disconnect

from src.data.crud import RentedMovieCost, CostPerDay, UserInDB
from src.data.database import db_connection


class TestRentedMovieCost(IsolatedAsyncioTestCase):
    def test_cost_for_0days_is_0(self):
        cost = RentedMovieCost()._cost(0)
        self.assertEqual(0, cost)

    def test_cost_for_1days_is_equal_to_cost_per_1day_upto3(self):
        cost = RentedMovieCost()._cost(1)
        cost_per_1day_upto3 = int(CostPerDay.up_to_3days)
        self.assertEqual(cost_per_1day_upto3, cost)

    def test_cost_for_13days(self):
        cost = RentedMovieCost()._cost(13)
        expected = CostPerDay.up_to_3days * 3 + CostPerDay.above_3days * 10
        self.assertEqual(expected, cost)

    async def test_cost_of_movie_is_int_at_least_1(self):
        disconnect()
        db_connection()

        user = await UserInDB(user_id=1).user()
        cost = await RentedMovieCost().cost_of_movie(user=user, movie_id=7)

        self.assertIsInstance(cost, int)
        self.assertGreaterEqual(cost, 1)

        disconnect()
