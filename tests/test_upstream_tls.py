import unittest

from kong_deck_gateway.upstream_tls import upstream_tls_is_safe, upstream_tls_violations


class UpstreamTlsTests(unittest.TestCase):
    def test_verified_https_upstream_passes(self):
        service = {"protocol": "https", "host": "orders.internal", "tls_verify": True, "tls_verify_depth": 3, "ca_certificates": ["internal-ca-id"]}
        self.assertTrue(upstream_tls_is_safe(service))

    def test_plaintext_and_disabled_verification_are_reported(self):
        violations = upstream_tls_violations({"protocol": "http", "host": "orders.internal", "tls_verify": False, "tls_verify_depth": 3, "ca_certificates": ["internal-ca-id"]})
        self.assertIn("upstream_protocol_must_be_https", violations)
        self.assertIn("tls_verification_must_be_enabled", violations)

    def test_ca_reference_and_bounded_depth_are_required(self):
        violations = upstream_tls_violations({"protocol": "https", "host": "orders.internal", "tls_verify": True, "tls_verify_depth": 0, "ca_certificates": []})
        self.assertIn("tls_verify_depth_must_be_between_1_and_9", violations)
        self.assertIn("trusted_ca_reference_is_required", violations)


if __name__ == "__main__":
    unittest.main()
