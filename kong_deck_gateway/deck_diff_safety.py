from __future__ import annotations

DESTRUCTIVE_ACTIONS = {"delete", "remove_plugin", "remove_route"}
KNOWN_ACTIONS = {"create", "update", "delete", "remove_plugin", "remove_route"}


def deck_diff_warnings(actions: list[str], *, destructive_approved: bool = False, reviewer: str | None = None, environment: str | None = None) -> tuple[str, ...]:
    warnings: list[str] = []
    unknown = [action for action in actions if action not in KNOWN_ACTIONS]
    if unknown:
        warnings.append("unknown_diff_action")
    if any(action in DESTRUCTIVE_ACTIONS for action in actions) and not destructive_approved:
        warnings.append("destructive_change_requires_approval")
    if not reviewer:
        warnings.append("reviewer_missing")
    if not environment:
        warnings.append("environment_missing")
    return tuple(warnings)


def deck_diff_is_safe(actions: list[str], *, destructive_approved: bool = False, reviewer: str | None = None, environment: str | None = None) -> bool:
    return not deck_diff_warnings(actions, destructive_approved=destructive_approved, reviewer=reviewer, environment=environment)
