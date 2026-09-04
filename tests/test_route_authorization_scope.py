import unittest

from kong_deck_gateway.route_authorization_scope import route_authorization_scope_violations, route_authorization_scopes_are_safe


class GatewayRouteAuthorizationScopeTests(unittest.TestCase):
    def test_public_and_explicitly_scoped_sensitive_routes_pass(self):
        routes = [{"name": "health", "paths": ["/health"]}, {"name": "admin-users", "paths": ["/admin/users"], "authentication_required": True, "authorization_scopes": ["users:read"]}]
        self.assertTrue(route_authorization_scopes_are_safe(routes, sensitive_prefixes=("/admin",)))

    def test_authentication_only_and_wildcard_authorization_fail(self):
        routes = [{"name": "admin-read", "paths": ["/admin/read"], "authentication_required": True}, {"name": "admin-write", "paths": ["/admin/write"], "authentication_required": True, "authorization_scopes": ["*"]}]
        violations = route_authorization_scope_violations(routes, sensitive_prefixes=("/admin",))
        self.assertIn("route_0:sensitive_route_requires_authorization_scopes", violations)
        self.assertIn("route_1:wildcard_authorization_scope_is_forbidden", violations)

    def test_missing_auth_and_invalid_policy_fail(self):
        routes = [{"name": "billing", "paths": ["/billing"], "authorization_scopes": ["billing:read"]}]
        self.assertIn("route_0:sensitive_route_must_require_authentication", route_authorization_scope_violations(routes, sensitive_prefixes=("/billing",)))
        with self.assertRaises(ValueError):
            route_authorization_scope_violations(routes, sensitive_prefixes=("admin",))
