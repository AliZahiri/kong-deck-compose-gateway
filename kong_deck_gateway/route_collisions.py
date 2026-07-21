from __future__ import annotations


def _methods(route: dict[str, object]) -> set[str] | None:
    methods = route.get("methods")
    if not isinstance(methods, list) or not methods:
        return None
    return {str(method).strip().upper() for method in methods if str(method).strip()}


def route_collisions(routes: list[dict[str, object]]) -> tuple[str, ...]:
    collisions: list[str] = []
    for index, left in enumerate(routes):
        left_name = str(left.get("name", "")).strip() or f"route-{index}"
        left_hosts = {str(host).strip().lower() for host in left.get("hosts", []) if str(host).strip()} if isinstance(left.get("hosts"), list) else set()
        left_paths = {str(path).strip() for path in left.get("paths", []) if str(path).strip()} if isinstance(left.get("paths"), list) else set()
        left_methods = _methods(left)
        for right_index, right in enumerate(routes[index + 1 :], start=index + 1):
            right_name = str(right.get("name", "")).strip() or f"route-{right_index}"
            right_hosts = {str(host).strip().lower() for host in right.get("hosts", []) if str(host).strip()} if isinstance(right.get("hosts"), list) else set()
            right_paths = {str(path).strip() for path in right.get("paths", []) if str(path).strip()} if isinstance(right.get("paths"), list) else set()
            right_methods = _methods(right)
            methods_overlap = left_methods is None or right_methods is None or bool(left_methods & right_methods)
            if left_hosts & right_hosts and left_paths & right_paths and methods_overlap:
                collisions.append(f"{left_name}:{right_name}")
    return tuple(collisions)


def routes_are_unambiguous(routes: list[dict[str, object]]) -> bool:
    return not route_collisions(routes)
