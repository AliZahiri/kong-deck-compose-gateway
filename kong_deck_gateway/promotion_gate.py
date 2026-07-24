from __future__ import annotations

from kong_deck_gateway.deck_diff_safety import deck_diff_warnings
from kong_deck_gateway.route_preflight import route_preflight_violations
from kong_deck_gateway.upstream_timeouts import upstream_timeout_warnings


def promotion_gate_violations(*, actions: list[str], routes: list[dict[str, object]], timeouts: dict[str, object], destructive_approved: bool = False, reviewer: str | None = None, environment: str | None = None) -> tuple[str, ...]:
    violations = list(deck_diff_warnings(actions, destructive_approved=destructive_approved, reviewer=reviewer, environment=environment))
    violations.extend(route_preflight_violations(routes))
    violations.extend(upstream_timeout_warnings(timeouts))
    return tuple(violations)


def promotion_is_safe(**inputs: object) -> bool:
    return not promotion_gate_violations(**inputs)
