from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_GIT_REVISION = re.compile(r"[0-9a-f]{40}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def gateway_promotion_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 86400) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum age must be a positive integer")

    violations: list[str] = []
    desired = evidence.get("desired_state_sha256")
    applied = evidence.get("applied_state_sha256")
    if not isinstance(desired, str) or not _SHA256.fullmatch(desired) or not isinstance(applied, str) or not _SHA256.fullmatch(applied):
        violations.append("state_sha256_values_must_be_valid")
    elif desired != applied:
        violations.append("applied_state_sha256_must_match_reviewed_state")
    revision = evidence.get("source_revision")
    if not isinstance(revision, str) or not _GIT_REVISION.fullmatch(revision):
        violations.append("source_revision_must_be_a_full_git_sha")
    if not isinstance(evidence.get("deck_version"), str) or not evidence["deck_version"].strip():
        violations.append("deck_version_is_required")
    for field in ("diff_reviewed", "sync_succeeded", "post_sync_healthcheck_passed"):
        if evidence.get(field) is not True:
            violations.append(f"{field}_must_be_true")

    started = _timestamp(evidence.get("started_at"))
    completed = _timestamp(evidence.get("completed_at"))
    if started is None:
        violations.append("started_at_must_be_timezone_aware")
    if completed is None:
        violations.append("completed_at_must_be_timezone_aware")
    elif completed > now or (now - completed).total_seconds() > maximum_age_seconds:
        violations.append("promotion_evidence_is_not_fresh")
    if started is not None and completed is not None and completed < started:
        violations.append("completed_at_must_not_precede_started_at")
    return tuple(violations)


def gateway_promotion_evidence_is_complete(evidence: dict[str, object], **policy: object) -> bool:
    return not gateway_promotion_evidence_violations(evidence, **policy)
