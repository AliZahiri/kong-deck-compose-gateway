import unittest

from kong_deck_gateway.route_sni_coverage import route_sni_coverage_violations, routes_have_sni_coverage


class GatewayRouteSniCoverageTests(unittest.TestCase):
    def test_exact_and_single_label_wildcard_coverage_passes(self):
        routes = [{"name": "payments", "hosts": ["pay.example.com", "status.internal.example"]}]
        self.assertTrue(routes_have_sni_coverage(routes, ["*.example.com", "status.internal.example"]))

    def test_duplicate_route_and_uncovered_host_fail(self):
        routes = [{"name": "payments", "hosts": ["deep.pay.example.com"]}, {"name": "payments", "hosts": ["api.other.test"]}]
        violations = route_sni_coverage_violations(routes, ["*.example.com"])
        self.assertIn("route_1:name_must_be_unique", violations)
        self.assertTrue(any("has_no_active_sni" in item for item in violations))
