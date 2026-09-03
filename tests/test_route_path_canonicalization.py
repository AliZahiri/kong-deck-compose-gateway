import unittest

from kong_deck_gateway.route_path_canonicalization import route_path_canonicalization_violations, route_paths_are_canonical


class GatewayRoutePathCanonicalizationTests(unittest.TestCase):
    def test_canonical_and_regex_paths_pass(self):
        routes = [{"paths": ["/orders", "~/orders/[0-9]+$"]}]
        self.assertTrue(route_paths_are_canonical(routes))

    def test_ambiguous_paths_fail(self):
        routes = [{"paths": ["orders", "/orders//new", "/orders/../admin", "/files/%2Fsecret", "/trailing/"]}]
        violations = route_path_canonicalization_violations(routes)
        self.assertIn("route_0:path_0:path_must_be_absolute", violations)
        self.assertIn("route_0:path_1:duplicate_path_separator_is_forbidden", violations)
        self.assertIn("route_0:path_2:dot_segments_are_forbidden", violations)
        self.assertIn("route_0:path_3:encoded_path_separator_is_forbidden", violations)
        self.assertIn("route_0:path_4:trailing_slash_requires_explicit_policy", violations)

    def test_explicit_trailing_slash_policy_and_invalid_shape(self):
        self.assertTrue(route_paths_are_canonical([{"paths": ["/v1/"]}], allow_trailing_slash=True))
        self.assertEqual(("routes_must_be_a_list",), route_path_canonicalization_violations({}))
