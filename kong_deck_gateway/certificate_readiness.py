from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"[a-fA-F0-9]{64}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def certificate_readiness_violations(certificate: dict[str, object], *, required_hosts: tuple[str, ...], now: datetime, minimum_validity_days: int = 30) -> tuple[str, ...]:
    if not isinstance(minimum_validity_days, int) or isinstance(minimum_validity_days, bool) or minimum_validity_days < 0:
        raise ValueError("minimum validity days must be a non-negative integer")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    violations: list[str] = []
    if not str(certificate.get("certificate_id", "")).strip():
        violations.append("certificate_id_is_required")
    fingerprint = certificate.get("sha256_fingerprint")
    if not isinstance(fingerprint, str) or not _SHA256.fullmatch(fingerprint.replace(":", "")):
        violations.append("sha256_fingerprint_is_invalid")
    expires_at = _timestamp(certificate.get("expires_at"))
    if expires_at is None:
        violations.append("expires_at_must_be_timezone_aware")
    elif (expires_at - now).total_seconds() < minimum_validity_days * 86400:
        violations.append("certificate_validity_margin_is_insufficient")
    normalized_required = {str(host).strip().lower() for host in required_hosts if str(host).strip()}
    if len(normalized_required) != len(required_hosts) or not normalized_required:
        violations.append("required_hosts_are_invalid")
    sans = certificate.get("dns_names")
    if not isinstance(sans, (list, tuple)):
        violations.append("certificate_dns_names_are_required")
    else:
        covered = {str(host).strip().lower() for host in sans if str(host).strip()}
        for host in sorted(normalized_required - covered):
            violations.append(f"hostname_not_covered:{host}")
    return tuple(violations)


def certificate_is_ready_for_promotion(certificate: dict[str, object], **policy: object) -> bool:
    return not certificate_readiness_violations(certificate, **policy)
