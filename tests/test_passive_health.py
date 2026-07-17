import unittest

from kong_deck_gateway.passive_health import passive_health_is_safe, passive_health_violations


class PassiveHealthTests(unittest.TestCase):
    def test_bounded_thresholds_pass(self):
        self.assertTrue(passive_health_is_safe({"http_failures": 5, "tcp_failures": 3, "successes": 2}))

    def test_missing_recovery_threshold_is_reported(self):
        violations = passive_health_violations({"http_failures": 5, "tcp_failures": 3})
        self.assertIn("successes_must_be_between_1_and_20", violations)


if __name__ == "__main__":
    unittest.main()
