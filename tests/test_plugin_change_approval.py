import unittest

from kong_deck_gateway.plugin_change_approval import plugin_change_violations, plugin_changes_are_approved


class ProtectedPluginChangeApprovalTests(unittest.TestCase):
    def test_reviewed_ticketed_protected_update_passes(self):
        changes = [{"plugin": "jwt", "scope": "route", "action": "update"}]
        self.assertTrue(plugin_changes_are_approved(changes, approved_by="platform-reviewer", change_ticket="CHG-2042"))

    def test_unreviewed_protected_removal_requires_reviewer_and_ticket(self):
        changes = [{"plugin": "rate-limiting", "scope": "service", "action": "remove"}]
        violations = plugin_change_violations(changes)
        self.assertIn("protected_plugin_change_requires_reviewer", violations)
        self.assertIn("protected_plugin_change_requires_ticket", violations)

    def test_invalid_and_duplicate_change_records_fail(self):
        changes = [
            {"plugin": "cors", "scope": "route", "action": "update"},
            {"plugin": "cors", "scope": "route", "action": "replace"},
        ]
        violations = plugin_change_violations(changes)
        self.assertIn("change_1:plugin_action_is_invalid", violations)
        self.assertIn("change_1:duplicate_plugin_scope_change", violations)


if __name__ == "__main__":
    unittest.main()
