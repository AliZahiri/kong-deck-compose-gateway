import unittest
from datetime import datetime, timezone

from kong_deck_gateway.break_glass_access import break_glass_access_is_safe, break_glass_access_violations


NOW = datetime(2026, 8, 30, 8, 0, tzinfo=timezone.utc)


class GatewayBreakGlassAccessEvidenceTests(unittest.TestCase):
    def test_approved_audited_bounded_grant_passes(self):
        grant = {"grant_id": "grant-42", "operator": "on-call", "incident_id": "INC-42", "approved_by": "platform-lead", "reason": "restore gateway routes", "mfa_verified": True, "audit_sink_enabled": True, "issued_at": "2026-08-30T07:45:00Z", "expires_at": "2026-08-30T08:30:00Z"}
        self.assertTrue(break_glass_access_is_safe([grant], now=NOW))

    def test_unapproved_unaudited_long_grant_fails(self):
        grant = {"grant_id": "grant-42", "operator": "", "incident_id": "", "approved_by": "", "reason": "", "mfa_verified": False, "audit_sink_enabled": False, "issued_at": "2026-08-30T06:00:00Z", "expires_at": "2026-08-30T12:00:00Z"}
        violations = break_glass_access_violations([grant], now=NOW)
        self.assertIn("grant_0:operator_is_required", violations)
        self.assertIn("grant_0:mfa_must_be_verified", violations)
        self.assertIn("grant_0:audit_sink_must_be_enabled", violations)
        self.assertIn("grant_0:validity_window_is_outside_policy", violations)

    def test_empty_grants_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_break_glass_grant_is_required",), break_glass_access_violations([], now=NOW))
        with self.assertRaises(ValueError):
            break_glass_access_violations([], now=NOW, maximum_validity_seconds=0)
