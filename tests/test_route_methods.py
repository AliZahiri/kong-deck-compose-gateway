import unittest

from kong_deck_gateway.route_methods import route_method_warnings, route_methods_are_safe


class RouteMethodTests(unittest.TestCase):
    def test_explicit_methods_pass(self):
        self.assertTrue(route_methods_are_safe(["GET", "POST"]))

    def test_unknown_method_is_reported(self):
        self.assertIn("route_method_is_not_allowed", route_method_warnings(["GET", "TRACE"]))


if __name__ == "__main__":
    unittest.main()
