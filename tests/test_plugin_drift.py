import unittest

from kong_deck_gateway.plugin_drift import plugin_drift_warnings, plugin_state_matches


class PluginDriftTests(unittest.TestCase):
    def test_matching_plugin_sets_pass(self):
        self.assertTrue(plugin_state_matches({"jwt", "rate-limiting"}, {"jwt", "rate-limiting"}))

    def test_protected_plugin_drift_is_reported(self):
        warnings = plugin_drift_warnings({"jwt", "rate-limiting"}, {"jwt"})

        self.assertIn("missing_live_plugin:rate-limiting", warnings)
        self.assertIn("protected_plugin_drift:rate-limiting", warnings)


if __name__ == "__main__":
    unittest.main()
