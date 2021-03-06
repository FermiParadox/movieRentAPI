from unittest import TestCase

from src.utils import ResponseCode


class TestResponseCodeBracket(TestCase):
    def test_code_2xx_is_true(self):
        self.assertTrue(ResponseCode().is_2xx(200))
        self.assertTrue(ResponseCode().is_2xx(202))
        self.assertTrue(ResponseCode().is_2xx(299))

    def test_code_3xx_is_true(self):
        self.assertTrue(ResponseCode().is_3xx(300))
        self.assertTrue(ResponseCode().is_3xx(302))
        self.assertTrue(ResponseCode().is_3xx(399))

    def test_code_4xx_is_true(self):
        self.assertTrue(ResponseCode().is_4xx(400))
        self.assertTrue(ResponseCode().is_4xx(402))
        self.assertTrue(ResponseCode().is_4xx(499))

    def test_code_5xx_is_true(self):
        self.assertTrue(ResponseCode().is_5xx(500))
        self.assertTrue(ResponseCode().is_5xx(502))
        self.assertTrue(ResponseCode().is_5xx(599))

    def test_code_2xx_is_false(self):
        self.assertFalse(ResponseCode().is_2xx(300))
        self.assertFalse(ResponseCode().is_2xx(402))
        self.assertFalse(ResponseCode().is_2xx(199))

    def test_code_3xx_is_false(self):
        self.assertFalse(ResponseCode().is_3xx(400))
        self.assertFalse(ResponseCode().is_3xx(502))
        self.assertFalse(ResponseCode().is_3xx(299))

    def test_code_4xx_is_false(self):
        self.assertFalse(ResponseCode().is_4xx(500))
        self.assertFalse(ResponseCode().is_4xx(202))
        self.assertFalse(ResponseCode().is_4xx(399))

    def test_code_5xx_is_false(self):
        self.assertFalse(ResponseCode().is_5xx(400))
        self.assertFalse(ResponseCode().is_5xx(202))
        self.assertFalse(ResponseCode().is_5xx(499))
