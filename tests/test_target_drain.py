import unittest

from kong_deck_gateway.target_drain import target_drain_violations, target_is_safe_to_remove


def drained_target():
    return {"target": "10.0.0.8:8080", "configured_weight": 0, "active_connections": 0, "consecutive_zero_connection_checks": 4, "drain_seconds": 45, "replacement_healthy": True}


class TargetDrainPolicyTests(unittest.TestCase):
    def test_zero_weight_observed_drain_with_replacement_passes(self):
        self.assertTrue(target_is_safe_to_remove(drained_target()))

    def test_weight_connections_duration_and_replacement_failures_are_combined(self):
        evidence = drained_target()
        evidence.update({"configured_weight": 10, "active_connections": 2, "consecutive_zero_connection_checks": 1, "drain_seconds": 5, "replacement_healthy": False})

        violations = target_drain_violations(evidence)

        self.assertIn("target_weight_must_be_zero", violations)
        self.assertIn("active_connections_must_be_zero", violations)
        self.assertIn("zero_connection_observations_below_minimum", violations)
        self.assertIn("drain_duration_below_minimum", violations)
        self.assertIn("healthy_replacement_must_be_confirmed", violations)

    def test_boolean_counters_and_invalid_policy_values_are_rejected(self):
        evidence = drained_target()
        evidence["active_connections"] = False
        self.assertIn("active_connections_must_be_zero", target_drain_violations(evidence))
        with self.assertRaises(ValueError):
            target_drain_violations(evidence, minimum_checks=0)


if __name__ == "__main__":
    unittest.main()
