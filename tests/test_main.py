from unittest import TestCase
from fastapi.testclient import TestClient

from main import app

print(f"Tests in {__name__} don't fail when run individually.\n"
      f"They do fail when running all tests in /tests.\n"
      f"There's probably some bug.")

client = TestClient(app=app)
EXISTING_MOVIE_ID = '2'


class TestAllMovies(TestCase):
    def setUp(self) -> None:
        from routers._endpoint_paths import ALL_MOVIES
        self.url = ALL_MOVIES.full

    def test_ok_response(self):
        response = client.get(self.url)
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')

    def test_response_contains_dict(self):
        response = client.get(self.url)
        data = response.json()
        self.assertIsInstance(data, dict)


class TestMoviesByCategory(TestCase):
    def setUp(self) -> None:
        from routers._endpoint_paths import MOVIES_BY_CAT
        self.url = MOVIES_BY_CAT.full

    def test_response_contains_list(self):
        response = client.post(url=self.url,
                               json={'categories': ['comedy', 'action']})
        data = response.json()
        self.assertIsInstance(data, list)

    def test_no_category_responds_422(self):
        response = client.post(url=self.url,
                               json={})
        code = response.status_code
        self.assertEqual(422, code, msg=f'Response code: {code}')

    def test_wrong_category_responds_422(self):
        response = client.post(url=self.url,
                               json={'categories': ['kdf9356a', 'action']})
        code = response.status_code
        self.assertEqual(422, code, msg=f'Response code: {code}')


class TestMovieByID(TestCase):
    def setUp(self) -> None:
        from routers._endpoint_paths import MOVIE_BY_ID
        # FastAPI's testing might be bugged, hence the dirty testing below.
        # (When calling TestClient with `params` it ignores them)
        self.url = MOVIE_BY_ID.stripped_relative
        self.url_for_movie_2 = self.url + EXISTING_MOVIE_ID

    def test_ok_response(self):
        response = client.get(self.url_for_movie_2)
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')

    def test_wrong_id_responds_422(self):
        response = client.get(url=self.url + '65234234')
        code = response.status_code
        self.assertEqual(422, code, msg=f'Response code: {code}')

    def test_details_id_title(self):
        response = client.get(self.url_for_movie_2)
        self.assertIn('title', response.json())
        self.assertIn('id_', response.json())
        self.assertIn('categories', response.json())
        self.assertIn('details', response.json())

    def test_categories_not_empty(self):
        response = client.get(self.url_for_movie_2)
        self.assertTrue(response.json()['categories'])


class TestRentMovie(TestCase):
    def setUp(self) -> None:
        from routers._endpoint_paths import RENT, RETURN

        self.test_user_id = 1

        self.rent_url = RENT.full
        self.rent_url_movie2 = self.rent_url + EXISTING_MOVIE_ID

        self.return_url = RETURN.full
        self.return_url_movie2 = self.return_url + EXISTING_MOVIE_ID

    def test_rent_ok(self):
        response = client.put(self.rent_url_movie2, json={"id_": self.test_user_id})
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')

    def test_rent_movie_raises_422_when_user_no_exist(self):
        response = client.put(self.rent_url_movie2, json={"id_": 46999345236})
        code = response.status_code
        self.assertEqual(422, code)

    def test_rent_movie_raises_422_when_movie_no_exist(self):
        response = client.put(self.return_url + '8293753', json={"id_": self.test_user_id})
        code = response.status_code
        self.assertEqual(422, code)

    def test_return_movie_ok(self):
        response = client.put(self.return_url_movie2, json={"id_": self.test_user_id})
        code = response.status_code
        self.assertTrue(response.ok, msg=f'Response code: {code}')

    def test_return_movie_raises_422_when_user_no_exist(self):
        response = client.put(self.return_url_movie2, json={"id_": 46999345236})
        code = response.status_code
        self.assertEqual(422, code)

    def test_return_movie_raises_422_when_movie_no_exist(self):
        response = client.put(self.return_url + '8293753', json={"id_": self.test_user_id})
        code = response.status_code
        self.assertEqual(422, code)
