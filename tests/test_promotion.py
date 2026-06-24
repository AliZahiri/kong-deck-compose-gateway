import unittest

from kong_deck_gateway.promotion import (
    REQUIRED_PROMOTION_STEPS,
    missing_promotion_steps,
    promotion_order_warnings,
    promotion_plan_is_complete,
)


class PromotionTests(unittest.TestCase):
    def test_complete_promotion_plan_passes(self):
        self.assertTrue(promotion_plan_is_complete(REQUIRED_PROMOTION_STEPS))

    def test_missing_promotion_steps_are_reported(self):
        missing = missing_promotion_steps({"start_inactive_backend"})

        self.assertIn("run_deck_diff", missing)
        self.assertIn("verify_proxy_traffic", missing)

    def test_promotion_order_keeps_diff_and_verification_before_destructive_steps(self):
        steps = list(REQUIRED_PROMOTION_STEPS)
        steps.remove("verify_proxy_traffic")
        steps.append("verify_proxy_traffic")

        warnings = promotion_order_warnings(steps)

        self.assertIn("proxy_verification_must_happen_before_stopping_old_backend", warnings)
        self.assertFalse(promotion_plan_is_complete(steps))


if __name__ == "__main__":
    unittest.main()
