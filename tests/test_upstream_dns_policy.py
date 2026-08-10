import unittest

from kong_deck_gateway.upstream_dns_policy import upstream_dns_policy_is_safe, upstream_dns_policy_violations


class UpstreamDnsPolicyGateTests(unittest.TestCase):
    def test_bounded_non_loopback_dns_policy_passes(self):
        policy = {"hostname": "api.internal.example", "resolver": "10.0.0.53", "timeout_seconds": 2, "ttl_seconds": 60}

        self.assertTrue(upstream_dns_policy_is_safe(policy))

    def test_invalid_hostname_resolver_and_timing_policy_fail(self):
        policy = {"hostname": "localhost", "resolver": "127.0.0.1", "timeout_seconds": 0, "ttl_seconds": 7200}

        violations = upstream_dns_policy_violations(policy)

        self.assertIn("hostname_must_be_a_valid_dns_name", violations)
        self.assertIn("resolver_must_not_be_loopback_or_unspecified", violations)
        self.assertIn("timeout_seconds_must_be_positive", violations)
        self.assertIn("ttl_seconds_must_be_bounded", violations)

    def test_invalid_limit_fails(self):
        with self.assertRaises(ValueError):
            upstream_dns_policy_violations({}, maximum_ttl_seconds=0)


if __name__ == "__main__":
    unittest.main()
