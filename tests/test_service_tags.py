import unittest

from kong_deck_gateway.service_tags import missing_service_tag_prefixes, service_tags_are_complete


class ServiceTagsTests(unittest.TestCase):
    def test_complete_tags_pass(self):
        tags = ["owner:platform", "env:prod", "runbook:https://example.invalid/runbook", "criticality:high"]

        self.assertTrue(service_tags_are_complete(tags))

    def test_missing_runbook_is_reported(self):
        self.assertIn("runbook:", missing_service_tag_prefixes(["owner:platform", "env:prod", "criticality:high"]))


if __name__ == "__main__":
    unittest.main()
