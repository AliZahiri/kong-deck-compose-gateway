from __future__ import annotations


def error_budget_warnings(policy: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not policy.get("route"):
        warnings.append("route_missing")
    for field in ("max_5xx_rate_pct", "max_upstream_failure_pct"):
        value = policy.get(field)
        if not isinstance(value, (int, float)) or not 0 <= value <= 100:
            warnings.append(f"{field}_must_be_between_0_and_100")
    if not policy.get("owner"):
        warnings.append("owner_missing")
    return tuple(warnings)


def error_budget_is_valid(policy: dict[str, object]) -> bool:
    return not error_budget_warnings(policy)
