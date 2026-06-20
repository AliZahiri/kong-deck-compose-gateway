import unittest

from kong_deck_gateway.policy import request_size_limit_plugin


class GatewayPolicyTests(unittest.TestCase):
    def test_request_size_limit_plugin_uses_kong_plugin_name(self):
        plugin = request_size_limit_plugin(10, route_name="uploads")

        self.assertEqual(plugin["name"], "request-size-limiting")
        self.assertEqual(plugin["config"]["allowed_payload_size"], 10)
        self.assertEqual(plugin["route"]["name"], "uploads")

    def test_request_size_limit_must_be_positive(self):
        with self.assertRaises(ValueError):
            request_size_limit_plugin(0)


if __name__ == "__main__":
    unittest.main()
