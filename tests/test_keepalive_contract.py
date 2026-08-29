import unittest

from kong_deck_gateway.keepalive_contract import keepalive_contract_is_safe, keepalive_contract_violations


class UpstreamKeepaliveResourceContractTests(unittest.TestCase):
    def test_bounded_keepalive_configuration_passes(self):
        config = {"service": "orders", "pool_size": 128, "idle_timeout_ms": 30000, "maximum_requests_per_connection": 1000, "connect_timeout_ms": 1000, "request_timeout_ms": 5000}
        self.assertTrue(keepalive_contract_is_safe(config))

    def test_oversized_pool_and_inverted_timeouts_fail(self):
        config = {"service": "", "pool_size": 2048, "idle_timeout_ms": 120000, "maximum_requests_per_connection": 0, "connect_timeout_ms": 6000, "request_timeout_ms": 5000}
        violations = keepalive_contract_violations(config)
        self.assertIn("pool_size_must_be_within_policy", violations)
        self.assertIn("idle_timeout_ms_must_be_within_policy", violations)
        self.assertIn("maximum_requests_per_connection_must_be_positive", violations)
        self.assertIn("connect_timeout_must_not_exceed_request_timeout", violations)

    def test_invalid_resource_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            keepalive_contract_violations({}, maximum_pool_size=0)
