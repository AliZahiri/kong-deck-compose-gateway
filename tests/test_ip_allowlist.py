import unittest

from kong_deck_gateway.ip_allowlist import ip_allowlist_is_safe, ip_allowlist_warnings


class IpAllowlistTests(unittest.TestCase):
    def test_private_allowlist_passes(self):
        self.assertTrue(ip_allowlist_is_safe({"cidrs": ["10.0.0.0/24"], "owner": "platform"}))

    def test_public_catch_all_requires_approval(self):
        warnings = ip_allowlist_warnings({"cidrs": ["0.0.0.0/0"]})

        self.assertIn("public_catch_all_requires_approval", warnings)
        self.assertIn("owner_missing", warnings)


if __name__ == "__main__":
    unittest.main()
