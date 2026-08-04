import unittest

from kong_deck_gateway.admin_api_exposure import admin_api_exposure_is_safe, admin_api_exposure_violations


class AdminApiExposureGateTests(unittest.TestCase):
    def test_loopback_and_hardened_control_plane_listener_pass(self):
        listeners = [{"address": "127.0.0.1"}, {"address": "10.20.0.5", "tls_enabled": True, "client_authentication_enabled": True, "rbac_enabled": True, "control_plane_only": True}]
        self.assertTrue(admin_api_exposure_is_safe(listeners))

    def test_duplicate_invalid_and_unprotected_remote_listener_fail(self):
        listeners = [{"address": "10.20.0.5"}, {"address": "10.20.0.5"}, {"address": "not-an-ip"}]
        violations = admin_api_exposure_violations(listeners)
        self.assertIn("listener_0:remote_listener_requires_tls", violations)
        self.assertIn("listener_0:remote_listener_requires_client_authentication", violations)
        self.assertIn("listener_0:remote_listener_requires_rbac", violations)
        self.assertIn("listener_0:remote_listener_must_be_control_plane_only", violations)
        self.assertIn("listener_1:address_must_be_unique", violations)
        self.assertIn("listener_2:address_must_be_an_ip_literal", violations)

    def test_empty_listener_set_fails(self):
        self.assertEqual(("at_least_one_admin_api_listener_is_required",), admin_api_exposure_violations([]))


if __name__ == "__main__":
    unittest.main()
