from __future__ import annotations


def rate_limit_tier_warnings(limits: dict[str, int]) -> tuple[str, ...]:
    warnings: list[str] = []
    for tier in ("free", "basic", "pro"):
        if not isinstance(limits.get(tier), int) or limits[tier] <= 0:
            warnings.append(f"{tier}_limit_must_be_positive")
    if warnings:
        return tuple(warnings)
    if not limits["free"] <= limits["basic"] <= limits["pro"]:
        warnings.append("tier_limits_must_be_ordered")
    return tuple(warnings)


def rate_limit_tiers_are_safe(limits: dict[str, int]) -> bool:
    return not rate_limit_tier_warnings(limits)
