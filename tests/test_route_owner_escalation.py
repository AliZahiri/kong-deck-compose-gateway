import unittest

from kong_deck_gateway.route_owner_escalation import route_has_operational_ownership, route_owner_escalation_violations


class RouteOwnerEscalationTests(unittest.TestCase):
    def test_owned_route_passes(self):
        self.assertTrue(route_has_operational_ownership({"owner": "platform", "escalation_contact": "oncall", "critical": True}))

    def test_missing_and_same_critical_contacts_fail(self):
        violations = route_owner_escalation_violations({"owner": "platform", "escalation_contact": "platform", "critical": True})
        self.assertEqual(violations, ("critical_route_needs_independent_escalation",))
        self.assertIn("owner_is_required", route_owner_escalation_violations({}))


if __name__ == "__main__":
    unittest.main()
