import unittest
from kong_deck_gateway.service_path import service_path_violations
class ServicePathContractTests(unittest.TestCase):
    def test_canonical_path_passes(self): self.assertEqual((), service_path_violations([{'name':'catalog','path':'/v1/catalog'}]))
    def test_ambiguous_path_and_duplicate_name_fail(self):
        violations = service_path_violations([{'name':'catalog','path':'/v1/../admin'}, {'name':'catalog','path':'/v1'}])
        self.assertIn('service_0:path_must_be_canonical_and_absolute', violations); self.assertIn('service_1:name_must_be_unique', violations)
