import unittest

from kong_deck_gateway.credential_rotation import credential_rotation_is_complete, credential_rotation_violations


class ConsumerCredentialRotationEvidenceTests(unittest.TestCase):
    def test_verified_bounded_rotation_without_secret_material_passes(self):
        evidence = {"consumer_id": "checkout", "old_credential_id": "cred-old", "new_credential_id": "cred-new", "new_credential_verified": True, "new_credential_verified_at": "2026-08-28T08:00:00Z", "old_credential_revoked": True, "old_credential_revoked_at": "2026-08-28T09:00:00Z", "authentication_failures_after_rotation": 0}
        self.assertTrue(credential_rotation_is_complete(evidence, maximum_overlap_seconds=7200))

    def test_revocation_before_verification_and_authentication_failures_fail(self):
        evidence = {"consumer_id": "checkout", "old_credential_id": "cred-old", "new_credential_id": "cred-new", "new_credential_verified": True, "new_credential_verified_at": "2026-08-28T10:00:00Z", "old_credential_revoked": True, "old_credential_revoked_at": "2026-08-28T09:00:00Z", "authentication_failures_after_rotation": 2}
        violations = credential_rotation_violations(evidence)
        self.assertIn("replacement_must_be_verified_before_revocation", violations)
        self.assertIn("post_rotation_authentication_failures_detected", violations)

    def test_secret_material_and_excessive_overlap_fail(self):
        evidence = {"consumer_id": "checkout", "old_credential_id": "cred-old", "new_credential_id": "cred-new", "token": "redacted-placeholder", "new_credential_verified": True, "new_credential_verified_at": "2026-08-27T08:00:00Z", "old_credential_revoked": True, "old_credential_revoked_at": "2026-08-28T10:00:00Z", "authentication_failures_after_rotation": 0}
        violations = credential_rotation_violations(evidence, maximum_overlap_seconds=3600)
        self.assertIn("credential_material_must_not_be_recorded", violations)
        self.assertIn("credential_overlap_exceeds_budget", violations)
