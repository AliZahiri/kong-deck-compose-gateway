import unittest

from kong_deck_gateway.failure_domain import failure_domain_violations, upstream_has_failure_domain_diversity


class UpstreamFailureDomainDiversityTests(unittest.TestCase):
    def test_healthy_targets_across_domains_pass(self):
        targets = [{"id": "a", "address": "10.0.1.10:8080", "failure_domain": "rack-a", "weight": 100, "healthy": True}, {"id": "b", "address": "10.0.2.10:8080", "failure_domain": "rack-b", "weight": 100, "healthy": True}]
        self.assertTrue(upstream_has_failure_domain_diversity(targets))

    def test_duplicate_unhealthy_single_domain_targets_fail(self):
        targets = [{"id": "shared", "address": "10.0.1.10:8080", "failure_domain": "rack-a", "weight": 100, "healthy": True}, {"id": "shared", "address": "10.0.1.10:8080", "failure_domain": "rack-a", "weight": 0, "healthy": False}]
        violations = failure_domain_violations(targets)
        self.assertIn("target_1:id_must_be_unique", violations)
        self.assertIn("target_1:address_must_be_unique", violations)
        self.assertIn("target_1:target_must_be_healthy", violations)
        self.assertIn("healthy_failure_domain_coverage_is_below_minimum", violations)

    def test_invalid_domain_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            failure_domain_violations([], minimum_domains=0)
