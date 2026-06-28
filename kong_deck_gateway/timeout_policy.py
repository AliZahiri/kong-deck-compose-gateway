from __future__ import annotations

TIMEOUT_FIELDS = ("connect_timeout", "read_timeout", "write_timeout")


def timeout_policy_warnings(policy: dict[str, object], *, max_timeout_ms: int = 60000) -> tuple[str, ...]:
    warnings: list[str] = []
    for field in TIMEOUT_FIELDS:
        value = policy.get(field)
        if not isinstance(value, int) or value <= 0:
            warnings.append(f"{field}_must_be_positive")
        elif value > max_timeout_ms:
            warnings.append(f"{field}_exceeds_maximum")
    return tuple(warnings)


def timeout_policy_is_safe(policy: dict[str, object], *, max_timeout_ms: int = 60000) -> bool:
    return not timeout_policy_warnings(policy, max_timeout_ms=max_timeout_ms)
