from __future__ import annotations

from ipaddress import ip_address

PUBLIC_BIND_ADDRESSES = {"0.0.0.0", "::"}
LOCAL_BIND_NAMES = {"localhost"}


def normalize_bind_address(bind_address: str) -> str:
    value = bind_address.strip().lower()
    if value.startswith("[") and "]" in value:
        return value[1 : value.index("]")]
    if value.count(":") == 1:
        return value.split(":", 1)[0]
    return value


def _has_trusted_networks(trusted_networks: list[str] | tuple[str, ...]) -> bool:
    return any(network.strip() for network in trusted_networks)


def _is_loopback(bind_address: str) -> bool:
    if bind_address in LOCAL_BIND_NAMES:
        return True
    try:
        return ip_address(bind_address).is_loopback
    except ValueError:
        return False


def admin_api_is_private(bind_address: str, *, trusted_networks: list[str] | tuple[str, ...] = ()) -> bool:
    normalized = normalize_bind_address(bind_address)
    if normalized in PUBLIC_BIND_ADDRESSES and not _has_trusted_networks(trusted_networks):
        return False
    return _is_loopback(normalized) or _has_trusted_networks(trusted_networks)


def admin_api_security_warnings(bind_address: str, *, trusted_networks: list[str] | tuple[str, ...] = ()) -> tuple[str, ...]:
    warnings: list[str] = []
    normalized = normalize_bind_address(bind_address)
    has_trusted_networks = _has_trusted_networks(trusted_networks)
    if normalized in PUBLIC_BIND_ADDRESSES:
        warnings.append("admin_api_public_bind")
    if not has_trusted_networks and not _is_loopback(normalized):
        warnings.append("trusted_network_missing")
    return tuple(warnings)
