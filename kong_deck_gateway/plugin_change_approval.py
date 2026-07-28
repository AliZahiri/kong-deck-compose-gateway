from __future__ import annotations

from kong_deck_gateway.plugin_drift import PROTECTED_PLUGINS


_ACTIONS = {"add", "update", "remove"}
_SCOPES = {"global", "service", "route", "consumer"}


def plugin_change_violations(changes: list[object], *, approved_by: object = None, change_ticket: object = None) -> tuple[str, ...]:
    if not changes:
        return ("at_least_one_plugin_change_is_required",)
    violations: list[str] = []
    seen: set[tuple[str, str]] = set()
    protected_change = False
    for index, change in enumerate(changes):
        if not isinstance(change, dict):
            violations.append(f"change_{index}:record_must_be_an_object")
            continue
        raw_plugin = change.get("plugin")
        plugin = raw_plugin.strip().lower() if isinstance(raw_plugin, str) else ""
        scope = str(change.get("scope", "")).strip().lower()
        action = str(change.get("action", "")).strip().lower()
        if not plugin:
            violations.append(f"change_{index}:plugin_name_is_required")
        if scope not in _SCOPES:
            violations.append(f"change_{index}:plugin_scope_is_invalid")
        if action not in _ACTIONS:
            violations.append(f"change_{index}:plugin_action_is_invalid")
        key = (plugin, scope)
        if key in seen:
            violations.append(f"change_{index}:duplicate_plugin_scope_change")
        seen.add(key)
        if plugin in PROTECTED_PLUGINS and action in {"update", "remove"}:
            protected_change = True
    if protected_change and (not isinstance(approved_by, str) or not approved_by.strip()):
        violations.append("protected_plugin_change_requires_reviewer")
    if protected_change and (not isinstance(change_ticket, str) or not change_ticket.strip()):
        violations.append("protected_plugin_change_requires_ticket")
    return tuple(violations)


def plugin_changes_are_approved(changes: list[object], *, approved_by: object = None, change_ticket: object = None) -> bool:
    return not plugin_change_violations(changes, approved_by=approved_by, change_ticket=change_ticket)


def plugin_change_report(
    changes: list[object],
    *,
    approved_by: object = None,
    change_ticket: object = None,
) -> dict[str, object]:
    violations = plugin_change_violations(changes, approved_by=approved_by, change_ticket=change_ticket)
    return {
        "approved": not violations,
        "change_count": len(changes),
        "reviewer_recorded": isinstance(approved_by, str) and bool(approved_by.strip()),
        "ticket_recorded": isinstance(change_ticket, str) and bool(change_ticket.strip()),
        "violations": list(violations),
    }
