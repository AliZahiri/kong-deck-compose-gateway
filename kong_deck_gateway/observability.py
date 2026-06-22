from __future__ import annotations

REQUIRED_GATEWAY_SIGNALS = (
    "request_count_by_route_status",
    "upstream_latency",
    "gateway_latency",
    "rate_limit_rejections",
    "request_size_rejections",
    "admin_api_change_history",
)


def missing_gateway_signals(signals: list[str] | tuple[str, ...] | set[str]) -> tuple[str, ...]:
    present = set(signals)
    return tuple(signal for signal in REQUIRED_GATEWAY_SIGNALS if signal not in present)


def gateway_observability_is_complete(signals: list[str] | tuple[str, ...] | set[str]) -> bool:
    return not missing_gateway_signals(signals)
