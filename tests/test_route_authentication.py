import unittest

from kong_deck_gateway.route_authentication import route_authentication_coverage_is_complete, route_authentication_violations


class RouteAuthenticationTests(unittest.TestCase):
    def test_authenticated_and_owned_public_routes_pass(self):
        routes = [{"name": "orders", "plugins": ["jwt"]}, {"name": "health", "public": True, "owner": "platform", "public_reason": "load balancer probe"}]
        self.assertTrue(route_authentication_coverage_is_complete(routes))

    def test_unprotected_private_route_is_reported(self):
        self.assertEqual(("orders:approved_authentication_plugin_is_required",), route_authentication_violations([{"name": "orders", "plugins": []}]))

    def test_public_exception_requires_owner_and_reason(self):
        violations = route_authentication_violations([{"name": "health", "public": True}])
        self.assertIn("health:public_route_owner_is_required", violations)
        self.assertIn("health:public_route_reason_is_required", violations)

    def test_empty_route_set_does_not_claim_coverage(self):
        self.assertFalse(route_authentication_coverage_is_complete([]))


if __name__ == "__main__":
    unittest.main()
