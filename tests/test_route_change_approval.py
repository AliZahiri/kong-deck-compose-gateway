import unittest

from kong_deck_gateway.route_change_approval import route_change_approval_violations, route_change_is_approved


class GatewayRouteChangeApprovalEvidenceGateTests(unittest.TestCase):
    def test_reviewed_route_change_passes(self):
        evidence = {"route_id": "orders-v1", "reviewed_by": "gateway-owner", "change_ticket": "API-41", "methods": ["GET", "POST"], "risk_reviewed": True, "rollback_plan_ready": True}
        self.assertTrue(route_change_is_approved(evidence))

    def test_missing_ticket_method_and_rollback_evidence_fails(self):
        violations = route_change_approval_violations({"route_id": "", "reviewed_by": "", "change_ticket": "41", "methods": ["TRACE"], "risk_reviewed": False, "rollback_plan_ready": False})
        self.assertEqual(violations, ("route_id_is_required", "reviewed_by_is_required", "change_ticket_is_invalid", "methods_contain_an_unsupported_value", "risk_review_must_pass", "rollback_plan_must_be_ready"))
