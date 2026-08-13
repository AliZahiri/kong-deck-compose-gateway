import unittest

from kong_deck_gateway.request_schema_contract import gateway_request_schema_is_safe, gateway_request_schema_violations


class GatewayRequestSchemaContractTests(unittest.TestCase):
    def test_bounded_json_contract_passes(self):
        contract = {"content_types": ["application/json"], "schema_enforced": True, "max_body_bytes": 4096, "required_fields": ["name"]}
        self.assertTrue(gateway_request_schema_is_safe(contract))

    def test_non_json_unbounded_and_duplicate_contract_fails(self):
        contract = {"content_types": ["application/json", "text/plain"], "schema_enforced": True, "max_body_bytes": 20_000_000, "required_fields": ["name", "name"]}
        violations = gateway_request_schema_violations(contract)
        self.assertIn("schema_enforcement_requires_json_only", violations)
        self.assertIn("max_body_bytes_must_be_bounded", violations)
        self.assertIn("required_fields_must_be_unique_non_empty_strings", violations)


if __name__ == "__main__":
    unittest.main()
