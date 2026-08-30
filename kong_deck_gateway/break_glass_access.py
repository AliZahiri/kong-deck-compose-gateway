from __future__ import annotations

from datetime import datetime


def break_glass_access_violations(grants: list[dict[str, object]], *, now: datetime, maximum_validity_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_validity_seconds, int) or isinstance(maximum_validity_seconds, bool) or maximum_validity_seconds < 1:
        raise ValueError("maximum_validity_seconds must be a positive integer")
    if not isinstance(grants, list) or not grants:
        return ("at_least_one_break_glass_grant_is_required",)
    violations: list[str] = []
    seen_grants: set[str] = set()
    for index, grant in enumerate(grants):
        if not isinstance(grant, dict):
            violations.append(f"grant_{index}:must_be_an_object")
            continue
        grant_id = grant.get("grant_id")
        if not isinstance(grant_id, str) or not grant_id.strip():
            violations.append(f"grant_{index}:grant_id_is_required")
        elif grant_id in seen_grants:
            violations.append(f"grant_{index}:grant_id_must_be_unique")
        else:
            seen_grants.add(grant_id)
        for field in ("operator", "incident_id", "approved_by", "reason"):
            if not isinstance(grant.get(field), str) or not grant[field].strip():
                violations.append(f"grant_{index}:{field}_is_required")
        if grant.get("mfa_verified") is not True:
            violations.append(f"grant_{index}:mfa_must_be_verified")
        if grant.get("audit_sink_enabled") is not True:
            violations.append(f"grant_{index}:audit_sink_must_be_enabled")
        issued_at, expires_at = _timestamp(grant.get("issued_at")), _timestamp(grant.get("expires_at"))
        if issued_at is None or expires_at is None:
            violations.append(f"grant_{index}:grant_times_must_be_timezone_aware")
        else:
            validity = (expires_at - issued_at).total_seconds()
            if validity <= 0 or validity > maximum_validity_seconds:
                violations.append(f"grant_{index}:validity_window_is_outside_policy")
            if issued_at > now or expires_at <= now:
                violations.append(f"grant_{index}:grant_is_not_currently_active")
    return tuple(violations)


def break_glass_access_is_safe(grants: list[dict[str, object]], **policy: object) -> bool:
    return not break_glass_access_violations(grants, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
