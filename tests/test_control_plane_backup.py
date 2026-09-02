import unittest
from datetime import datetime, timezone

from kong_deck_gateway.control_plane_backup import control_plane_backup_is_ready, control_plane_backup_violations


NOW = datetime(2026, 9, 2, 4, 0, tzinfo=timezone.utc)


class GatewayControlPlaneBackupEvidenceTests(unittest.TestCase):
    def test_fresh_encrypted_verified_backup_passes(self):
        evidence = {"schema_version": "3.0", "state_sha256": "sha256:" + "a" * 64, "encrypted_at_rest": True, "restore_parse_verified": True, "entity_count": 120, "created_at": "2026-09-02T03:00:00Z"}
        self.assertTrue(control_plane_backup_is_ready(evidence, now=NOW))

    def test_stale_unverified_incompatible_backup_fails(self):
        evidence = {"schema_version": "2.1", "state_sha256": "bad", "encrypted_at_rest": False, "restore_parse_verified": False, "entity_count": 0, "created_at": "2026-08-01T00:00:00Z"}
        violations = control_plane_backup_violations(evidence, now=NOW)
        self.assertIn("backup_schema_version_is_not_supported", violations)
        self.assertIn("backup_must_be_encrypted_at_rest", violations)
        self.assertIn("restore_parse_verification_is_required", violations)
        self.assertIn("backup_evidence_is_stale_or_future_dated", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            control_plane_backup_violations({}, now=NOW, maximum_age_seconds=0)
