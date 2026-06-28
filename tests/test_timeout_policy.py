import unittest

from kong_deck_gateway.timeout_policy import timeout_policy_is_safe, timeout_policy_warnings


class TimeoutPolicyTests(unittest.TestCase):
    def test_safe_timeouts_pass(self):
        self.assertTrue(timeout_policy_is_safe({"connect_timeout": 5000, "read_timeout": 30000, "write_timeout": 30000}))

    def test_excessive_timeout_is_reported(self):
        warnings = timeout_policy_warnings({"connect_timeout": 0, "read_timeout": 120000, "write_timeout": 1000})

        self.assertIn("connect_timeout_must_be_positive", warnings)
        self.assertIn("read_timeout_exceeds_maximum", warnings)


if __name__ == "__main__":
    unittest.main()
