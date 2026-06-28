import unittest

from kong_deck_gateway.consumer_quota import consumer_quota_is_safe, consumer_quota_warnings


class ConsumerQuotaTests(unittest.TestCase):
    def test_valid_quota_passes(self):
        self.assertTrue(consumer_quota_is_safe({"consumer": "mobile", "rpm": 120, "burst": 20, "alert_threshold_pct": 80}))

    def test_invalid_quota_is_reported(self):
        warnings = consumer_quota_warnings({"rpm": 0, "burst": -1})

        self.assertIn("consumer_missing", warnings)
        self.assertIn("rpm_must_be_positive", warnings)

    def test_burst_and_alert_threshold_are_bounded(self):
        warnings = consumer_quota_warnings({"consumer": "mobile", "rpm": 100, "burst": 120, "alert_threshold_pct": 120})

        self.assertIn("burst_must_not_exceed_rpm", warnings)
        self.assertIn("alert_threshold_pct_must_be_1_to_100", warnings)


if __name__ == "__main__":
    unittest.main()
