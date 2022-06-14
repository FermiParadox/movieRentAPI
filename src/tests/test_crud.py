from unittest import TestCase

from src.data.crud import RentedMovieCost, CostPerDay


class TestRentedMovieCost(TestCase):
    def test_cost_for_0days_is_0(self):
        cost = RentedMovieCost().cost(0)
        self.assertEqual(0, cost)

    def test_cost_for_1days_is_equal_to_cost_per_1day_upto3(self):
        cost = RentedMovieCost().cost(1)
        cost_per_1day_upto3 = int(CostPerDay.up_to_3days)
        self.assertEqual(cost_per_1day_upto3, cost)

    def test_cost_for_13days(self):
        cost = RentedMovieCost().cost(13)
        expected = CostPerDay.up_to_3days * 3 + CostPerDay.above_3days * 10
        self.assertEqual(expected, cost)
