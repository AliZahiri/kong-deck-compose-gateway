import unittest

from kong_deck_gateway.client_mtls_contract import client_mtls_contract_is_valid, client_mtls_violations


class GatewayClientMtlsContractTests(unittest.TestCase):
    def test_external_ca_and_restricted_subject_pass(self):
        route = {"route_id": "payments", "mtls_enabled": True, "ca_bundle_ref": "secret://gateway/client-ca", "verify_depth": 2, "revocation_check": True, "allowed_subjects": ["spiffe://platform/payments"]}
        self.assertTrue(client_mtls_contract_is_valid(route))

    def test_inline_or_unverified_mtls_contract_fails(self):
        violations = client_mtls_violations({"route_id": "", "mtls_enabled": False, "ca_bundle_ref": "certificate-data", "verify_depth": 0, "revocation_check": False, "allowed_subjects": []})
        self.assertEqual(len(violations), 6)
