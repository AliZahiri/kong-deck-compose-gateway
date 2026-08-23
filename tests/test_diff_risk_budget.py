import unittest

from kong_deck_gateway.diff_risk_budget import diff_is_within_risk_budget, diff_risk_budget_violations


class GatewayDeckDiffRiskBudgetTests(unittest.TestCase):
    def test_small_non_destructive_diff_passes(self):
        self.assertTrue(diff_is_within_risk_budget({"created": 2, "updated": 3, "deleted": 0, "protected_changes": []}, max_total_changes=5))

    def test_large_destructive_unapproved_diff_fails(self):
        violations = diff_risk_budget_violations({"created": 5, "updated": 5, "deleted": 2, "protected_changes": ["jwt"], "protected_change_approved": False}, max_total_changes=10, max_deletions=0)
        self.assertEqual(violations, ("total_changes_exceed_risk_budget", "deletions_exceed_risk_budget", "protected_changes_require_approval"))
