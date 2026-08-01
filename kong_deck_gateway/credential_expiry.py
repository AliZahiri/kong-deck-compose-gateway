from __future__ import annotations

from datetime import datetime


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def credential_expiry_violations(credentials: list[dict[str, object]], *, now: datetime, maximum_lifetime_seconds: int = 7776000, minimum_rotation_window_seconds: int = 604800) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_lifetime_seconds, int) or isinstance(maximum_lifetime_seconds, bool) or maximum_lifetime_seconds <= 0:
        raise ValueError("maximum lifetime must be a positive integer")
    if not isinstance(minimum_rotation_window_seconds, int) or isinstance(minimum_rotation_window_seconds, bool) or minimum_rotation_window_seconds < 0:
        raise ValueError("minimum rotation window must be a non-negative integer")
    violations: list[str] = []
    seen: set[str] = set()
    for position, credential in enumerate(credentials):
        identity = str(credential.get("credential_id", "")).strip()
        if not identity:
            violations.append(f"credential_{position}:identity_is_required")
        elif identity in seen:
            violations.append(f"credential_{position}:identity_must_be_unique")
        seen.add(identity)
        issued = _timestamp(credential.get("issued_at"))
        expires = _timestamp(credential.get("expires_at"))
        if issued is None or expires is None:
            violations.append(f"credential_{position}:timestamps_must_be_timezone_aware")
            continue
        lifetime = (expires - issued).total_seconds()
        if lifetime <= 0 or lifetime > maximum_lifetime_seconds:
            violations.append(f"credential_{position}:lifetime_is_out_of_policy")
        if (expires - now).total_seconds() < minimum_rotation_window_seconds:
            violations.append(f"credential_{position}:rotation_window_is_too_short")
    return tuple(violations)


def consumer_credentials_are_rotation_ready(credentials: list[dict[str, object]], **policy: object) -> bool:
    return not credential_expiry_violations(credentials, **policy)
