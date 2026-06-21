from __future__ import annotations

PUBLIC_BIND_ADDRESSES = {"0.0.0.0", "::"}


def admin_api_is_private(bind_address: str, *, trusted_networks: list[str] | tuple[str, ...] = ()) -> bool:
    if bind_address in PUBLIC_BIND_ADDRESSES and not trusted_networks:
        return False
    return bind_address in {"127.0.0.1", "localhost"} or bool(trusted_networks)


def admin_api_security_warnings(bind_address: str, *, trusted_networks: list[str] | tuple[str, ...] = ()) -> tuple[str, ...]:
    warnings: list[str] = []
    if bind_address in PUBLIC_BIND_ADDRESSES:
        warnings.append("admin_api_public_bind")
    if not trusted_networks and bind_address not in {"127.0.0.1", "localhost"}:
        warnings.append("trusted_network_missing")
    return tuple(warnings)
