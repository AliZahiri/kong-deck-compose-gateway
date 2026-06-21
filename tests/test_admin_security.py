import unittest

from kong_deck_gateway.admin_security import admin_api_is_private, admin_api_security_warnings


class AdminSecurityTests(unittest.TestCase):
    def test_localhost_admin_api_is_private(self):
        self.assertTrue(admin_api_is_private("127.0.0.1"))

    def test_public_bind_without_trusted_network_warns(self):
        warnings = admin_api_security_warnings("0.0.0.0")

        self.assertIn("admin_api_public_bind", warnings)
        self.assertIn("trusted_network_missing", warnings)
        self.assertFalse(admin_api_is_private("0.0.0.0"))


if __name__ == "__main__":
    unittest.main()
