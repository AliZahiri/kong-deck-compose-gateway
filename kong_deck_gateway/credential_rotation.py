from __future__ import annotations

from datetime import datetime


_SECRET_FIELDS = {"key", "secret", "token", "value", "credential"}


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def credential_rotation_violations(evidence: dict[str, object], *, maximum_overlap_seconds: int = 86400) -> tuple[str, ...]:
    if not isinstance(maximum_overlap_seconds, int) or isinstance(maximum_overlap_seconds, bool) or maximum_overlap_seconds < 0:
        raise ValueError("maximum overlap must be a non-negative integer")
    violations: list[str] = []
    if any(field in evidence for field in _SECRET_FIELDS):
        violations.append("credential_material_must_not_be_recorded")
    if not isinstance(evidence.get("consumer_id"), str) or not evidence["consumer_id"].strip():
        violations.append("consumer_id_is_required")
    old_id, new_id = evidence.get("old_credential_id"), evidence.get("new_credential_id")
    if not isinstance(old_id, str) or not old_id.strip() or not isinstance(new_id, str) or not new_id.strip():
        violations.append("old_and_new_credential_ids_are_required")
    elif old_id == new_id:
        violations.append("replacement_credential_id_must_be_distinct")
    verified_at = _timestamp(evidence.get("new_credential_verified_at"))
    revoked_at = _timestamp(evidence.get("old_credential_revoked_at"))
    if verified_at is None or revoked_at is None:
        violations.append("rotation_timestamps_must_be_timezone_aware")
    else:
        overlap = (revoked_at - verified_at).total_seconds()
        if overlap < 0:
            violations.append("replacement_must_be_verified_before_revocation")
        elif overlap > maximum_overlap_seconds:
            violations.append("credential_overlap_exceeds_budget")
    if evidence.get("new_credential_verified") is not True:
        violations.append("replacement_credential_must_be_verified")
    if evidence.get("old_credential_revoked") is not True:
        violations.append("previous_credential_must_be_revoked")
    failures = evidence.get("authentication_failures_after_rotation")
    if not isinstance(failures, int) or isinstance(failures, bool) or failures < 0:
        violations.append("authentication_failure_count_must_be_non_negative")
    elif failures > 0:
        violations.append("post_rotation_authentication_failures_detected")
    return tuple(violations)


def credential_rotation_is_complete(evidence: dict[str, object], **policy: object) -> bool:
    return not credential_rotation_violations(evidence, **policy)
