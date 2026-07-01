import unittest

from kong_deck_gateway.rate_limit_tier import rate_limit_tier_warnings, rate_limit_tiers_are_safe


class RateLimitTierTests(unittest.TestCase):
    def test_ordered_limits_pass(self):
        self.assertTrue(rate_limit_tiers_are_safe({"free": 10, "basic": 60, "pro": 300}))

    def test_unordered_limits_are_reported(self):
        self.assertIn("tier_limits_must_be_ordered", rate_limit_tier_warnings({"free": 100, "basic": 50, "pro": 300}))


if __name__ == "__main__":
    unittest.main()
