import unittest

from kong_deck_gateway.change_summary import summarize_changes


class ChangeSummaryTests(unittest.TestCase):
    def test_changes_are_grouped_by_type(self):
        summary = summarize_changes([{"type": "routes"}, {"type": "routes"}, {"type": "plugins"}, {"type": "ignored"}])

        self.assertEqual(summary["routes"], 2)
        self.assertEqual(summary["plugins"], 1)
        self.assertEqual(summary["services"], 0)


if __name__ == "__main__":
    unittest.main()
