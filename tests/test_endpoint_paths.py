from unittest import TestCase

from endpoint_paths import EndPointPath, HOME


class TestEndPointPath(TestCase):
    def test_appended_to_base_path(self):
        relative = '/abcde'
        expected = HOME + relative
        path = EndPointPath(relative=relative).full
        self.assertEqual(expected, path)
