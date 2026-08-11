import unittest

from kong_deck_gateway.response_security_headers import response_security_header_violations, response_security_headers_are_safe


class GatewayResponseSecurityHeaderContractTests(unittest.TestCase):
    def test_public_https_route_with_required_headers_passes(self):
        route = {"public_https": True, "headers": {"Strict-Transport-Security": "max-age=31536000", "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY"}}
        self.assertTrue(response_security_headers_are_safe(route))

    def test_missing_and_duplicate_security_headers_fail(self):
        route = {"public_https": True, "headers": {"X-Content-Type-Options": "nosniff", "x-content-type-options": "nosniff"}}
        violations = response_security_header_violations(route)
        self.assertIn("header_names_must_be_unique_case_insensitively", violations)
        self.assertIn("x-frame-options_is_required", violations)
        self.assertIn("strict_transport_security_is_required_for_public_https", violations)


if __name__ == "__main__":
    unittest.main()
