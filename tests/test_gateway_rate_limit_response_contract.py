import unittest
from scripts.gateway_rate_limit_response_contract import rate_limit_response_is_safe, rate_limit_response_violations

class GatewayRateLimitResponseContractTests(unittest.TestCase):
    def test_explicit_allowlisted_response_passes(self): self.assertTrue(rate_limit_response_is_safe({"status_code": 429, "headers": ["Retry-After", "RateLimit-Remaining"]}))
    def test_wrong_status_and_sensitive_header_fail(self):
        violations = rate_limit_response_violations({"status_code": 500, "headers": ["Authorization"]})
        self.assertIn("status_code_must_be_429", violations); self.assertIn("headers_must_be_unique_allowlisted_values", violations)

if __name__ == "__main__": unittest.main()
