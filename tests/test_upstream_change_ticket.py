import unittest

from kong_deck_gateway.upstream_change_ticket import upstream_change_is_traceable, upstream_change_ticket_violations


class UpstreamChangeTicketTests(unittest.TestCase):
    def test_ticketed_owned_unique_upstreams_pass(self):
        change = {"change_ticket": "CHG-81", "owner": "gateway-team", "affected_upstreams": ["payments", "catalog"], "change_type": "update"}
        self.assertTrue(upstream_change_is_traceable(change))

    def test_missing_duplicate_and_removal_without_rollback_fail(self):
        change = {"change_ticket": "", "owner": " ", "affected_upstreams": ["payments", "Payments", ""], "change_type": "remove"}
        violations = upstream_change_ticket_violations(change)
        self.assertIn("change_ticket_is_required", violations)
        self.assertIn("owner_is_required", violations)
        self.assertIn("affected_upstreams_1_must_be_unique", violations)
        self.assertIn("affected_upstreams_2_is_invalid", violations)
        self.assertIn("rollback_reference_is_required_for_removal", violations)
