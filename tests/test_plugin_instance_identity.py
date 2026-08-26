import unittest

from kong_deck_gateway.plugin_instance_identity import plugin_instance_identities_are_valid, plugin_instance_identity_violations


class GatewayPluginInstanceIdentityTests(unittest.TestCase):
    def test_named_owned_route_plugin_passes(self):
        self.assertTrue(plugin_instance_identities_are_valid([{"name": "rate-limiting", "instance_name": "payments-rate-limit", "route": "payments", "tags": ["owner:platform"]}]))

    def test_duplicate_multiscope_unowned_plugin_fails(self):
        plugins = [{"name": "cors", "instance_name": "shared", "global": True, "tags": ["owner:platform"]}, {"name": "cors", "instance_name": "SHARED", "route": "api", "service": "backend", "tags": []}]
        violations = plugin_instance_identity_violations(plugins)
        self.assertIn("plugin_1:instance_name_must_be_unique", violations)
        self.assertIn("plugin_1:exactly_one_scope_is_required", violations)
        self.assertIn("plugin_1:owner_tag_is_required", violations)
