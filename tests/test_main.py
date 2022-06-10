from unittest import TestCase
from fastapi.testclient import TestClient

from endpoint_paths import ALL_MOVIES, MOVIES_BY_CAT
from main import app


class TestAllMovies(TestCase):
    def test_ok_response(self):
        response = TestClient(app=app).get(ALL_MOVIES.full)
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')


class TestMovies(TestCase):
    def test_ok_response(self):
        response = TestClient(app=app).post(url=MOVIES_BY_CAT.full,
                                            json={'categories': ['comedy', 'action']})
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')

    def test_wrong_category_responds_422(self):
        response = TestClient(app=app).post(url=MOVIES_BY_CAT.full,
                                            json={'categories': ['kdf9356a', 'action']})
        code = response.status_code
        self.assertEqual(422, code, msg=f'Response code: {code}')
