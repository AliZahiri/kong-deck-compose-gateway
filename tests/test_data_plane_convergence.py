import unittest
from datetime import datetime, timezone

from kong_deck_gateway.data_plane_convergence import data_plane_convergence_violations, data_plane_has_converged


PROMOTED_AT = datetime(2026, 9, 1, tzinfo=timezone.utc)


class GatewayDataPlaneConvergenceTests(unittest.TestCase):
    def test_ready_matching_fresh_nodes_pass(self):
        nodes = [{"node_id": "dp-1", "ready": True, "config_digest": "sha256:abc", "observed_at": "2026-09-01T00:00:30Z"}, {"node_id": "dp-2", "ready": True, "config_digest": "sha256:abc", "observed_at": "2026-09-01T00:01:00Z"}]
        self.assertTrue(data_plane_has_converged("sha256:abc", nodes, promoted_at=PROMOTED_AT))

    def test_stale_mismatched_unready_node_fails(self):
        nodes = [{"node_id": "dp-1", "ready": False, "config_digest": "sha256:old", "observed_at": "2026-09-01T00:05:00Z"}]
        violations = data_plane_convergence_violations("sha256:new", nodes, promoted_at=PROMOTED_AT)
        self.assertIn("node_0:node_must_be_ready", violations)
        self.assertIn("node_0:config_digest_does_not_match", violations)
        self.assertIn("node_0:observation_is_outside_convergence_window", violations)

    def test_invalid_policy_time_fails(self):
        with self.assertRaises(ValueError):
            data_plane_convergence_violations("digest", [], promoted_at=datetime(2026, 9, 1))
