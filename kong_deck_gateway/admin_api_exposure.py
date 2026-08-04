from __future__ import annotations

import ipaddress


def admin_api_exposure_violations(listeners: list[dict[str, object]]) -> tuple[str, ...]:
    if not listeners:
        return ("at_least_one_admin_api_listener_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, listener in enumerate(listeners):
        address = str(listener.get("address", "")).strip()
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            violations.append(f"listener_{position}:address_must_be_an_ip_literal")
            ip = None
        if address in seen:
            violations.append(f"listener_{position}:address_must_be_unique")
        seen.add(address)
        if ip is not None and not ip.is_loopback:
            if listener.get("tls_enabled") is not True:
                violations.append(f"listener_{position}:remote_listener_requires_tls")
            if listener.get("client_authentication_enabled") is not True:
                violations.append(f"listener_{position}:remote_listener_requires_client_authentication")
            if listener.get("rbac_enabled") is not True:
                violations.append(f"listener_{position}:remote_listener_requires_rbac")
            if listener.get("control_plane_only") is not True:
                violations.append(f"listener_{position}:remote_listener_must_be_control_plane_only")
    return tuple(violations)


def admin_api_exposure_is_safe(listeners: list[dict[str, object]]) -> bool:
    return not admin_api_exposure_violations(listeners)
