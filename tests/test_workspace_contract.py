import unittest

from kong_deck_gateway.workspace_contract import gateway_workspace_contract_is_satisfied, gateway_workspace_contract_violations


class GatewayWorkspaceContractGateTests(unittest.TestCase):
    def test_unique_matching_workspace_resources_pass(self):
        resources = [{"type": "service", "name": "orders", "workspace": "production", "tags": ["owner:payments", "env:production"]}, {"type": "route", "name": "orders-public", "workspace": "production", "tags": ["env:production"]}]
        self.assertTrue(gateway_workspace_contract_is_satisfied(resources, environment="production"))

    def test_cross_environment_duplicate_and_ambiguous_tags_fail(self):
        resources = [{"type": "service", "name": "orders", "workspace": "staging", "tags": ["env:staging"]}, {"type": "service", "name": "orders", "workspace": "production", "tags": ["env:production", "env:staging"]}]
        violations = gateway_workspace_contract_violations(resources, environment="production")
        self.assertIn("resource_0:workspace_must_match_environment", violations)
        self.assertIn("resource_0:must_have_one_matching_environment_tag", violations)
        self.assertIn("resource_1:type_and_name_must_be_unique", violations)
        self.assertIn("resource_1:must_have_one_matching_environment_tag", violations)

    def test_empty_resources_and_invalid_environment_fail(self):
        self.assertEqual(("at_least_one_resource_is_required",), gateway_workspace_contract_violations([], environment="staging"))
        with self.assertRaises(ValueError):
            gateway_workspace_contract_violations([], environment="")


if __name__ == "__main__":
    unittest.main()
