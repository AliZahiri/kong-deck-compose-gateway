import unittest

from kong_deck_gateway.idempotency_replay import idempotency_replay_contract_is_safe, idempotency_replay_violations


class GatewayIdempotencyReplayContractTests(unittest.TestCase):
    def test_mutating_route_with_replay_contract_passes(self):
        routes = [{"name": "create-order", "methods": ["POST"], "idempotency_key_header": "Idempotency-Key", "retention_seconds": 3600, "key_scope": "route-consumer", "request_body_fingerprint": True, "replay_response_enabled": True, "payload_conflict_status": 409}]
        self.assertTrue(idempotency_replay_contract_is_safe(routes))

    def test_missing_replay_safety_controls_fail(self):
        routes = [{"name": "create-order", "methods": ["POST"], "idempotency_key_header": "X-Request-ID", "retention_seconds": 5, "key_scope": "global", "request_body_fingerprint": False, "replay_response_enabled": False, "payload_conflict_status": 400}, {"name": "create-order", "methods": ["GET"]}]
        violations = idempotency_replay_violations(routes)
        self.assertIn("route_0:idempotency_key_header_must_be_standard", violations)
        self.assertIn("route_0:retention_must_be_within_policy", violations)
        self.assertIn("route_0:key_scope_must_be_route_or_consumer_bound", violations)
        self.assertIn("route_0:request_body_fingerprint_is_required", violations)
        self.assertIn("route_0:replay_response_must_be_enabled", violations)
        self.assertIn("route_0:payload_conflict_status_must_be_409", violations)
        self.assertIn("route_1:name_must_be_unique", violations)

    def test_empty_routes_and_invalid_limit_fail(self):
        self.assertEqual(("at_least_one_route_is_required",), idempotency_replay_violations([]))
        with self.assertRaises(ValueError):
            idempotency_replay_violations([], maximum_retention_seconds=59)


if __name__ == "__main__":
    unittest.main()
