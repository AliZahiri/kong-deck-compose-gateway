import unittest
from datetime import datetime, timezone

from kong_deck_gateway.jwks_rotation import jwks_rotation_is_safe, jwks_rotation_violations


NOW = datetime(2026, 8, 28, 12, 0, tzinfo=timezone.utc)


class JwtJwksRotationEvidenceTests(unittest.TestCase):
    def test_active_and_bounded_retiring_public_keys_pass(self):
        keys = [{"kid": "new", "alg": "RS256", "status": "active", "not_before": "2026-08-28T11:00:00Z", "expires_at": "2026-09-28T12:00:00Z"}, {"kid": "old", "alg": "RS256", "status": "retiring", "not_before": "2026-07-01T00:00:00Z", "expires_at": "2026-08-28T18:00:00Z"}]
        self.assertTrue(jwks_rotation_is_safe(keys, now=NOW, allowed_algorithms={"RS256"}))

    def test_duplicate_private_and_excessively_retiring_key_fail(self):
        keys = [{"kid": "shared", "alg": "RS256", "status": "active", "not_before": "2026-08-28T11:00:00Z", "expires_at": "2026-09-28T12:00:00Z"}, {"kid": "shared", "alg": "RS256", "status": "retiring", "not_before": "2026-07-01T00:00:00Z", "expires_at": "2026-08-30T12:00:00Z", "private_key": "forbidden"}]
        violations = jwks_rotation_violations(keys, now=NOW, allowed_algorithms={"RS256"}, maximum_retiring_seconds=3600)
        self.assertIn("key_1:kid_must_be_unique", violations)
        self.assertIn("key_1:private_key_material_is_forbidden", violations)
        self.assertIn("key_1:retiring_window_exceeds_budget", violations)

    def test_missing_retiring_key_and_disallowed_algorithm_fail(self):
        keys = [{"kid": "new", "alg": "none", "status": "active", "not_before": "2026-08-28T11:00:00Z", "expires_at": "2026-09-28T12:00:00Z"}]
        violations = jwks_rotation_violations(keys, now=NOW, allowed_algorithms={"RS256"})
        self.assertIn("key_0:algorithm_is_not_allowed", violations)
        self.assertIn("at_least_one_retiring_verification_key_is_required", violations)
