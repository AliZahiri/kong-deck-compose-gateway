from __future__ import annotations


def upstream_health_warnings(policy: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not policy.get("active_path"):
        warnings.append("active_path_missing")
    if not isinstance(policy.get("healthy_threshold"), int) or policy.get("healthy_threshold", 0) <= 0:
        warnings.append("healthy_threshold_must_be_positive")
    if not isinstance(policy.get("unhealthy_threshold"), int) or policy.get("unhealthy_threshold", 0) <= 0:
        warnings.append("unhealthy_threshold_must_be_positive")
    if policy.get("passive_checks_enabled") is not True:
        warnings.append("passive_checks_must_be_enabled")
    return tuple(warnings)


def upstream_health_policy_is_safe(policy: dict[str, object]) -> bool:
    return not upstream_health_warnings(policy)
