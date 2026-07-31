import unittest

from kong_deck_gateway.upstream_capacity import upstream_capacity_violations, upstream_has_failover_capacity


class UpstreamFailoverCapacityGateTests(unittest.TestCase):
    def test_healthy_weight_across_two_zones_passes(self):
        targets = [{"name": "api-a", "zone": "az-a", "healthy": True, "weight": 100}, {"name": "api-b", "zone": "az-b", "healthy": True, "weight": 100}]
        self.assertTrue(upstream_has_failover_capacity(targets))

    def test_concentrated_insufficient_capacity_fails(self):
        targets = [{"name": "api-a", "zone": "az-a", "healthy": True, "weight": 50}, {"name": "api-b", "zone": "az-a", "healthy": False, "weight": 100}]
        violations = upstream_capacity_violations(targets)
        self.assertIn("healthy_target_count_below_minimum", violations)
        self.assertIn("healthy_target_weight_below_minimum", violations)
        self.assertIn("healthy_target_zone_diversity_below_minimum", violations)

    def test_duplicate_invalid_target_and_invalid_policy_fail(self):
        violations = upstream_capacity_violations([{"name": "api", "zone": "", "healthy": "yes", "weight": True}, {"name": "api", "zone": "az-b", "healthy": True, "weight": 200}])
        self.assertIn("target_1:name_must_be_unique", violations)
        self.assertIn("target_0:healthy_must_be_boolean", violations)
        with self.assertRaises(ValueError):
            upstream_capacity_violations([], minimum_healthy_zones=0)


if __name__ == "__main__":
    unittest.main()
