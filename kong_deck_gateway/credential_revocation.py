from __future__ import annotations

from datetime import datetime


def credential_revocation_violations(evidence: dict[str, object], *, maximum_propagation_seconds: int = 120) -> tuple[str, ...]:
    if not isinstance(maximum_propagation_seconds, int) or isinstance(maximum_propagation_seconds, bool) or maximum_propagation_seconds < 1:
        raise ValueError("maximum_propagation_seconds must be a positive integer")
    violations: list[str] = []
    for field in ("credential_id", "consumer_id", "change_ticket", "audit_event_id"):
        if not isinstance(evidence.get(field), str) or not evidence[field].strip():
            violations.append(f"{field}_is_required")
    revoked_at = _timestamp(evidence.get("revoked_at"))
    rejected_at = _timestamp(evidence.get("gateway_rejected_at"))
    if revoked_at is None:
        violations.append("revoked_at_must_be_timezone_aware")
    if rejected_at is None:
        violations.append("gateway_rejected_at_must_be_timezone_aware")
    elif revoked_at is not None and not 0 <= (rejected_at - revoked_at).total_seconds() <= maximum_propagation_seconds:
        violations.append("revocation_propagation_budget_exceeded")
    if evidence.get("authentication_cache_purged") is not True:
        violations.append("authentication_cache_must_be_purged")
    if evidence.get("revoked_credential_rejected") is not True:
        violations.append("revoked_credential_must_be_rejected")
    return tuple(violations)


def credential_revocation_is_effective(evidence: dict[str, object], **policy: object) -> bool:
    return not credential_revocation_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
