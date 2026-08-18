from __future__ import annotations


def route_owner_escalation_violations(route: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    for field in ("owner", "escalation_contact"):
        value = route.get(field)
        if not isinstance(value, str) or not value.strip():
            violations.append(f"{field}_is_required")
    if route.get("critical") is True and route.get("escalation_contact") == route.get("owner"):
        violations.append("critical_route_needs_independent_escalation")
    return tuple(violations)


def route_has_operational_ownership(route: dict[str, object]) -> bool:
    return not route_owner_escalation_violations(route)
