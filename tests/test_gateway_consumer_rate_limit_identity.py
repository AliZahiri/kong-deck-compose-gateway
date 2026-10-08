import unittest

from scripts.gateway_consumer_rate_limit_identity import consumer_rate_limit_identity_violations, consumer_rate_limits_are_safe


class GatewayConsumerRateLimitIdentityTests(unittest.TestCase):
    def test_unique_consumer_policy_with_approved_identity_passes(self):
        policies = [{"consumer_id": "consumer-a", "identity_key": "credential", "limit": 120, "window": "minute"}]
        self.assertTrue(consumer_rate_limits_are_safe(policies))

    def test_duplicate_ambiguous_and_unbounded_policy_fails(self):
        policies = [{"consumer_id": "consumer-a", "identity_key": "header", "limit": 0, "window": "forever"}, {"consumer_id": "consumer-a", "identity_key": "ip", "limit": 1, "window": "second"}]
        violations = consumer_rate_limit_identity_violations(policies)
        self.assertIn("policy_0:identity_key_is_not_approved", violations)
        self.assertIn("policy_0:limit_must_be_positive", violations)
        self.assertIn("policy_0:window_must_be_explicit", violations)
        self.assertIn("policy_1:consumer_id_must_be_unique", violations)

    def test_invalid_identity_policy_fails(self):
        with self.assertRaises(ValueError):
            consumer_rate_limit_identity_violations([], approved_identity_keys=frozenset())
