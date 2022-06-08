from unittest import TestCase
from fastapi.testclient import TestClient

from main import app


class TestAllMovies(TestCase):
    def test_ok_response(self):
        response = TestClient(app=app).get('http://127.0.0.1:8000/all_movies')
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')
