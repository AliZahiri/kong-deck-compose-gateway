import unittest

from kong_deck_gateway.plugin_scope import plugin_scope_is_safe, plugin_scope_warnings


class PluginScopeTests(unittest.TestCase):
    def test_route_scoped_plugin_is_safe(self):
        self.assertTrue(plugin_scope_is_safe({"name": "rate-limiting", "route": {"name": "api"}}))

    def test_unscoped_plugin_requires_global_approval(self):
        warnings = plugin_scope_warnings({"name": "rate-limiting"})

        self.assertIn("plugin_scope_missing", warnings)
        self.assertTrue(plugin_scope_is_safe({"name": "correlation-id"}, allow_global=True))


if __name__ == "__main__":
    unittest.main()
