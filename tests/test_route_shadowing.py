import unittest

from kong_deck_gateway.route_shadowing import routes_are_unambiguous


class RouteShadowingTests(unittest.TestCase):
    def test_unique_named_paths_pass(self):
        self.assertTrue(routes_are_unambiguous([{"name": "orders", "path": "/orders"}]))

    def test_duplicate_route_identity_fails(self):
        self.assertFalse(routes_are_unambiguous([{"name": "orders", "path": "/orders"}, {"name": "orders", "path": "/orders"}]))
