import unittest

from kong_deck_gateway.route_preflight import route_preflight_violations, routes_are_ready_for_sync


class RoutePreflightTests(unittest.TestCase):
    def test_authenticated_bounded_route_is_ready(self):
        routes = [{"name": "orders", "plugins": ["jwt"], "methods": ["POST"], "allowed_payload_size_megabytes": 8}]
        self.assertTrue(routes_are_ready_for_sync(routes))

    def test_authentication_and_request_size_failures_are_combined(self):
        violations = route_preflight_violations([{"name": "orders", "plugins": [], "methods": ["POST"]}])
        self.assertIn("orders:approved_authentication_plugin_is_required", violations)
        self.assertIn("orders:positive_request_size_limit_is_required", violations)

    def test_empty_route_set_does_not_claim_readiness(self):
        self.assertFalse(routes_are_ready_for_sync([]))


if __name__ == "__main__":
    unittest.main()
