from __future__ import annotations


def request_size_limit_plugin(allowed_payload_size_mb: int, *, route_name: str | None = None) -> dict[str, object]:
    if allowed_payload_size_mb <= 0:
        raise ValueError("allowed payload size must be positive")

    plugin: dict[str, object] = {
        "name": "request-size-limiting",
        "config": {"allowed_payload_size": allowed_payload_size_mb},
    }
    if route_name:
        plugin["route"] = {"name": route_name}
    return plugin
