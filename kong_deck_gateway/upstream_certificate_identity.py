from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"(?:sha256:)?[0-9a-f]{64}\Z")


def upstream_certificate_identity_violations(evidence: dict[str, object], *, now: datetime, minimum_validity_seconds: int = 604800) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(minimum_validity_seconds, int) or isinstance(minimum_validity_seconds, bool) or minimum_validity_seconds < 1:
        raise ValueError("minimum_validity_seconds must be a positive integer")
    violations: list[str] = []
    sni, sans = evidence.get("sni"), evidence.get("subject_alt_names")
    if not isinstance(sni, str) or not sni.strip():
        violations.append("sni_is_required")
    if not isinstance(sans, list) or any(not isinstance(item, str) or not item.strip() for item in sans):
        violations.append("subject_alt_names_must_be_a_string_list")
    elif sni not in sans:
        violations.append("sni_is_not_covered_by_subject_alt_names")
    fingerprint = evidence.get("certificate_sha256")
    if not isinstance(fingerprint, str) or not _SHA256.fullmatch(fingerprint):
        violations.append("certificate_sha256_is_invalid")
    if evidence.get("trusted_chain") is not True:
        violations.append("certificate_chain_must_be_trusted")
    if evidence.get("revocation_checked") is not True:
        violations.append("certificate_revocation_check_is_required")
    expires_at = _timestamp(evidence.get("expires_at"))
    if expires_at is None:
        violations.append("expires_at_must_be_timezone_aware")
    elif (expires_at - now).total_seconds() < minimum_validity_seconds:
        violations.append("certificate_validity_margin_is_too_small")
    return tuple(violations)


def upstream_certificate_identity_is_ready(evidence: dict[str, object], **policy: object) -> bool:
    return not upstream_certificate_identity_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
