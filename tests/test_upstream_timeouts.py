import unittest

from kong_deck_gateway.upstream_timeouts import upstream_timeout_warnings, upstream_timeouts_are_safe


class UpstreamTimeoutTests(unittest.TestCase):
    def test_bounded_timeouts_pass(self):
        self.assertTrue(upstream_timeouts_are_safe({"connect_ms": 1000, "read_ms": 30000, "write_ms": 30000}))

    def test_missing_timeout_is_reported(self):
        self.assertIn("write_ms_is_out_of_range", upstream_timeout_warnings({"connect_ms": 1000, "read_ms": 30000}))


if __name__ == "__main__":
    unittest.main()
