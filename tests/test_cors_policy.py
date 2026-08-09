import unittest

from kong_deck_gateway.cors_policy import route_cors_policy_is_safe, route_cors_policy_violations


class RouteCorsPolicyGateTests(unittest.TestCase):
    def test_explicit_https_credentialed_origin_passes(self):
        routes = [{"route": "orders", "origins": ["https://app.example.com"], "allow_credentials": True, "methods": ["GET", "POST"], "preflight_max_age_seconds": 600}]
        self.assertTrue(route_cors_policy_is_safe(routes))

    def test_duplicate_insecure_wildcard_and_invalid_method_fail(self):
        routes = [{"route": "orders", "origins": ["*"], "allow_credentials": True, "methods": ["TRACE"], "preflight_max_age_seconds": 90000}, {"route": "orders", "origins": ["http://app.example.com/path"], "methods": ["GET"], "preflight_max_age_seconds": 60}]
        violations = route_cors_policy_violations(routes)
        self.assertIn("route_0:credentialed_cors_cannot_use_wildcard_origin", violations)
        self.assertIn("route_0:methods_are_invalid", violations)
        self.assertIn("route_0:preflight_max_age_is_invalid", violations)
        self.assertIn("route_1:name_must_be_unique", violations)
        self.assertIn("route_1:origin_must_be_an_https_origin", violations)

    def test_empty_input_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_route_cors_policy_is_required",), route_cors_policy_violations([]))
        with self.assertRaises(ValueError):
            route_cors_policy_violations([], maximum_preflight_age_seconds=-1)


if __name__ == "__main__":
    unittest.main()
