from __future__ import annotations


_APPROVED_PLUGINS = {"jwt", "key-auth", "openid-connect", "oauth2", "mtls-auth"}


def route_authentication_violations(routes: list[dict[str, object]]) -> tuple[str, ...]:
    violations: list[str] = []
    for index, route in enumerate(routes):
        name = str(route.get("name", "")).strip() or f"route_{index}"
        plugins = {str(plugin).strip().lower() for plugin in route.get("plugins", []) if str(plugin).strip()} if isinstance(route.get("plugins", []), (list, tuple, set)) else set()
        if plugins & _APPROVED_PLUGINS:
            continue
        if route.get("public") is not True:
            violations.append(f"{name}:approved_authentication_plugin_is_required")
            continue
        if not str(route.get("owner", "")).strip():
            violations.append(f"{name}:public_route_owner_is_required")
        if not str(route.get("public_reason", "")).strip():
            violations.append(f"{name}:public_route_reason_is_required")
    return tuple(violations)


def route_authentication_coverage_is_complete(routes: list[dict[str, object]]) -> bool:
    return bool(routes) and not route_authentication_violations(routes)
