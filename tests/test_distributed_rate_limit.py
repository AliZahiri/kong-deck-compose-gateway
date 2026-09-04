import unittest

from kong_deck_gateway.distributed_rate_limit import distributed_rate_limit_violations, distributed_rate_limits_are_consistent


class DistributedRateLimitConsistencyTests(unittest.TestCase):
    def test_redis_backed_fail_closed_policies_pass(self):
        policies = [{"route_id": "orders", "strategy": "redis", "redis_host_reference": "${REDIS_HOST}", "redis_timeout_ms": 250, "fault_tolerant": False, "namespace": "orders-v1"}]
        self.assertTrue(distributed_rate_limits_are_consistent(policies))

    def test_local_literal_and_fail_open_policy_fails(self):
        policies = [{"route_id": "orders", "strategy": "local", "redis_host_reference": "redis.internal", "redis_timeout_ms": 5000, "fault_tolerant": True, "namespace": "orders-v1"}]
        violations = distributed_rate_limit_violations(policies)
        self.assertIn("policy_0:strategy_must_be_redis", violations)
        self.assertIn("policy_0:redis_host_must_be_an_environment_reference", violations)
        self.assertIn("policy_0:redis_timeout_exceeds_policy", violations)
        self.assertIn("policy_0:fault_tolerant_must_be_false_for_fail_closed_limits", violations)

    def test_duplicate_namespace_and_invalid_policy_fail(self):
        base = {"strategy": "redis", "redis_host_reference": "${REDIS_HOST}", "redis_timeout_ms": 250, "fault_tolerant": False, "namespace": "shared"}
        violations = distributed_rate_limit_violations([{**base, "route_id": "one"}, {**base, "route_id": "two"}])
        self.assertIn("policy_1:namespace_must_be_non_empty_and_unique", violations)
        with self.assertRaises(ValueError):
            distributed_rate_limit_violations([], maximum_redis_timeout_ms=0)
