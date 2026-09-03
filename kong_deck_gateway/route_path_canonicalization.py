from __future__ import annotations


def route_path_canonicalization_violations(routes: list[dict[str, object]], *, allow_trailing_slash: bool = False) -> tuple[str, ...]:
    if not isinstance(allow_trailing_slash, bool):
        raise ValueError("allow trailing slash must be boolean")
    if not isinstance(routes, list):
        return ("routes_must_be_a_list",)

    violations: list[str] = []
    for route_index, route in enumerate(routes):
        paths = route.get("paths") if isinstance(route, dict) else None
        if not isinstance(paths, list) or not paths:
            violations.append(f"route_{route_index}:paths_must_be_a_non_empty_list")
            continue
        for path_index, path in enumerate(paths):
            if isinstance(path, str) and path.startswith("~"):
                continue
            prefix = f"route_{route_index}:path_{path_index}"
            if not isinstance(path, str) or not path.startswith("/"):
                violations.append(f"{prefix}:path_must_be_absolute")
                continue
            lowered = path.lower()
            if "//" in path:
                violations.append(f"{prefix}:duplicate_path_separator_is_forbidden")
            if path in {"/.", "/.."} or "/./" in path or "/../" in path:
                violations.append(f"{prefix}:dot_segments_are_forbidden")
            if "%2f" in lowered or "%5c" in lowered:
                violations.append(f"{prefix}:encoded_path_separator_is_forbidden")
            if not allow_trailing_slash and path != "/" and path.endswith("/"):
                violations.append(f"{prefix}:trailing_slash_requires_explicit_policy")
    return tuple(violations)


def route_paths_are_canonical(routes: list[dict[str, object]], **policy: object) -> bool:
    return not route_path_canonicalization_violations(routes, **policy)
