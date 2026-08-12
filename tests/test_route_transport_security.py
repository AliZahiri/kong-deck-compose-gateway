import unittest

from kong_deck_gateway.route_transport_security import route_transport_security_is_safe, route_transport_security_violations


class GatewayRouteTransportSecurityGateTests(unittest.TestCase):
    def test_encrypted_public_and_permitted_internal_routes_pass(self):
        routes = [{"name": "public-api", "exposure": "public", "protocols": ["https"]}, {"name": "internal-health", "exposure": "internal", "protocols": ["http"]}]
        self.assertTrue(route_transport_security_is_safe(routes))

    def test_plaintext_duplicate_and_invalid_routes_fail(self):
        routes = [{"name": "public-api", "exposure": "public", "protocols": ["http"]}, {"name": "public-api", "exposure": "external", "protocols": ["https", "https"]}, {"name": "bad-protocol", "exposure": "public", "protocols": ["smtp"]}]
        violations = route_transport_security_violations(routes)
        self.assertIn("route_0:public_route_requires_encrypted_protocol", violations)
        self.assertIn("route_0:public_route_must_not_allow_insecure_protocol", violations)
        self.assertIn("route_1:name_must_be_unique", violations)
        self.assertIn("route_1:exposure_must_be_public_or_internal", violations)
        self.assertIn("route_2:protocols_must_be_a_unique_supported_list", violations)

    def test_empty_routes_and_strict_internal_policy_fail(self):
        self.assertEqual(("at_least_one_route_is_required",), route_transport_security_violations([]))
        violations = route_transport_security_violations([{"name": "internal", "exposure": "internal", "protocols": ["http"]}], allow_insecure_internal=False)
        self.assertIn("route_0:internal_route_must_not_allow_insecure_protocol", violations)
        with self.assertRaises(ValueError):
            route_transport_security_violations([], allow_insecure_internal="yes")


if __name__ == "__main__":
    unittest.main()
