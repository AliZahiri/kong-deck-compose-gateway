import unittest

from kong_deck_gateway.forwarded_header_trust import forwarded_header_trust_is_safe, forwarded_header_trust_violations


class ForwardedHeaderTrustGateTests(unittest.TestCase):
    def test_explicit_proxy_network_and_replaced_headers_pass(self):
        services = [{"service": "orders", "strip_incoming_forwarded_headers": True, "replace_x_forwarded_for": True, "replace_x_forwarded_proto": True, "generate_request_id": True}]
        self.assertTrue(forwarded_header_trust_is_safe(services, trusted_proxy_cidrs=["10.0.0.0/24"]))

    def test_duplicate_service_and_unsanitized_headers_fail(self):
        services = [{"service": "orders", "strip_incoming_forwarded_headers": False, "replace_x_forwarded_for": True, "replace_x_forwarded_proto": False, "generate_request_id": False}, {"service": "orders", "strip_incoming_forwarded_headers": True, "replace_x_forwarded_for": True, "replace_x_forwarded_proto": True, "generate_request_id": True}]
        violations = forwarded_header_trust_violations(services, trusted_proxy_cidrs=["10.0.0.0/24"])
        self.assertIn("service_0:strip_incoming_forwarded_headers_must_be_enabled", violations)
        self.assertIn("service_0:replace_x_forwarded_proto_must_be_enabled", violations)
        self.assertIn("service_0:generate_request_id_must_be_enabled", violations)
        self.assertIn("service_1:name_must_be_unique", violations)

    def test_empty_or_noncanonical_proxy_policy_fails(self):
        self.assertEqual(("at_least_one_service_header_policy_is_required",), forwarded_header_trust_violations([], trusted_proxy_cidrs=["10.0.0.0/24"]))
        with self.assertRaises(ValueError):
            forwarded_header_trust_violations([], trusted_proxy_cidrs=["10.0.0.1/24"])


if __name__ == "__main__":
    unittest.main()
