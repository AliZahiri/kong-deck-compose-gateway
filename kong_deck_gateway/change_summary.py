from __future__ import annotations

CHANGE_TYPES = ("routes", "services", "plugins", "upstreams")


def summarize_changes(changes: list[dict[str, str]]) -> dict[str, int]:
    summary = {change_type: 0 for change_type in CHANGE_TYPES}
    for change in changes:
        change_type = change.get("type", "")
        if change_type in summary:
            summary[change_type] += 1
    return summary
