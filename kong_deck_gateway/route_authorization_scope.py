from __future__ import annotations


def route_authorization_scope_violations(routes: list[dict[str, object]], *, sensitive_prefixes: tuple[str, ...]) -> tuple[str, ...]:
    prefixes = tuple(value.rstrip("/") or "/" for value in sensitive_prefixes if isinstance(value, str) and value.startswith("/"))
    if not prefixes or len(prefixes) != len(sensitive_prefixes):
        raise ValueError("sensitive_prefixes must contain absolute paths")
    if not isinstance(routes, list):
        return ("routes_must_be_a_list",)

    violations: list[str] = []
    route_names: set[str] = set()
    for index, route in enumerate(routes):
        prefix = f"route_{index}"
        if not isinstance(route, dict):
            violations.append(f"{prefix}:must_be_an_object")
            continue
        name = route.get("name")
        if not isinstance(name, str) or not name.strip() or name in route_names:
            violations.append(f"{prefix}:name_must_be_non_empty_and_unique")
        else:
            route_names.add(name)
        paths = route.get("paths")
        if not isinstance(paths, list) or not paths or any(not isinstance(path, str) or not path.startswith("/") for path in paths):
            violations.append(f"{prefix}:paths_must_be_non_empty_absolute_paths")
            continue
        if not any(_is_sensitive(path, prefixes) for path in paths):
            continue
        if route.get("authentication_required") is not True:
            violations.append(f"{prefix}:sensitive_route_must_require_authentication")
        scopes = route.get("authorization_scopes")
        if not isinstance(scopes, list) or not scopes or any(not isinstance(scope, str) or not scope.strip() for scope in scopes):
            violations.append(f"{prefix}:sensitive_route_requires_authorization_scopes")
        elif len(scopes) != len(set(scopes)):
            violations.append(f"{prefix}:authorization_scopes_must_be_unique")
        elif any(scope.strip() == "*" for scope in scopes):
            violations.append(f"{prefix}:wildcard_authorization_scope_is_forbidden")
    return tuple(violations)


def route_authorization_scopes_are_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not route_authorization_scope_violations(routes, **policy)


def _is_sensitive(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path == prefix or path.startswith(prefix + "/") for prefix in prefixes)
