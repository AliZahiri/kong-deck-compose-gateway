import unittest
from datetime import datetime, timezone

from kong_deck_gateway.data_plane_freshness import data_plane_configuration_is_fresh, data_plane_freshness_violations


NOW = datetime(2026, 8, 30, 8, 0, tzinfo=timezone.utc)
DIGEST = "sha256:" + "a" * 64


class GatewayDataPlaneFreshnessEvidenceTests(unittest.TestCase):
    def test_fresh_quorum_with_matching_configuration_passes(self):
        nodes = [
            {"node_id": "dp-1", "control_plane_id": "cp-prod", "sync_status": "ready", "config_digest": DIGEST, "plugin_schema_compatible": True, "observed_at": "2026-08-30T07:59:00Z"},
            {"node_id": "dp-2", "control_plane_id": "cp-prod", "sync_status": "ready", "config_digest": DIGEST, "plugin_schema_compatible": True, "observed_at": "2026-08-30T07:58:00+00:00"},
        ]
        self.assertTrue(data_plane_configuration_is_fresh(nodes, expected_config_digest=DIGEST, now=NOW))

    def test_stale_mismatched_and_unready_nodes_fail(self):
        nodes = [
            {"node_id": "dp-1", "control_plane_id": "cp-prod", "sync_status": "error", "config_digest": "sha256:" + "b" * 64, "plugin_schema_compatible": False, "observed_at": "2026-08-30T07:00:00Z"},
            {"node_id": "dp-1", "control_plane_id": "cp-prod", "sync_status": "ready", "config_digest": DIGEST, "plugin_schema_compatible": True, "observed_at": "2026-08-30T08:01:00Z"},
        ]
        violations = data_plane_freshness_violations(nodes, expected_config_digest=DIGEST, now=NOW)
        self.assertIn("node_0:config_digest_does_not_match_control_plane", violations)
        self.assertIn("node_0:observation_is_stale", violations)
        self.assertIn("node_1:node_id_must_be_unique", violations)
        self.assertIn("ready_data_plane_quorum_is_below_policy", violations)

    def test_invalid_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            data_plane_freshness_violations([], expected_config_digest="latest", now=NOW)
