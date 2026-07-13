import unittest

from kong_deck_gateway.request_id_policy import request_id_is_safe, request_id_warnings


class RequestIdPolicyTests(unittest.TestCase):
    def test_standard_request_id_passes(self):
        self.assertTrue(request_id_is_safe("X-Request-ID", "req-123"))

    def test_oversized_request_id_is_reported(self):
        warnings = request_id_warnings("X-Request-ID", "x" * 129)

        self.assertIn("request_id_value_exceeds_max_length", warnings)


if __name__ == "__main__":
    unittest.main()
