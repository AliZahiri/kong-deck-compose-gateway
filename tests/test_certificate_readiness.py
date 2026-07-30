import unittest
from datetime import datetime, timezone

from kong_deck_gateway.certificate_readiness import certificate_is_ready_for_promotion, certificate_readiness_violations


NOW = datetime(2026, 7, 30, tzinfo=timezone.utc)


class GatewayCertificateReadinessGateTests(unittest.TestCase):
    def test_identified_certificate_with_margin_and_host_coverage_passes(self):
        certificate = {"certificate_id": "edge-2026-01", "sha256_fingerprint": "ab:" * 31 + "ab", "expires_at": "2026-12-01T00:00:00Z", "dns_names": ["api.example.com", "admin.example.com"]}
        self.assertTrue(certificate_is_ready_for_promotion(certificate, required_hosts=("api.example.com", "admin.example.com"), now=NOW))

    def test_expiry_fingerprint_and_host_failures_are_reported_together(self):
        certificate = {"certificate_id": "edge", "sha256_fingerprint": "short", "expires_at": "2026-08-01T00:00:00Z", "dns_names": ["api.example.com"]}
        violations = certificate_readiness_violations(certificate, required_hosts=("api.example.com", "admin.example.com"), now=NOW, minimum_validity_days=30)
        self.assertIn("sha256_fingerprint_is_invalid", violations)
        self.assertIn("certificate_validity_margin_is_insufficient", violations)
        self.assertIn("hostname_not_covered:admin.example.com", violations)

    def test_missing_metadata_and_invalid_policy_fail(self):
        violations = certificate_readiness_violations({}, required_hosts=("api.example.com",), now=NOW)
        self.assertIn("certificate_id_is_required", violations)
        self.assertIn("expires_at_must_be_timezone_aware", violations)
        self.assertIn("certificate_dns_names_are_required", violations)
        with self.assertRaises(ValueError):
            certificate_readiness_violations({}, required_hosts=("api.example.com",), now=NOW, minimum_validity_days=-1)


if __name__ == "__main__":
    unittest.main()
