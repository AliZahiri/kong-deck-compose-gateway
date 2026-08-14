import unittest

from kong_deck_gateway.upstream_failover import upstream_failover_is_safe, upstream_failover_violations


class UpstreamFailoverContractTests(unittest.TestCase):
    def test_balanced_failover_targets_pass(self):
        upstream = {"targets": [{"address": "api-a:8080", "weight": 50}, {"address": "api-b:8080", "weight": 50}], "failover_enabled": True, "retries": 2}
        self.assertTrue(upstream_failover_is_safe(upstream))

    def test_duplicate_unbalanced_and_unbounded_targets_fail(self):
        upstream = {"targets": [{"address": "api:8080", "weight": 60}, {"address": "api:8080", "weight": 20}], "failover_enabled": True, "retries": 4}
        violations = upstream_failover_violations(upstream)
        self.assertIn("target_1:address_must_be_unique", violations)
        self.assertIn("target_weights_must_total_100", violations)
        self.assertIn("retries_must_be_between_0_and_3", violations)


if __name__ == "__main__":
    unittest.main()
