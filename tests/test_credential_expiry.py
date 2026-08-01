import unittest
from datetime import datetime, timezone

from kong_deck_gateway.credential_expiry import consumer_credentials_are_rotation_ready, credential_expiry_violations


NOW = datetime(2026, 8, 1, tzinfo=timezone.utc)


class ConsumerCredentialExpiryGateTests(unittest.TestCase):
    def test_unique_bounded_credential_with_rotation_window_passes(self):
        credentials = [{"credential_id": "orders-jwt-v2", "issued_at": "2026-07-01T00:00:00Z", "expires_at": "2026-09-01T00:00:00Z"}]
        self.assertTrue(consumer_credentials_are_rotation_ready(credentials, now=NOW))

    def test_duplicate_excessive_and_expiring_credentials_fail(self):
        credentials = [{"credential_id": "shared", "issued_at": "2026-01-01T00:00:00Z", "expires_at": "2026-08-02T00:00:00Z"}, {"credential_id": "shared", "issued_at": "bad", "expires_at": "bad"}]
        violations = credential_expiry_violations(credentials, now=NOW)
        self.assertIn("credential_0:lifetime_is_out_of_policy", violations)
        self.assertIn("credential_0:rotation_window_is_too_short", violations)
        self.assertIn("credential_1:identity_must_be_unique", violations)
        self.assertIn("credential_1:timestamps_must_be_timezone_aware", violations)

    def test_naive_now_and_invalid_policy_fail(self):
        with self.assertRaises(ValueError):
            credential_expiry_violations([], now=datetime(2026, 8, 1))
        with self.assertRaises(ValueError):
            credential_expiry_violations([], now=NOW, maximum_lifetime_seconds=0)


if __name__ == "__main__":
    unittest.main()
