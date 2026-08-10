import unittest

from kong_deck_gateway.request_transformer_safety import request_transformer_is_safe, request_transformer_violations


class RequestTransformerSafetyGateTests(unittest.TestCase):
    def test_safe_non_protected_header_addition_passes(self):
        policy = {"header_changes": [{"name": "X-Client-Region", "operation": "add"}], "preserve_request_id": True}

        self.assertTrue(request_transformer_is_safe(policy))

    def test_protected_duplicate_and_invalid_changes_fail(self):
        policy = {"header_changes": [{"name": "Authorization", "operation": "remove"}, {"name": "authorization", "operation": "invalid"}], "preserve_request_id": False}

        violations = request_transformer_violations(policy)

        self.assertIn("change_0:protected_header_must_not_be_modified", violations)
        self.assertIn("change_1:header_name_must_be_unique", violations)
        self.assertIn("change_1:operation_is_invalid", violations)
        self.assertIn("request_id_preservation_is_required", violations)

    def test_non_list_configuration_fails(self):
        self.assertEqual(("header_changes_must_be_a_list",), request_transformer_violations({}))


if __name__ == "__main__":
    unittest.main()
