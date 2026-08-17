from __future__ import annotations

from datetime import datetime


def route_change_window_violations(window: dict[str, object], *, max_minutes: int = 120) -> tuple[str, ...]:
    violations: list[str] = []
    values: list[datetime] = []
    for field in ("starts_at", "ends_at"):
        value = window.get(field)
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else None
        except ValueError:
            parsed = None
        if parsed is None or parsed.tzinfo is None or parsed.utcoffset() is None:
            violations.append(f"{field}_must_be_timezone_aware")
        else:
            values.append(parsed)
    if len(values) == 2 and (values[1] <= values[0] or (values[1] - values[0]).total_seconds() > max_minutes * 60):
        violations.append("change_window_must_be_positive_and_bounded")
    if not isinstance(window.get("approval_reference"), str) or not window["approval_reference"].strip():
        violations.append("approval_reference_is_required")
    return tuple(violations)


def route_change_window_is_approved(window: dict[str, object], *, max_minutes: int = 120) -> bool:
    return not route_change_window_violations(window, max_minutes=max_minutes)
