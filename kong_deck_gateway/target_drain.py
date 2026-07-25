from __future__ import annotations


def target_drain_violations(evidence: dict[str, object], *, minimum_checks: int = 3, minimum_drain_seconds: int = 30) -> tuple[str, ...]:
    if not isinstance(minimum_checks, int) or isinstance(minimum_checks, bool) or minimum_checks <= 0:
        raise ValueError("minimum checks must be a positive integer")
    if not isinstance(minimum_drain_seconds, int) or isinstance(minimum_drain_seconds, bool) or minimum_drain_seconds <= 0:
        raise ValueError("minimum drain duration must be a positive integer")
    violations: list[str] = []
    if not str(evidence.get("target", "")).strip():
        violations.append("target_is_required")
    weight = evidence.get("configured_weight")
    if not isinstance(weight, int) or isinstance(weight, bool) or weight != 0:
        violations.append("target_weight_must_be_zero")
    connections = evidence.get("active_connections")
    if not isinstance(connections, int) or isinstance(connections, bool) or connections != 0:
        violations.append("active_connections_must_be_zero")
    checks = evidence.get("consecutive_zero_connection_checks")
    if not isinstance(checks, int) or isinstance(checks, bool) or checks < minimum_checks:
        violations.append("zero_connection_observations_below_minimum")
    duration = evidence.get("drain_seconds")
    if not isinstance(duration, int) or isinstance(duration, bool) or duration < minimum_drain_seconds:
        violations.append("drain_duration_below_minimum")
    if evidence.get("replacement_healthy") is not True:
        violations.append("healthy_replacement_must_be_confirmed")
    return tuple(violations)


def target_is_safe_to_remove(evidence: dict[str, object], *, minimum_checks: int = 3, minimum_drain_seconds: int = 30) -> bool:
    return not target_drain_violations(evidence, minimum_checks=minimum_checks, minimum_drain_seconds=minimum_drain_seconds)
