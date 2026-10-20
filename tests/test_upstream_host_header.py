import unittest
from kong_deck_gateway.upstream_host_header import upstream_host_header_violations
class UpstreamHostHeaderTests(unittest.TestCase):
    def test_explicit_rewritten_dns_host_passes(self): self.assertEqual((), upstream_host_header_violations([{'name':'catalog','preserve_host':False,'upstream_host':'catalog.internal'}]))
    def test_implicit_and_invalid_host_fail(self):
        violations=upstream_host_header_violations([{'name':'catalog','preserve_host':'yes','upstream_host':'bad host'},{'name':'catalog','preserve_host':False,'upstream_host':'localhost'}])
        self.assertIn('service_0:preserve_host_must_be_explicit', violations); self.assertIn('service_1:name_must_be_unique', violations); self.assertIn('service_1:rewritten_upstream_host_must_be_dns_name', violations)
