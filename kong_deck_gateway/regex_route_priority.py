from __future__ import annotations


def regex_route_priority_violations(routes: list[dict[str, object]], *, maximum_regex_routes: int = 20) -> tuple[str, ...]:
    if not isinstance(maximum_regex_routes, int) or isinstance(maximum_regex_routes, bool) or maximum_regex_routes < 0:
        raise ValueError("maximum regex routes must be a non-negative integer")
    violations: list[str] = []
    priorities: set[int] = set()
    regex_count = 0
    for route_index, route in enumerate(routes):
        paths = route.get("paths")
        regex_paths = []
        if isinstance(paths, list):
            regex_paths = [(path_index, path) for path_index, path in enumerate(paths) if isinstance(path, str) and path.startswith("~")]
        if not regex_paths:
            continue
        regex_count += len(regex_paths)
        for path_index, path in regex_paths:
            pattern = path[1:]
            if not pattern:
                violations.append(f"route_{route_index}:path_{path_index}:regex_pattern_is_required")
            elif not pattern.startswith("/"):
                violations.append(f"route_{route_index}:path_{path_index}:regex_pattern_must_start_with_slash")
        priority = route.get("regex_priority")
        if not isinstance(priority, int) or isinstance(priority, bool) or priority < 0:
            violations.append(f"route_{route_index}:regex_priority_must_be_a_non_negative_integer")
        elif priority in priorities:
            violations.append(f"route_{route_index}:regex_priority_must_be_unique")
        else:
            priorities.add(priority)
    if regex_count > maximum_regex_routes:
        violations.append("regex_route_count_exceeds_maximum")
    return tuple(violations)


def regex_route_priorities_are_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not regex_route_priority_violations(routes, **policy)
