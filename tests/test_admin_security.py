import unittest

from kong_deck_gateway.admin_security import (
    admin_api_is_private,
    admin_api_security_warnings,
    normalize_bind_address,
)


class AdminSecurityTests(unittest.TestCase):
    def test_localhost_admin_api_is_private(self):
        self.assertTrue(admin_api_is_private("127.0.0.1"))
        self.assertTrue(admin_api_is_private("[::1]:8001"))

    def test_public_bind_without_trusted_network_warns(self):
        warnings = admin_api_security_warnings("0.0.0.0:8001")

        self.assertIn("admin_api_public_bind", warnings)
        self.assertIn("trusted_network_missing", warnings)
        self.assertFalse(admin_api_is_private("0.0.0.0:8001"))

    def test_public_bind_with_trusted_network_is_explicitly_flagged_but_allowed(self):
        warnings = admin_api_security_warnings("0.0.0.0", trusted_networks=("10.0.0.0/24",))

        self.assertIn("admin_api_public_bind", warnings)
        self.assertTrue(admin_api_is_private("0.0.0.0", trusted_networks=("10.0.0.0/24",)))

    def test_bind_address_normalization_handles_ports(self):
        self.assertEqual(normalize_bind_address("127.0.0.1:8001"), "127.0.0.1")
        self.assertEqual(normalize_bind_address("[::1]:8001"), "::1")


if __name__ == "__main__":
    unittest.main()
