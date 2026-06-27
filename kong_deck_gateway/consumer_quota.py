from __future__ import annotations


def consumer_quota_warnings(policy: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not policy.get("consumer"):
        warnings.append("consumer_missing")
    rpm = policy.get("rpm")
    burst = policy.get("burst")
    if not isinstance(rpm, int) or rpm <= 0:
        warnings.append("rpm_must_be_positive")
    if not isinstance(burst, int) or burst < 0:
        warnings.append("burst_must_be_non_negative")
    return tuple(warnings)


def consumer_quota_is_safe(policy: dict[str, object]) -> bool:
    return not consumer_quota_warnings(policy)
