from unittest import TestCase

from src.routers.endpoint_paths import HOME, EndpointPath, PathCreationError


class TestEndPointPath(TestCase):
    def test_appended_to_base_path(self):
        fastapi_format = '/abcde'
        expected = HOME + fastapi_format
        path = EndpointPath(fastapi_format=fastapi_format).full
        self.assertEqual(expected, path)

    def test_not_starting_with_slash_raises(self):
        with self.assertRaises(PathCreationError):
            EndpointPath(fastapi_format='no_slash_at_start')

    def test_ends_with_slash_raises(self):
        with self.assertRaises(PathCreationError):
            EndpointPath(fastapi_format='/slash_at_end/')

    def test_full_path_strips_bracketed_content(self):
        obj = EndpointPath(fastapi_format='/hello/{num}')
        full_path = obj.full
        self.assertNotIn('{', full_path)
        self.assertNotIn('}', full_path)
