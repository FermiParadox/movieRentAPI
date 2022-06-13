from unittest import TestCase

from data.crud import RentedMovieModifier


class TestRentedMovieModifier(TestCase):
    def test_rent_movie_str(self):
        s = RentedMovieModifier().rent_movie_str(movie_id=1, date='2022-06-13')
        self.assertEqual('1:2022-06-13', s)
