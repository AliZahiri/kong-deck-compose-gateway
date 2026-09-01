import unittest

from kong_deck_gateway.credential_revocation import credential_revocation_is_effective, credential_revocation_violations


class ConsumerCredentialRevocationTests(unittest.TestCase):
    def test_bounded_audited_revocation_passes(self):
        evidence = {"credential_id": "cred-1", "consumer_id": "consumer-1", "change_ticket": "SEC-42", "audit_event_id": "audit-1", "revoked_at": "2026-09-01T00:00:00Z", "gateway_rejected_at": "2026-09-01T00:01:00Z", "authentication_cache_purged": True, "revoked_credential_rejected": True}
        self.assertTrue(credential_revocation_is_effective(evidence))

    def test_late_unpurged_revocation_fails(self):
        evidence = {"credential_id": "cred-1", "consumer_id": "consumer-1", "change_ticket": "SEC-42", "audit_event_id": "audit-1", "revoked_at": "2026-09-01T00:00:00Z", "gateway_rejected_at": "2026-09-01T00:10:00Z", "authentication_cache_purged": False, "revoked_credential_rejected": False}
        violations = credential_revocation_violations(evidence)
        self.assertIn("revocation_propagation_budget_exceeded", violations)
        self.assertIn("authentication_cache_must_be_purged", violations)
        self.assertIn("revoked_credential_must_be_rejected", violations)
