import unittest

from kong_deck_gateway.upstream_transport import upstream_transport_is_safe, upstream_transport_violations


class UpstreamTransportContractTests(unittest.TestCase):
    def test_https_verified_upstream_with_bounded_timeouts_passes(self):
        upstreams = [{"name": "payments", "protocol": "https", "tls_verify": True, "connect_timeout_ms": 500, "read_timeout_ms": 5_000, "write_timeout_ms": 5_000}]
        self.assertTrue(upstream_transport_is_safe(upstreams))

    def test_insecure_transport_and_unbounded_timeout_fail(self):
        upstreams = [{"name": "payments", "protocol": "http", "tls_verify": False, "connect_timeout_ms": 0, "read_timeout_ms": 60_000, "write_timeout_ms": True}]
        violations = upstream_transport_violations(upstreams)
        self.assertIn("upstream_0:protocol_must_be_https", violations)
        self.assertIn("upstream_0:tls_verify_must_be_enabled", violations)
        self.assertIn("upstream_0:connect_timeout_ms_must_be_within_budget", violations)
        self.assertIn("upstream_0:write_timeout_ms_must_be_within_budget", violations)

    def test_duplicate_name_and_invalid_policy_fail(self):
        item = {"name": "catalog", "protocol": "https", "tls_verify": True, "connect_timeout_ms": 100, "read_timeout_ms": 100, "write_timeout_ms": 100}
        self.assertIn("upstream_1:name_must_be_unique", upstream_transport_violations([item, item]))
        with self.assertRaises(ValueError):
            upstream_transport_violations([item], maximum_timeout_ms=0)
