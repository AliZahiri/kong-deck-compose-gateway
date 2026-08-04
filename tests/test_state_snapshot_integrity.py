import unittest

from kong_deck_gateway.state_snapshot_integrity import deck_state_snapshot_is_rollback_ready, state_snapshot_integrity_violations


DIGEST = "a" * 64


class DeckStateSnapshotIntegrityGateTests(unittest.TestCase):
    def test_encrypted_verified_matching_snapshot_passes(self):
        snapshot = {"snapshot_id": "deck-20260804", "kong_version": "3.9", "expected_sha256": DIGEST, "stored_sha256": DIGEST, "encrypted_at_rest": True, "restore_verified": True}
        self.assertTrue(deck_state_snapshot_is_rollback_ready(snapshot))

    def test_missing_metadata_mismatch_and_unverified_snapshot_fail(self):
        snapshot = {"snapshot_id": "", "kong_version": "", "expected_sha256": DIGEST, "stored_sha256": "b" * 64, "encrypted_at_rest": False, "restore_verified": False}
        violations = state_snapshot_integrity_violations(snapshot)
        self.assertIn("snapshot_id_is_required", violations)
        self.assertIn("kong_version_is_required", violations)
        self.assertIn("stored_snapshot_digest_mismatch", violations)
        self.assertIn("snapshot_must_be_encrypted_at_rest", violations)
        self.assertIn("snapshot_restore_must_be_verified", violations)

    def test_malformed_digest_fails(self):
        violations = state_snapshot_integrity_violations({"expected_sha256": "BAD", "stored_sha256": DIGEST})
        self.assertIn("expected_sha256_is_invalid", violations)


if __name__ == "__main__":
    unittest.main()
