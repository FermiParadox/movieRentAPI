from unittest import TestCase

from data.crud import RentedMovieHandler
from utils import ResponseCodeBracket


class TestRentedMovieHandler(TestCase):
    def test_rent_response_on_successful_modification_is_ok(self):
        response = RentedMovieHandler().rent_response(modified=True, movie_id=1)
        code = response.status_code
        self.assertTrue(ResponseCodeBracket().code_2xx(code=code), msg=f'Response code: {code}')

    def test_rent_response_on_failed_modification_is_not_ok(self):
        response = RentedMovieHandler().rent_response(modified=False, movie_id=1)
        code = response.status_code
        self.assertFalse(ResponseCodeBracket().code_2xx(code=code), msg=f'Response code: {code}')
