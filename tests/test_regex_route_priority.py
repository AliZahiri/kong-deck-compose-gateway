import unittest

from kong_deck_gateway.regex_route_priority import regex_route_priorities_are_safe, regex_route_priority_violations


class RegexRoutePriorityGateTests(unittest.TestCase):
    def test_explicit_distinct_regex_priorities_pass(self):
        routes = [{"paths": [r"~/orders/\d+$"], "regex_priority": 20}, {"paths": [r"~/orders/\d+/lines"], "regex_priority": 10}, {"paths": ["/health"]}]
        self.assertTrue(regex_route_priorities_are_safe(routes, maximum_regex_routes=2))

    def test_malformed_duplicate_and_excessive_regex_routes_fail(self):
        routes = [{"paths": ["~"], "regex_priority": 0}, {"paths": ["~orders"], "regex_priority": 0}, {"paths": ["~/ready"], "regex_priority": True}]
        violations = regex_route_priority_violations(routes, maximum_regex_routes=2)
        self.assertIn("route_0:path_0:regex_pattern_is_required", violations)
        self.assertIn("route_1:path_0:regex_pattern_must_start_with_slash", violations)
        self.assertIn("route_1:regex_priority_must_be_unique", violations)
        self.assertIn("route_2:regex_priority_must_be_a_non_negative_integer", violations)
        self.assertIn("regex_route_count_exceeds_maximum", violations)

    def test_invalid_regex_route_limit_fails(self):
        with self.assertRaises(ValueError):
            regex_route_priority_violations([], maximum_regex_routes=-1)


if __name__ == "__main__":
    unittest.main()
