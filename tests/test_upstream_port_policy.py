import unittest
from kong_deck_gateway.upstream_port_policy import upstream_port_policy_violations
class UpstreamPortPolicyTests(unittest.TestCase):
    def test_standard_tls_endpoint_passes(self): self.assertEqual((), upstream_port_policy_violations([{'name':'catalog','port':443}]))
    def test_non_tls_port_and_duplicate_endpoint_fail(self):
        violations=upstream_port_policy_violations([{'name':'catalog','port':80},{'name':'catalog','port':443},{'name':'catalog','port':443}])
        self.assertIn('upstream_0:port_is_not_allowed', violations); self.assertIn('upstream_2:endpoint_must_be_unique', violations)
    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError): upstream_port_policy_violations([], allowed_ports=frozenset())
