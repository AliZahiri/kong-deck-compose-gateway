import unittest

from kong_deck_gateway.promotion_gate import promotion_gate_violations, promotion_is_safe


class PromotionGateTests(unittest.TestCase):
    def test_reviewed_safe_configuration_passes(self):
        routes = [{"name": "orders", "plugins": ["jwt"], "methods": ["GET"]}]
        self.assertTrue(promotion_is_safe(actions=["update"], routes=routes, timeouts={"connect_ms": 1000, "read_ms": 30000, "write_ms": 30000}, reviewer="platform", environment="staging"))

    def test_diff_route_and_timeout_failures_are_combined(self):
        violations = promotion_gate_violations(actions=["delete"], routes=[{"name": "orders", "plugins": []}], timeouts={}, reviewer=None, environment=None)
        self.assertIn("destructive_change_requires_approval", violations)
        self.assertIn("orders:approved_authentication_plugin_is_required", violations)
        self.assertIn("connect_ms_is_out_of_range", violations)


if __name__ == "__main__":
    unittest.main()
