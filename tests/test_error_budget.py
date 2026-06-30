import unittest

from kong_deck_gateway.error_budget import error_budget_is_valid, error_budget_warnings


class ErrorBudgetTests(unittest.TestCase):
    def test_valid_budget_passes(self):
        self.assertTrue(error_budget_is_valid({"route": "api", "max_5xx_rate_pct": 1, "max_upstream_failure_pct": 2, "owner": "sre"}))

    def test_invalid_budget_is_reported(self):
        warnings = error_budget_warnings({"max_5xx_rate_pct": 200})

        self.assertIn("route_missing", warnings)
        self.assertIn("max_5xx_rate_pct_must_be_between_0_and_100", warnings)


if __name__ == "__main__":
    unittest.main()
