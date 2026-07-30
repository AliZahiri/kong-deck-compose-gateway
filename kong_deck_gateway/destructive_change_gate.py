from __future__ import annotations


_ACTIONS = {"create", "update", "delete"}
_ENTITY_TYPES = {"service", "route", "consumer", "upstream", "plugin"}


def destructive_change_violations(changes: list[dict[str, object]], *, approved_by: str | None = None, change_ticket: str | None = None, backup_reference: str | None = None) -> tuple[str, ...]:
    if not changes:
        return ("at_least_one_deck_change_is_required",)
    violations: list[str] = []
    seen: set[tuple[str, str]] = set()
    has_deletion = False
    for index, change in enumerate(changes):
        entity_type = str(change.get("entity_type", "")).strip().lower()
        entity_name = str(change.get("entity_name", "")).strip()
        action = str(change.get("action", "")).strip().lower()
        if entity_type not in _ENTITY_TYPES:
            violations.append(f"change_{index}:entity_type_is_invalid")
        if not entity_name:
            violations.append(f"change_{index}:entity_name_is_required")
        if action not in _ACTIONS:
            violations.append(f"change_{index}:action_is_invalid")
        key = (entity_type, entity_name)
        if entity_name and key in seen:
            violations.append(f"change_{index}:duplicate_entity_change")
        seen.add(key)
        has_deletion = has_deletion or action == "delete"
    if has_deletion and not str(approved_by or "").strip():
        violations.append("destructive_change_requires_reviewer")
    if has_deletion and not str(change_ticket or "").strip():
        violations.append("destructive_change_requires_ticket")
    if has_deletion and not str(backup_reference or "").strip():
        violations.append("destructive_change_requires_backup_reference")
    return tuple(violations)


def deck_change_plan_is_safe(changes: list[dict[str, object]], **evidence: object) -> bool:
    return not destructive_change_violations(changes, **evidence)
