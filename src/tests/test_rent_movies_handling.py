from datetime import datetime
from unittest import TestCase

from src.data.crud import RentedMovieHandler, RentedMovieModifier, RentDaysHandler
from src.utils import ResponseCodeBracket


class TestRentedMovieHandler(TestCase):
    def test_rent_response_on_successful_modification_is_ok(self):
        response = RentedMovieHandler().rent_response(modified=True, movie_id=1)
        code = response.status_code
        self.assertTrue(ResponseCodeBracket().code_2xx(code=code), msg=f'Response code: {code}')

    def test_rent_response_on_failed_modification_is_not_ok(self):
        response = RentedMovieHandler().rent_response(modified=False, movie_id=1)
        code = response.status_code
        self.assertFalse(ResponseCodeBracket().code_2xx(code=code), msg=f'Response code: {code}')


class TestRentedMovieModifier(TestCase):
    def test_rent_movie_str(self):
        s = RentedMovieModifier().rent_movie_str(movie_id=1, date='2022-06-13')
        self.assertEqual('1:2022-06-13', s)


class TestRentDaysHandler(TestCase):
    def test__days_from_today_until_today_is_0(self):
        current_date_str = RentDaysHandler().current_date_str()
        days = RentDaysHandler()._days(start_day=current_date_str)
        self.assertEqual(0, days)

    def test_charged_days_from_today_until_today_is_1(self):
        current_date_str = RentDaysHandler().current_date_str()
        days = RentDaysHandler().charged_days(start_day=current_date_str)
        self.assertEqual(1, days)
