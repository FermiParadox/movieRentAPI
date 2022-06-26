from unittest import TestCase

from src.data.crud import RentingHandler, RentDays, ITransactionHandler, MovieHandlingResponse
from src.tests.test_models import MOCK_USER
from src.utils import ResponseCode

from src.data.crud import IRentedMovieDBModifier


class MockTransactionHandler(ITransactionHandler):
    def apply_cost(self, *_, **__):
        pass


class MockSuccessfulDBModifier(IRentedMovieDBModifier):
    def add(self, *_, **__):
        return True

    def delete(self, *_, **__):
        return True


class MockFailedDBModifier(IRentedMovieDBModifier):
    def add(self, *_, **__):
        return False

    def delete(self, *_, **__):
        return False


class TestRentedMovieHandler(TestCase):
    def test__rent_movie_responds_4xx_when_modification_fails(self):
        response = RentingHandler()._rent_movie(movie_id=2, user=MOCK_USER,
                                                db_modifier=MockFailedDBModifier())
        code = response.status_code
        self.assertTrue(ResponseCode().is_4xx(code=code), msg=f'Response code: {code}')

    def test__rent_movie_responds_2xx_when_modification_succeeds(self):
        response = RentingHandler()._rent_movie(movie_id=2, user=MOCK_USER,
                                                db_modifier=MockSuccessfulDBModifier())
        code = response.status_code
        self.assertTrue(ResponseCode().is_2xx(code=code), msg=f'Response code: {code}')


class TestRentResponse(TestCase):
    def test_rent_response_on_successful_modification_is_ok(self):
        response = MovieHandlingResponse().rent(modified=True, movie_id=1)
        code = response.status_code
        self.assertTrue(ResponseCode().is_2xx(code=code), msg=f'Response code: {code}')

    def test_rent_response_on_failed_modification_is_not_ok(self):
        response = MovieHandlingResponse().rent(modified=False, movie_id=1)
        code = response.status_code
        self.assertTrue(ResponseCode().is_4xx(code=code), msg=f'Response code: {code}')


class TestRentedMovieDecoder(TestCase):
    def test_decode_contains_movie_id_and_date(self):
        from src.data.crud import RentedMovieDateEncoder
        movie_id = '1'
        date = '2031-09-14'
        obj = RentedMovieDateEncoder().decoded_pair(f'{movie_id}{RentedMovieDateEncoder.STR_SEPARATOR}{date}')
        self.assertEqual(movie_id, obj.movie_id)
        self.assertEqual(date, obj.start_date)

    def test_rent_movie_str(self):
        from src.data.crud import RentedMovieDateEncoder

        date = '2022-06-13'
        movie_id = '1'
        result = RentedMovieDateEncoder().encoded_pair(movie_id=1, date=date)

        self.assertTrue(result.startswith(movie_id))
        self.assertTrue(result.endswith(date))


class TestRentDaysHandler(TestCase):
    def test__days_from_today_until_today_is_0(self):
        current_date_str = RentDays().current_date_str()
        days = RentDays()._days(start_day=current_date_str)
        self.assertEqual(0, days)

    def test_charged_days_from_today_until_today_is_1(self):
        current_date_str = RentDays().current_date_str()
        days = RentDays().charged_days(start_day=current_date_str)
        self.assertEqual(1, days)
