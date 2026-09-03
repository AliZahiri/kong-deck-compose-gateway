import unittest

from kong_deck_gateway.regex_route_safety import regex_route_safety_violations, regex_routes_are_safe


class GatewayRegexRouteSafetyTests(unittest.TestCase):
    def test_bounded_absolute_regex_passes(self):
        routes = [{"paths": [r"~/orders/[0-9]+$"]}, {"paths": ["/health"]}]
        self.assertTrue(regex_routes_are_safe(routes))

    def test_relative_nested_and_oversized_patterns_fail(self):
        routes = [{"paths": ["~orders", r"~/(a+)+$", "~/" + "a" * 300]}]
        violations = regex_route_safety_violations(routes)
        self.assertIn("route_0:path_0:regex_pattern_must_start_with_slash", violations)
        self.assertIn("route_0:path_1:potential_nested_quantifier_is_forbidden", violations)
        self.assertIn("route_0:path_2:regex_pattern_exceeds_length_budget", violations)

    def test_invalid_policy_and_route_shape_fail(self):
        self.assertEqual(("routes_must_be_a_list",), regex_route_safety_violations({}))
        with self.assertRaises(ValueError):
            regex_route_safety_violations([], maximum_pattern_length=0)
