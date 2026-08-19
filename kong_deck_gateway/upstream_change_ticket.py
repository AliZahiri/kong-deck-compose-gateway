from __future__ import annotations


def upstream_change_ticket_violations(change: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    for field in ("change_ticket", "owner"):
        value = change.get(field)
        if not isinstance(value, str) or not value.strip():
            violations.append(f"{field}_is_required")
    targets = change.get("affected_upstreams")
    if not isinstance(targets, list) or not targets:
        violations.append("affected_upstreams_must_be_a_non_empty_list")
    else:
        seen: set[str] = set()
        for index, target in enumerate(targets):
            if not isinstance(target, str) or not target.strip():
                violations.append(f"affected_upstreams_{index}_is_invalid")
                continue
            normalized = target.strip().lower()
            if normalized in seen:
                violations.append(f"affected_upstreams_{index}_must_be_unique")
            seen.add(normalized)
    if change.get("change_type") == "remove" and (not isinstance(change.get("rollback_reference"), str) or not change["rollback_reference"].strip()):
        violations.append("rollback_reference_is_required_for_removal")
    return tuple(violations)


def upstream_change_is_traceable(change: dict[str, object]) -> bool:
    return not upstream_change_ticket_violations(change)
