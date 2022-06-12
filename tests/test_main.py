from unittest import TestCase
from fastapi.testclient import TestClient

from main import app


class TestAllMovies(TestCase):
    def setUp(self) -> None:
        from routers._endpoint_paths import ALL_MOVIES
        self.url = ALL_MOVIES.full

    def test_ok_response(self):
        response = TestClient(app=app).get(self.url)
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')

    def test_response_contains_list(self):
        response = TestClient(app=app).get(self.url)
        data = response.json()
        self.assertIsInstance(data, list)


class TestMoviesByCategory(TestCase):
    def setUp(self) -> None:
        from routers._endpoint_paths import MOVIES_BY_CAT
        self.url = MOVIES_BY_CAT.full

    def test_response_contains_list(self):
        response = TestClient(app=app).post(url=self.url,
                                            json={'categories': ['comedy', 'action']})
        data = response.json()
        self.assertIsInstance(data, list)

    def test_no_category_responds_422(self):
        response = TestClient(app=app).post(url=self.url,
                                            json={})
        code = response.status_code
        self.assertEqual(422, code, msg=f'Response code: {code}')

    def test_wrong_category_responds_422(self):
        response = TestClient(app=app).post(url=self.url,
                                            json={'categories': ['kdf9356a', 'action']})
        code = response.status_code
        self.assertEqual(422, code, msg=f'Response code: {code}')
