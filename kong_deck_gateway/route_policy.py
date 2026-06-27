from __future__ import annotations


def route_policy_warnings(route: dict[str, object], *, allow_wildcard: bool = False) -> tuple[str, ...]:
    warnings: list[str] = []
    hosts = route.get("hosts")
    paths = route.get("paths")
    if not isinstance(hosts, list) or not hosts:
        warnings.append("route_hosts_missing")
    elif "*" in hosts and not allow_wildcard:
        warnings.append("wildcard_host_requires_approval")
    if not isinstance(paths, list) or not paths:
        warnings.append("route_paths_missing")
    if "strip_path" not in route:
        warnings.append("strip_path_must_be_explicit")
    return tuple(warnings)


def route_policy_is_safe(route: dict[str, object], *, allow_wildcard: bool = False) -> bool:
    return not route_policy_warnings(route, allow_wildcard=allow_wildcard)
