from __future__ import annotations

import re


_ENV_REFERENCE = re.compile(r"\$\{[A-Z][A-Z0-9_]*\}\Z")


def distributed_rate_limit_violations(policies: list[dict[str, object]], *, maximum_redis_timeout_ms: int = 1000) -> tuple[str, ...]:
    if not isinstance(maximum_redis_timeout_ms, int) or isinstance(maximum_redis_timeout_ms, bool) or maximum_redis_timeout_ms < 1:
        raise ValueError("maximum_redis_timeout_ms must be positive")
    if not isinstance(policies, list) or not policies:
        return ("at_least_one_rate_limit_policy_is_required",)

    violations: list[str] = []
    route_ids: set[str] = set()
    namespaces: set[str] = set()
    for index, policy in enumerate(policies):
        prefix = f"policy_{index}"
        if not isinstance(policy, dict):
            violations.append(f"{prefix}:must_be_an_object")
            continue
        route_id = policy.get("route_id")
        if not isinstance(route_id, str) or not route_id.strip() or route_id in route_ids:
            violations.append(f"{prefix}:route_id_must_be_non_empty_and_unique")
        else:
            route_ids.add(route_id)
        if policy.get("strategy") != "redis":
            violations.append(f"{prefix}:strategy_must_be_redis")
        reference = policy.get("redis_host_reference")
        if not isinstance(reference, str) or not _ENV_REFERENCE.fullmatch(reference):
            violations.append(f"{prefix}:redis_host_must_be_an_environment_reference")
        timeout = policy.get("redis_timeout_ms")
        if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= maximum_redis_timeout_ms:
            violations.append(f"{prefix}:redis_timeout_exceeds_policy")
        if policy.get("fault_tolerant") is not False:
            violations.append(f"{prefix}:fault_tolerant_must_be_false_for_fail_closed_limits")
        namespace = policy.get("namespace")
        if not isinstance(namespace, str) or not namespace.strip() or namespace in namespaces:
            violations.append(f"{prefix}:namespace_must_be_non_empty_and_unique")
        else:
            namespaces.add(namespace)
    return tuple(violations)


def distributed_rate_limits_are_consistent(policies: list[dict[str, object]], **policy: object) -> bool:
    return not distributed_rate_limit_violations(policies, **policy)
