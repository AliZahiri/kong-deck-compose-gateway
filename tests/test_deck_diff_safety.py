import unittest

from kong_deck_gateway.deck_diff_safety import deck_diff_is_safe, deck_diff_warnings


class DeckDiffSafetyTests(unittest.TestCase):
    def test_non_destructive_diff_passes(self):
        self.assertTrue(deck_diff_is_safe(["create", "update"], reviewer="platform", environment="staging"))

    def test_destructive_diff_requires_approval(self):
        warnings = deck_diff_warnings(["delete"], reviewer="platform", environment="prod")

        self.assertIn("destructive_change_requires_approval", warnings)


if __name__ == "__main__":
    unittest.main()
