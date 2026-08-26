import unittest

from kong_deck_gateway.upstream_target_churn import (
    upstream_target_churn_is_safe,
    upstream_target_churn_violations,
)


class UpstreamTargetChurnBudgetTests(unittest.TestCase):
    def test_one_weight_change_within_budget_passes(self):
        before = [{"target": "app-a:8080", "weight": 100}, {"target": "app-b:8080", "weight": 100}]
        after = [{"target": "app-a:8080", "weight": 90}, {"target": "app-b:8080", "weight": 100}]

        self.assertTrue(upstream_target_churn_is_safe(before, after, max_churn_percent=50))

    def test_full_replacement_exceeds_budget(self):
        before = [{"target": "app-a:8080", "weight": 100}, {"target": "app-b:8080", "weight": 100}]
        after = [{"target": "app-c:8080", "weight": 100}, {"target": "app-d:8080", "weight": 100}]

        self.assertIn(
            "upstream_target_churn_exceeds_budget",
            upstream_target_churn_violations(before, after, max_churn_percent=25),
        )

    def test_duplicate_target_and_invalid_weight_fail(self):
        invalid = [{"target": "APP-A:8080", "weight": 0}, {"target": "app-a:8080", "weight": 100}]
        violations = upstream_target_churn_violations(invalid, [{"target": "app-a:8080", "weight": 100}])

        self.assertIn("before_target_0:weight_must_be_between_1_and_65535", violations)
        self.assertIn("before_target_1:target_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()
