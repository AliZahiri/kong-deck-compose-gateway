from __future__ import annotations

import re


_NESTED_UNBOUNDED_QUANTIFIER = re.compile(r"\((?:[^()]|\([^()]*\))*[+*][^()]*\)[+*]")


def regex_route_safety_violations(routes: list[dict[str, object]], *, maximum_pattern_length: int = 256) -> tuple[str, ...]:
    if not isinstance(maximum_pattern_length, int) or isinstance(maximum_pattern_length, bool) or maximum_pattern_length < 1:
        raise ValueError("maximum pattern length must be a positive integer")
    if not isinstance(routes, list):
        return ("routes_must_be_a_list",)

    violations: list[str] = []
    for route_index, route in enumerate(routes):
        paths = route.get("paths") if isinstance(route, dict) else None
        if not isinstance(paths, list):
            violations.append(f"route_{route_index}:paths_must_be_a_list")
            continue
        for path_index, path in enumerate(paths):
            if not isinstance(path, str) or not path.startswith("~"):
                continue
            pattern = path[1:]
            prefix = f"route_{route_index}:path_{path_index}"
            if not pattern:
                violations.append(f"{prefix}:regex_pattern_is_required")
                continue
            if not pattern.startswith("/"):
                violations.append(f"{prefix}:regex_pattern_must_start_with_slash")
            if len(pattern) > maximum_pattern_length:
                violations.append(f"{prefix}:regex_pattern_exceeds_length_budget")
            if _NESTED_UNBOUNDED_QUANTIFIER.search(pattern):
                violations.append(f"{prefix}:potential_nested_quantifier_is_forbidden")
    return tuple(violations)


def regex_routes_are_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not regex_route_safety_violations(routes, **policy)
