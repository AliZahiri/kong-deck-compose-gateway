from __future__ import annotations


def route_shadowing_violations(routes: list[dict[str, object]]) -> tuple[str, ...]:
    seen: set[tuple[str, str]] = set()
    violations: list[str] = []
    for index, route in enumerate(routes):
        name, path = route.get("name"), route.get("path")
        if not isinstance(name, str) or not name.strip() or not isinstance(path, str) or not path.startswith("/"):
            violations.append(f"route_{index}:name_and_absolute_path_are_required")
            continue
        identity = (name, path)
        if identity in seen:
            violations.append(f"route_{index}:duplicate_route_identity")
        seen.add(identity)
    return tuple(violations)


def routes_are_unambiguous(routes: list[dict[str, object]]) -> bool:
    return not route_shadowing_violations(routes)
