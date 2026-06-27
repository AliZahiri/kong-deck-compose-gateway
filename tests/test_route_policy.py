import unittest

from kong_deck_gateway.route_policy import route_policy_is_safe, route_policy_warnings


class RoutePolicyTests(unittest.TestCase):
    def test_constrained_route_passes(self):
        route = {"hosts": ["api.example.com"], "paths": ["/v1"], "strip_path": False}

        self.assertTrue(route_policy_is_safe(route))

    def test_wildcard_route_requires_approval(self):
        warnings = route_policy_warnings({"hosts": ["*"], "paths": ["/"], "strip_path": True})

        self.assertIn("wildcard_host_requires_approval", warnings)


if __name__ == "__main__":
    unittest.main()
