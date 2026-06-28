from __future__ import annotations


def consumer_quota_warnings(policy: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not policy.get("consumer"):
        warnings.append("consumer_missing")
    rpm = policy.get("rpm")
    burst = policy.get("burst")
    alert_threshold_pct = policy.get("alert_threshold_pct", 80)
    if not isinstance(rpm, int) or rpm <= 0:
        warnings.append("rpm_must_be_positive")
    if not isinstance(burst, int) or burst < 0:
        warnings.append("burst_must_be_non_negative")
    if not isinstance(alert_threshold_pct, (int, float)) or not 1 <= alert_threshold_pct <= 100:
        warnings.append("alert_threshold_pct_must_be_1_to_100")
    if isinstance(rpm, int) and isinstance(burst, int) and burst > rpm:
        warnings.append("burst_must_not_exceed_rpm")
    return tuple(warnings)


def consumer_quota_is_safe(policy: dict[str, object]) -> bool:
    return not consumer_quota_warnings(policy)
