import unittest

from kong_deck_gateway.plugin_order import plugin_order_is_safe, plugin_order_warnings


class PluginOrderTests(unittest.TestCase):
    def test_auth_first_chain_passes(self):
        self.assertTrue(plugin_order_is_safe(["jwt", "rate-limiting", "request-transformer"]))

    def test_transformer_before_auth_is_reported(self):
        warnings = plugin_order_warnings(["request-transformer", "jwt"])

        self.assertIn("request-transformer_runs_before_auth", warnings)


if __name__ == "__main__":
    unittest.main()
