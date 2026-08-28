from __future__ import annotations

from datetime import datetime


_PRIVATE_FIELDS = {"d", "p", "q", "dp", "dq", "qi", "private_key", "secret"}


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def jwks_rotation_violations(keys: list[dict[str, object]], *, now: datetime, allowed_algorithms: set[str], maximum_retiring_seconds: int = 86400) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not allowed_algorithms or any(not isinstance(item, str) or not item.strip() for item in allowed_algorithms):
        raise ValueError("allowed algorithms must be a non-empty string set")
    if not isinstance(maximum_retiring_seconds, int) or isinstance(maximum_retiring_seconds, bool) or maximum_retiring_seconds < 0:
        raise ValueError("maximum retiring window must be non-negative")
    if not isinstance(keys, list) or not keys:
        return ("jwks_keys_are_required",)
    violations: list[str] = []
    seen: set[str] = set()
    active = retiring = 0
    for index, key in enumerate(keys):
        if not isinstance(key, dict):
            violations.append(f"key_{index}:must_be_an_object")
            continue
        if any(field in key for field in _PRIVATE_FIELDS):
            violations.append(f"key_{index}:private_key_material_is_forbidden")
        kid = key.get("kid")
        if not isinstance(kid, str) or not kid.strip():
            violations.append(f"key_{index}:kid_is_required")
        elif kid in seen:
            violations.append(f"key_{index}:kid_must_be_unique")
        else:
            seen.add(kid)
        if key.get("alg") not in allowed_algorithms:
            violations.append(f"key_{index}:algorithm_is_not_allowed")
        status = key.get("status")
        if status == "active":
            active += 1
        elif status == "retiring":
            retiring += 1
        else:
            violations.append(f"key_{index}:status_is_invalid")
        not_before, expires_at = _timestamp(key.get("not_before")), _timestamp(key.get("expires_at"))
        if not_before is None or expires_at is None or not not_before <= now < expires_at:
            violations.append(f"key_{index}:validity_window_does_not_cover_now")
        elif status == "retiring" and (expires_at - now).total_seconds() > maximum_retiring_seconds:
            violations.append(f"key_{index}:retiring_window_exceeds_budget")
    if active < 1:
        violations.append("at_least_one_active_signing_key_is_required")
    if retiring < 1:
        violations.append("at_least_one_retiring_verification_key_is_required")
    return tuple(violations)


def jwks_rotation_is_safe(keys: list[dict[str, object]], **policy: object) -> bool:
    return not jwks_rotation_violations(keys, **policy)
