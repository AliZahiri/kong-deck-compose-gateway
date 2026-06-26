import unittest

from kong_deck_gateway.change_summary import has_unreviewed_change_types, summarize_changes


class ChangeSummaryTests(unittest.TestCase):
    def test_changes_are_grouped_by_type(self):
        summary = summarize_changes([{"type": "routes"}, {"type": "routes"}, {"type": "plugins"}, {"type": "ignored"}])

        self.assertEqual(summary["routes"], 2)
        self.assertEqual(summary["plugins"], 1)
        self.assertEqual(summary["services"], 0)
        self.assertEqual(summary["unknown"], 1)

    def test_unknown_change_types_require_review(self):
        self.assertTrue(has_unreviewed_change_types([{"type": "certificates"}]))
        self.assertFalse(has_unreviewed_change_types([{"type": "routes"}]))


if __name__ == "__main__":
    unittest.main()
