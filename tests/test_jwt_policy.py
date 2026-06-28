import unittest

from kong_deck_gateway.jwt_policy import jwt_policy_is_safe, jwt_policy_warnings


class JwtPolicyTests(unittest.TestCase):
    def test_safe_jwt_policy_passes(self):
        self.assertTrue(jwt_policy_is_safe({"required_claims": ["sub", "aud"], "algorithms": ["RS256"], "anonymous_access": False}))

    def test_weak_algorithm_is_reported(self):
        warnings = jwt_policy_warnings({"required_claims": ["sub"], "algorithms": ["HS256"]})

        self.assertIn("weak_jwt_algorithm_configured", warnings)


if __name__ == "__main__":
    unittest.main()
