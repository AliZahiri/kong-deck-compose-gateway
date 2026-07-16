from __future__ import annotations

REQUIRED_TIMEOUTS = ("connect_ms", "read_ms", "write_ms")


def upstream_timeout_warnings(timeouts: dict[str, object], *, maximum_ms: int = 120000) -> tuple[str, ...]:
    warnings: list[str] = []
    for name in REQUIRED_TIMEOUTS:
        value = timeouts.get(name)
        if not isinstance(value, int) or not 0 < value <= maximum_ms:
            warnings.append(f"{name}_is_out_of_range")
    return tuple(warnings)


def upstream_timeouts_are_safe(timeouts: dict[str, object], *, maximum_ms: int = 120000) -> bool:
    return not upstream_timeout_warnings(timeouts, maximum_ms=maximum_ms)
