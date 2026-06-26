from __future__ import annotations

CHANGE_TYPES = ("routes", "services", "plugins", "upstreams")


def summarize_changes(changes: list[dict[str, str]]) -> dict[str, int]:
    summary = {change_type: 0 for change_type in CHANGE_TYPES}
    summary["unknown"] = 0
    for change in changes:
        change_type = change.get("type", "")
        if change_type in summary:
            summary[change_type] += 1
        else:
            summary["unknown"] += 1
    return summary


def has_unreviewed_change_types(changes: list[dict[str, str]]) -> bool:
    return summarize_changes(changes)["unknown"] > 0
