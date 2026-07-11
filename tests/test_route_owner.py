import unittest

from kong_deck_gateway.route_owner import route_owner_is_valid, route_owner_warnings


class RouteOwnerTests(unittest.TestCase):
    def test_complete_owner_metadata_is_valid(self):
        metadata = {"route": "api-v1", "owner": "platform", "escalation": "on-call", "tier": "critical"}

        self.assertTrue(route_owner_is_valid(metadata))

    def test_missing_owner_fields_are_reported(self):
        warnings = route_owner_warnings({"route": "api-v1", "tier": "unknown"})

        self.assertIn("owner_is_required", warnings)
        self.assertIn("escalation_is_required", warnings)
        self.assertIn("tier_is_unknown", warnings)


if __name__ == "__main__":
    unittest.main()
