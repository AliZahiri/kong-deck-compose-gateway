import unittest

from kong_deck_gateway.plugin_secret_references import plugin_secret_reference_violations, plugin_secret_references_are_safe


class PluginConfigSecretReferenceGateTests(unittest.TestCase):
    def test_environment_referenced_secret_passes(self):
        settings = [{"name": "token", "sensitive": True, "value": "${KONG_PLUGIN_TOKEN}"}]
        self.assertTrue(plugin_secret_references_are_safe(settings))

    def test_literal_and_duplicate_secret_reference_fail(self):
        settings = [{"name": "token", "sensitive": True, "value": "plain-secret"}, {"name": "key", "sensitive": True, "value": "${KONG_PLUGIN_TOKEN}"}, {"name": "backup", "sensitive": True, "value": "${KONG_PLUGIN_TOKEN}"}]
        violations = plugin_secret_reference_violations(settings)
        self.assertIn("setting_0:sensitive_value_must_be_environment_reference", violations)
        self.assertIn("setting_2:secret_reference_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()
