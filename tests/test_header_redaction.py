import unittest

from kong_deck_gateway.header_redaction import header_redaction_is_safe, header_redaction_violations


class GatewaySensitiveHeaderRedactionContractTests(unittest.TestCase):
    def test_case_insensitive_complete_policy_passes(self):
        self.assertTrue(header_redaction_is_safe({"headers": ["Authorization", "COOKIE", "X-API-Key"], "case_insensitive": True, "retain_request_id": True}))

    def test_incomplete_policy_reports_controls(self):
        violations = header_redaction_violations({"headers": ["authorization"], "case_insensitive": False, "retain_request_id": False})
        self.assertEqual(violations, ("required_sensitive_headers_are_missing", "case_insensitive_matching_is_required", "request_id_retention_is_required"))


if __name__ == "__main__":
    unittest.main()
