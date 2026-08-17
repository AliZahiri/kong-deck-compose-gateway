import unittest

from kong_deck_gateway.route_change_window import route_change_window_is_approved, route_change_window_violations


class GatewayRouteChangeWindowGateTests(unittest.TestCase):
    def test_bounded_approved_window_passes(self):
        self.assertTrue(route_change_window_is_approved({"starts_at": "2026-08-17T02:00:00Z", "ends_at": "2026-08-17T02:30:00Z", "approval_reference": "CHG-42"}))

    def test_naive_unbounded_and_unapproved_window_fails(self):
        violations = route_change_window_violations({"starts_at": "2026-08-17T02:00:00", "ends_at": "2026-08-17T06:30:00Z", "approval_reference": ""})
        self.assertEqual(violations, ("starts_at_must_be_timezone_aware", "approval_reference_is_required"))


if __name__ == "__main__":
    unittest.main()
