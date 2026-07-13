import unittest

from kong_deck_gateway.upstream_weights import upstream_weight_warnings, upstream_weights_are_safe


class UpstreamWeightTests(unittest.TestCase):
    def test_balanced_targets_pass(self):
        self.assertTrue(upstream_weights_are_safe([{"target": "blue:80", "weight": 50}, {"target": "green:80", "weight": 50}]))

    def test_incomplete_distribution_is_reported(self):
        warnings = upstream_weight_warnings([{"target": "blue:80", "weight": 70}, {"target": "green:80", "weight": 20}])

        self.assertIn("target_weights_must_total_100", warnings)


if __name__ == "__main__":
    unittest.main()
