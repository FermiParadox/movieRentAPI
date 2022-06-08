from unittest import TestCase
from fastapi.testclient import TestClient

from endpoint_paths import ALL_MOVIES
from main import app


class TestAllMovies(TestCase):
    def test_ok_response(self):
        response = TestClient(app=app).get(ALL_MOVIES.full)
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')
