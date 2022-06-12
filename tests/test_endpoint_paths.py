from unittest import TestCase

from routers._endpoint_paths import EndPointPath, HOME, PathCreationError


class TestEndPointPath(TestCase):
    def test_appended_to_base_path(self):
        relative = '/abcde'
        expected = HOME + relative
        path = EndPointPath(relative=relative).full
        self.assertEqual(expected, path)

    def test_not_starting_with_slash_raises(self):
        with self.assertRaises(PathCreationError):
            EndPointPath(relative='no_slash_at_start')

    def test_ends_with_slash_raises(self):
        with self.assertRaises(PathCreationError):
            EndPointPath(relative='/slash_at_end/')

    def test_full_path_strips_bracketed_content(self):
        obj = EndPointPath(relative='/hello/{num}')
        full_path = obj.full
        self.assertNotIn('{', full_path)
        self.assertNotIn('}', full_path)
