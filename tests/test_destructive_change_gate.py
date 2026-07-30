import unittest

from kong_deck_gateway.destructive_change_gate import deck_change_plan_is_safe, destructive_change_violations


class DeckDestructiveChangeGateTests(unittest.TestCase):
    def test_reviewed_recoverable_deletion_passes(self):
        changes = [{"entity_type": "route", "entity_name": "legacy-api", "action": "delete"}]
        self.assertTrue(deck_change_plan_is_safe(changes, approved_by="gateway-reviewer", change_ticket="CHG-42", backup_reference="deck-state-20260730"))

    def test_unapproved_deletion_requires_all_recovery_evidence(self):
        violations = destructive_change_violations([{"entity_type": "service", "entity_name": "billing", "action": "delete"}])
        self.assertIn("destructive_change_requires_reviewer", violations)
        self.assertIn("destructive_change_requires_ticket", violations)
        self.assertIn("destructive_change_requires_backup_reference", violations)

    def test_invalid_and_duplicate_records_fail_without_requiring_delete_evidence(self):
        changes = [{"entity_type": "route", "entity_name": "api", "action": "update"}, {"entity_type": "route", "entity_name": "api", "action": "replace"}]
        violations = destructive_change_violations(changes)
        self.assertIn("change_1:action_is_invalid", violations)
        self.assertIn("change_1:duplicate_entity_change", violations)
        self.assertNotIn("destructive_change_requires_reviewer", violations)


if __name__ == "__main__":
    unittest.main()
