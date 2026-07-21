import unittest

from kong_deck_gateway.route_collisions import route_collisions, routes_are_unambiguous


class RouteCollisionTests(unittest.TestCase):
    def test_distinct_methods_do_not_collide(self):
        routes = [{"name": "read", "hosts": ["api.example.com"], "paths": ["/orders"], "methods": ["GET"]}, {"name": "write", "hosts": ["api.example.com"], "paths": ["/orders"], "methods": ["POST"]}]
        self.assertTrue(routes_are_unambiguous(routes))

    def test_overlapping_method_is_reported(self):
        routes = [{"name": "orders-a", "hosts": ["API.EXAMPLE.COM"], "paths": ["/orders"], "methods": ["GET"]}, {"name": "orders-b", "hosts": ["api.example.com"], "paths": ["/orders"], "methods": ["GET", "POST"]}]
        self.assertEqual(("orders-a:orders-b",), route_collisions(routes))

    def test_route_without_methods_overlaps_all_methods(self):
        routes = [{"name": "catch-all", "hosts": ["api.example.com"], "paths": ["/orders"]}, {"name": "read", "hosts": ["api.example.com"], "paths": ["/orders"], "methods": ["GET"]}]
        self.assertEqual(("catch-all:read",), route_collisions(routes))


if __name__ == "__main__":
    unittest.main()
