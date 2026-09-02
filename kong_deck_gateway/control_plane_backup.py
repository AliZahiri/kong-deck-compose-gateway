from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"(?:sha256:)?[0-9a-f]{64}\Z")


def control_plane_backup_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 86400, supported_schema_versions: tuple[str, ...] = ("3.0",)) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be a positive integer")
    if not supported_schema_versions or any(not isinstance(item, str) or not item for item in supported_schema_versions):
        raise ValueError("supported_schema_versions must be non-empty strings")
    violations: list[str] = []
    if evidence.get("schema_version") not in supported_schema_versions:
        violations.append("backup_schema_version_is_not_supported")
    digest = evidence.get("state_sha256")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        violations.append("state_sha256_is_invalid")
    if evidence.get("encrypted_at_rest") is not True:
        violations.append("backup_must_be_encrypted_at_rest")
    if evidence.get("restore_parse_verified") is not True:
        violations.append("restore_parse_verification_is_required")
    entity_count = evidence.get("entity_count")
    if not isinstance(entity_count, int) or isinstance(entity_count, bool) or entity_count < 1:
        violations.append("entity_count_must_be_positive")
    created_at = _timestamp(evidence.get("created_at"))
    if created_at is None:
        violations.append("created_at_must_be_timezone_aware")
    elif not 0 <= (now - created_at).total_seconds() <= maximum_age_seconds:
        violations.append("backup_evidence_is_stale_or_future_dated")
    return tuple(violations)


def control_plane_backup_is_ready(evidence: dict[str, object], **policy: object) -> bool:
    return not control_plane_backup_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
