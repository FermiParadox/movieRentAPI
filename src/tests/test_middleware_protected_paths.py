from unittest import TestCase

from src.middleware._base import ProtectedPaths


class TestProtectedPaths(TestCase):
    def test_0ignored_protects_all(self):
        all_paths = frozenset({'a', 'b'})
        paths = ProtectedPaths(all_paths=all_paths, ignored=frozenset())
        protected = paths.protected
        self.assertCountEqual(all_paths, protected)

    def test_all_ignored_protects_0(self):
        all_paths = frozenset({'a', 'b'})
        paths = ProtectedPaths(all_paths=all_paths, ignored=all_paths)
        protected = paths.protected
        self.assertCountEqual(frozenset(), protected)
