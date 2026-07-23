import unittest

from kong_deck_gateway.request_size import request_size_contract_is_valid, request_size_violations


class RequestSizeTests(unittest.TestCase):
    def test_bounded_post_route_passes(self):
        self.assertTrue(request_size_contract_is_valid({"methods": ["POST"], "allowed_payload_size_megabytes": 8}))

    def test_read_only_route_does_not_require_body_limit(self):
        self.assertTrue(request_size_contract_is_valid({"methods": ["GET"]}))

    def test_missing_and_oversized_limits_fail(self):
        self.assertEqual(("positive_request_size_limit_is_required",), request_size_violations({"methods": ["PATCH"]}))
        self.assertEqual(("request_size_limit_exceeds_platform_maximum",), request_size_violations({"methods": ["PUT"], "allowed_payload_size_megabytes": 64}))


if __name__ == "__main__":
    unittest.main()
