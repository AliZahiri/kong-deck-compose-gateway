from __future__ import annotations

REQUIRED_THRESHOLDS = ("http_failures", "tcp_failures", "successes")


def passive_health_violations(config: dict[str, object], *, maximum_threshold: int = 20) -> tuple[str, ...]:
    violations: list[str] = []
    for name in REQUIRED_THRESHOLDS:
        value = config.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= maximum_threshold:
            violations.append(f"{name}_must_be_between_1_and_{maximum_threshold}")
    return tuple(violations)


def passive_health_is_safe(config: dict[str, object], *, maximum_threshold: int = 20) -> bool:
    return not passive_health_violations(config, maximum_threshold=maximum_threshold)
