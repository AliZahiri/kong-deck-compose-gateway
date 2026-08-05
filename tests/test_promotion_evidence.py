import unittest
from datetime import datetime, timezone

from kong_deck_gateway.promotion_evidence import gateway_promotion_evidence_is_complete, gateway_promotion_evidence_violations


NOW = datetime(2026, 8, 5, 10, 0, tzinfo=timezone.utc)
DIGEST = "a" * 64
REVISION = "b" * 40


class GatewayPromotionEvidenceGateTests(unittest.TestCase):
    def test_reviewed_applied_and_healthy_promotion_passes(self):
        evidence = {"desired_state_sha256": DIGEST, "applied_state_sha256": DIGEST, "source_revision": REVISION, "deck_version": "1.44.0", "diff_reviewed": True, "sync_succeeded": True, "post_sync_healthcheck_passed": True, "started_at": "2026-08-05T09:55:00Z", "completed_at": "2026-08-05T09:56:00Z"}
        self.assertTrue(gateway_promotion_evidence_is_complete(evidence, now=NOW))

    def test_mismatched_unreviewed_and_stale_evidence_fails(self):
        evidence = {"desired_state_sha256": DIGEST, "applied_state_sha256": "c" * 64, "source_revision": "short", "deck_version": "", "diff_reviewed": False, "sync_succeeded": False, "post_sync_healthcheck_passed": False, "started_at": "2026-08-05T09:55:00", "completed_at": "2026-08-01T00:00:00Z"}
        violations = gateway_promotion_evidence_violations(evidence, now=NOW)
        self.assertIn("applied_state_sha256_must_match_reviewed_state", violations)
        self.assertIn("source_revision_must_be_a_full_git_sha", violations)
        self.assertIn("deck_version_is_required", violations)
        self.assertIn("diff_reviewed_must_be_true", violations)
        self.assertIn("promotion_evidence_is_not_fresh", violations)
        self.assertIn("started_at_must_be_timezone_aware", violations)

    def test_invalid_age_policy_fails(self):
        with self.assertRaises(ValueError):
            gateway_promotion_evidence_violations({}, now=NOW, maximum_age_seconds=0)


if __name__ == "__main__":
    unittest.main()
