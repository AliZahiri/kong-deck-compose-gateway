import unittest

from kong_deck_gateway.config_schema_contract import config_schema_is_compatible, config_schema_violations


class GatewayConfigSchemaVersionGateTests(unittest.TestCase):
    def test_supported_reviewed_schema_passes(self):
        evidence = {"declared_schema_version": "v2", "supported_schema_version": "v2", "config_sha256": "a" * 64, "rollback_snapshot_sha256": "b" * 64, "deck_diff_reviewed": True}
        self.assertTrue(config_schema_is_compatible(evidence))

    def test_unsupported_or_unreviewed_schema_fails(self):
        violations = config_schema_violations({"declared_schema_version": "v0", "supported_schema_version": "v3", "config_sha256": "bad", "rollback_snapshot_sha256": "", "deck_diff_reviewed": False})
        self.assertEqual(violations, ("declared_schema_version_is_invalid", "config_sha256_is_invalid", "rollback_snapshot_sha256_is_invalid", "deck_diff_must_be_reviewed"))
