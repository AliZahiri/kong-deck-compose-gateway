import unittest

from kong_deck_gateway.plugin_change_approval import (
    plugin_change_report,
    plugin_change_violations,
    plugin_changes_are_approved,
)


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

    def test_protected_plugin_matching_is_case_insensitive(self):
        changes = [{"plugin": "JWT", "scope": "route", "action": "remove"}]

        violations = plugin_change_violations(changes)

        self.assertIn("protected_plugin_change_requires_reviewer", violations)
        self.assertIn("protected_plugin_change_requires_ticket", violations)

    def test_non_object_change_is_reported_without_crashing(self):
        self.assertEqual(
            ("change_0:record_must_be_an_object",),
            plugin_change_violations(["jwt"]),
        )

    def test_non_string_plugin_name_is_rejected(self):
        violations = plugin_change_violations(
            [{"plugin": None, "scope": "route", "action": "add"}],
        )

        self.assertIn("change_0:plugin_name_is_required", violations)

    def test_report_contains_only_approval_metadata(self):
        report = plugin_change_report(
            [{"plugin": "jwt", "scope": "route", "action": "update"}],
            approved_by="platform-reviewer",
            change_ticket="CHG-2042",
        )

        self.assertTrue(report["approved"])
        self.assertTrue(report["reviewer_recorded"])
        self.assertNotIn("approved_by", report)

    def test_non_string_approval_metadata_cannot_bypass_gate(self):
        violations = plugin_change_violations(
            [{"plugin": "jwt", "scope": "route", "action": "update"}],
            approved_by=42,
            change_ticket=True,
        )

        self.assertIn("protected_plugin_change_requires_reviewer", violations)
        self.assertIn("protected_plugin_change_requires_ticket", violations)


if __name__ == "__main__":
    unittest.main()
