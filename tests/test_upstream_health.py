import unittest

from kong_deck_gateway.upstream_health import upstream_health_policy_is_safe, upstream_health_warnings


class UpstreamHealthTests(unittest.TestCase):
    def test_safe_policy_passes(self):
        policy = {"active_path": "/health", "healthy_threshold": 2, "unhealthy_threshold": 2, "passive_checks_enabled": True}

        self.assertTrue(upstream_health_policy_is_safe(policy))

    def test_missing_policy_values_are_reported(self):
        warnings = upstream_health_warnings({})

        self.assertIn("active_path_missing", warnings)
        self.assertIn("passive_checks_must_be_enabled", warnings)


if __name__ == "__main__":
    unittest.main()
