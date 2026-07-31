import unittest

from kong_deck_gateway.retry_safety import gateway_retry_policy_is_safe, retry_safety_violations


class GatewayRetrySafetyContractTests(unittest.TestCase):
    def test_safe_method_and_idempotency_protected_post_pass(self):
        routes = [{"name": "catalog", "methods": ["GET"], "retries": 2}, {"name": "orders", "methods": ["POST"], "retries": 1, "idempotency_key_required": True}]
        self.assertTrue(gateway_retry_policy_is_safe(routes))

    def test_unsafe_unprotected_and_excessive_retries_fail(self):
        violations = retry_safety_violations([{"name": "orders", "methods": ["POST"], "retries": 4}])
        self.assertIn("route_0:retries_exceed_maximum", violations)
        self.assertIn("route_0:unsafe_method_retries_require_idempotency_key", violations)

    def test_duplicate_invalid_route_and_policy_fail(self):
        violations = retry_safety_violations([{"name": "api", "methods": [], "retries": True}, {"name": "api", "methods": ["GET"], "retries": 0}])
        self.assertIn("route_1:name_must_be_unique", violations)
        self.assertIn("route_0:methods_must_be_a_non_empty_list", violations)
        with self.assertRaises(ValueError):
            retry_safety_violations([], maximum_retries=-1)


if __name__ == "__main__":
    unittest.main()
