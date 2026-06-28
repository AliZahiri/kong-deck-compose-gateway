from __future__ import annotations

WEAK_ALGORITHMS = {"none", "HS256"}


def jwt_policy_warnings(policy: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    claims = policy.get("required_claims")
    algorithms = set(policy.get("algorithms", [])) if isinstance(policy.get("algorithms"), list) else set()
    if not isinstance(claims, list) or not claims:
        warnings.append("required_claims_missing")
    if not algorithms:
        warnings.append("algorithms_missing")
    if algorithms & WEAK_ALGORITHMS:
        warnings.append("weak_jwt_algorithm_configured")
    if policy.get("anonymous_access") is True:
        warnings.append("anonymous_access_must_be_explicitly_reviewed")
    return tuple(warnings)


def jwt_policy_is_safe(policy: dict[str, object]) -> bool:
    return not jwt_policy_warnings(policy)
