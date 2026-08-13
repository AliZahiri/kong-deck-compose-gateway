from __future__ import annotations


def gateway_cache_policy_violations(policy: dict[str, object], *, maximum_ttl_seconds: int = 3600) -> tuple[str, ...]:
    if not isinstance(maximum_ttl_seconds, int) or isinstance(maximum_ttl_seconds, bool) or maximum_ttl_seconds <= 0:
        raise ValueError("maximum TTL must be positive")
    violations: list[str] = []
    methods = policy.get("methods")
    if not isinstance(methods, list) or not methods:
        violations.append("methods_must_be_a_non_empty_list")
    elif policy.get("cache_enabled") is True and not set(methods).issubset({"GET", "HEAD"}):
        violations.append("only_get_and_head_routes_may_be_cached")
    if policy.get("private") is True and policy.get("cache_control") != "no-store":
        violations.append("private_routes_must_use_no_store")
    if policy.get("authenticated") is True and policy.get("shared_cache") is True:
        violations.append("authenticated_routes_must_not_use_shared_cache")
    ttl = policy.get("ttl_seconds")
    if policy.get("cache_enabled") is True and (not isinstance(ttl, int) or isinstance(ttl, bool) or not 0 < ttl <= maximum_ttl_seconds):
        violations.append("cache_ttl_must_be_bounded")
    return tuple(violations)


def gateway_cache_policy_is_safe(policy: dict[str, object], **limits: object) -> bool:
    return not gateway_cache_policy_violations(policy, **limits)
