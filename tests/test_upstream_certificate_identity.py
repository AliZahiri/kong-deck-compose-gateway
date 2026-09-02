import unittest
from datetime import datetime, timezone

from kong_deck_gateway.upstream_certificate_identity import upstream_certificate_identity_is_ready, upstream_certificate_identity_violations


NOW = datetime(2026, 9, 2, 4, 0, tzinfo=timezone.utc)


class UpstreamCertificateIdentityEvidenceTests(unittest.TestCase):
    def test_trusted_matching_certificate_with_margin_passes(self):
        evidence = {"sni": "api.internal.example", "subject_alt_names": ["api.internal.example"], "certificate_sha256": "a" * 64, "trusted_chain": True, "revocation_checked": True, "expires_at": "2026-10-02T04:00:00Z"}
        self.assertTrue(upstream_certificate_identity_is_ready(evidence, now=NOW))

    def test_identity_trust_revocation_and_expiry_failures_are_combined(self):
        evidence = {"sni": "api.internal.example", "subject_alt_names": ["other.internal.example"], "certificate_sha256": "bad", "trusted_chain": False, "revocation_checked": False, "expires_at": "2026-09-03T04:00:00Z"}
        violations = upstream_certificate_identity_violations(evidence, now=NOW)
        self.assertIn("sni_is_not_covered_by_subject_alt_names", violations)
        self.assertIn("certificate_chain_must_be_trusted", violations)
        self.assertIn("certificate_revocation_check_is_required", violations)
        self.assertIn("certificate_validity_margin_is_too_small", violations)
