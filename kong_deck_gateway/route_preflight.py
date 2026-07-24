from __future__ import annotations

from kong_deck_gateway.request_size import request_size_violations
from kong_deck_gateway.route_authentication import route_authentication_violations


def route_preflight_violations(routes: list[dict[str, object]], *, platform_max_megabytes: int = 32) -> tuple[str, ...]:
    violations = list(route_authentication_violations(routes))
    for index, route in enumerate(routes):
        name = str(route.get("name", "")).strip() or f"route_{index}"
        violations.extend(f"{name}:{violation}" for violation in request_size_violations(route, platform_max_megabytes=platform_max_megabytes))
    return tuple(violations)


def routes_are_ready_for_sync(routes: list[dict[str, object]], *, platform_max_megabytes: int = 32) -> bool:
    return bool(routes) and not route_preflight_violations(routes, platform_max_megabytes=platform_max_megabytes)
