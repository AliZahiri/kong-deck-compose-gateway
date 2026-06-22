import unittest

from kong_deck_gateway.observability import REQUIRED_GATEWAY_SIGNALS, gateway_observability_is_complete, missing_gateway_signals


class GatewayObservabilityTests(unittest.TestCase):
    def test_complete_signal_set_passes(self):
        self.assertTrue(gateway_observability_is_complete(REQUIRED_GATEWAY_SIGNALS))

    def test_missing_signals_are_reported(self):
        missing = missing_gateway_signals({"upstream_latency"})

        self.assertIn("request_count_by_route_status", missing)
        self.assertIn("admin_api_change_history", missing)


if __name__ == "__main__":
    unittest.main()
