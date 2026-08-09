from __future__ import annotations

from urllib.parse import urlparse


_ALLOWED_METHODS = {"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"}


def route_cors_policy_violations(routes: list[dict[str, object]], *, maximum_preflight_age_seconds: int = 86400) -> tuple[str, ...]:
    if not isinstance(maximum_preflight_age_seconds, int) or isinstance(maximum_preflight_age_seconds, bool) or maximum_preflight_age_seconds < 0:
        raise ValueError("maximum preflight age must be a non-negative integer")
    if not routes:
        return ("at_least_one_route_cors_policy_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, route in enumerate(routes):
        name = str(route.get("route", "")).strip()
        if not name:
            violations.append(f"route_{position}:name_is_required")
        elif name in seen:
            violations.append(f"route_{position}:name_must_be_unique")
        seen.add(name)
        origins = route.get("origins")
        if not isinstance(origins, list) or not origins or any(not isinstance(value, str) or not value.strip() for value in origins):
            violations.append(f"route_{position}:origins_must_be_non_empty_strings")
            origins = []
        if len(origins) != len(set(origins)):
            violations.append(f"route_{position}:origins_must_be_unique")
        for origin in origins:
            if origin == "*":
                if route.get("allow_credentials") is True:
                    violations.append(f"route_{position}:credentialed_cors_cannot_use_wildcard_origin")
                continue
            parsed = urlparse(origin)
            if parsed.scheme != "https" or not parsed.netloc or parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
                violations.append(f"route_{position}:origin_must_be_an_https_origin")
        methods = route.get("methods")
        if not isinstance(methods, list) or not methods or any(method not in _ALLOWED_METHODS for method in methods):
            violations.append(f"route_{position}:methods_are_invalid")
        elif len(methods) != len(set(methods)):
            violations.append(f"route_{position}:methods_must_be_unique")
        max_age = route.get("preflight_max_age_seconds")
        if not isinstance(max_age, int) or isinstance(max_age, bool) or not 0 <= max_age <= maximum_preflight_age_seconds:
            violations.append(f"route_{position}:preflight_max_age_is_invalid")
    return tuple(violations)


def route_cors_policy_is_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not route_cors_policy_violations(routes, **policy)
