import unittest

from kong_deck_gateway.cache_policy import gateway_cache_policy_is_safe, gateway_cache_policy_violations


class GatewayCachePolicyContractTests(unittest.TestCase):
    def test_bounded_public_get_cache_passes(self):
        policy = {"methods": ["GET"], "cache_enabled": True, "private": False, "authenticated": False, "shared_cache": True, "ttl_seconds": 60}
        self.assertTrue(gateway_cache_policy_is_safe(policy))

    def test_mutating_private_and_authenticated_cache_fails(self):
        policy = {"methods": ["POST"], "cache_enabled": True, "private": True, "cache_control": "public", "authenticated": True, "shared_cache": True, "ttl_seconds": 7200}
        violations = gateway_cache_policy_violations(policy)
        self.assertIn("only_get_and_head_routes_may_be_cached", violations)
        self.assertIn("private_routes_must_use_no_store", violations)
        self.assertIn("authenticated_routes_must_not_use_shared_cache", violations)
        self.assertIn("cache_ttl_must_be_bounded", violations)


if __name__ == "__main__":
    unittest.main()
