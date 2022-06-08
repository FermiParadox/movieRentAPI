from unittest import TestCase

from endpoint_paths import EndPointPath, HOME, PathCreationError


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
