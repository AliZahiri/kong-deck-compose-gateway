import unittest

from kong_deck_gateway.admin_audit_retention import admin_audit_retention_is_safe, admin_audit_retention_violations


class AdminAuditRetentionContractTests(unittest.TestCase):
    def test_reviewable_audit_policy_passes(self):
        policy = {"retention_days": 30, "capture_actor": True, "capture_request_id": True, "redact_credentials": True, "sink": "http"}
        self.assertTrue(admin_audit_retention_is_safe(policy))

    def test_short_untraceable_unredacted_policy_fails(self):
        violations = admin_audit_retention_violations({"retention_days": 1, "capture_actor": False, "capture_request_id": False, "redact_credentials": False, "sink": "file"})
        self.assertIn("retention_days_must_be_between_7_and_365", violations)
        self.assertIn("actor_capture_is_required", violations)
        self.assertIn("request_id_capture_is_required", violations)
        self.assertIn("credential_redaction_is_required", violations)
        self.assertIn("audit_sink_must_be_supported", violations)


if __name__ == "__main__":
    unittest.main()
