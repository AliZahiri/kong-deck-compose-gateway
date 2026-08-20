import unittest

from kong_deck_gateway.config_provenance import config_provenance_is_valid, config_provenance_violations


class GatewayConfigProvenanceGateTests(unittest.TestCase):
    def test_reviewed_immutable_production_config_passes(self):
        evidence = {"config_sha256": "a" * 64, "reviewed_by": "platform-reviewer", "target_environment": "production", "deck_diff_reviewed": True}
        self.assertTrue(config_provenance_is_valid(evidence))

    def test_missing_or_unreviewed_provenance_fails(self):
        violations = config_provenance_violations({"config_sha256": "bad", "reviewed_by": "", "target_environment": "development", "deck_diff_reviewed": False})
        self.assertEqual(violations, ("config_sha256_is_invalid", "reviewed_by_is_required", "target_environment_is_not_allowed", "deck_diff_must_be_reviewed"))
