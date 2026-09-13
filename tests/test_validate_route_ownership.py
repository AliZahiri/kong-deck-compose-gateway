import unittest
from scripts.validate_route_ownership import route_ownership_violations
class RouteOwnershipTests(unittest.TestCase):
    def test_unique_owned_target_routes_pass(self):
        routes=[{'id':'orders','path':'/orders','owner':'commerce','environment':'production'}]
        self.assertEqual((),route_ownership_violations(routes,required_environment='production'))
    def test_duplicate_unowned_and_wrong_target_routes_fail(self):
        routes=[{'id':'x','path':'orders','owner':'','environment':'staging'},{'id':'x','path':'orders','owner':'team','environment':'production'}]
        v=route_ownership_violations(routes,required_environment='production')
        self.assertIn('route_0:path_must_be_absolute_and_unique',v); self.assertIn('route_0:owner_must_be_nonempty',v); self.assertIn('route_1:id_must_be_nonempty_and_unique',v)
    def test_invalid_catalog_fails(self): self.assertEqual(('route_catalog_must_be_a_nonempty_list',),route_ownership_violations([],required_environment='production'))
