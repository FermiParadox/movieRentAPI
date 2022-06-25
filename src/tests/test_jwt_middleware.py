from unittest import TestCase

from src.middleware.jwt_middleware import JWT_PROTECTED_PATHS, JWT_IGNORED_PATHS


class TestJWTProtectedPaths(TestCase):
    def test_more_than_0_protected(self):
        self.assertGreater(len(JWT_PROTECTED_PATHS), 0)

    def test_at_least_1_not_protected(self):
        self.assertGreaterEqual(len(JWT_IGNORED_PATHS), 1)
