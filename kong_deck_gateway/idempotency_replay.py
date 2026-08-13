from __future__ import annotations


_UNSAFE_METHODS = {"POST", "PATCH", "PUT", "DELETE"}
_ALLOWED_SCOPES = {"route-consumer", "consumer"}


def idempotency_replay_violations(routes: list[dict[str, object]], *, maximum_retention_seconds: int = 86400) -> tuple[str, ...]:
    if not isinstance(maximum_retention_seconds, int) or isinstance(maximum_retention_seconds, bool) or maximum_retention_seconds < 60:
        raise ValueError("maximum retention must be an integer of at least 60 seconds")
    if not routes:
        return ("at_least_one_route_is_required",)

    violations: list[str] = []
    seen_names: set[str] = set()
    for index, route in enumerate(routes):
        name = route.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"route_{index}:name_is_required")
            name = f"route_{index}"
        elif name in seen_names:
            violations.append(f"route_{index}:name_must_be_unique")
        seen_names.add(name)

        methods = route.get("methods")
        if not isinstance(methods, list) or not methods or not all(isinstance(method, str) and method.strip() for method in methods):
            violations.append(f"route_{index}:methods_must_be_a_non_empty_string_list")
            continue
        if not {method.upper() for method in methods} & _UNSAFE_METHODS:
            continue
        if route.get("idempotency_key_header") != "Idempotency-Key":
            violations.append(f"route_{index}:idempotency_key_header_must_be_standard")
        retention = route.get("retention_seconds")
        if not isinstance(retention, int) or isinstance(retention, bool) or not 60 <= retention <= maximum_retention_seconds:
            violations.append(f"route_{index}:retention_must_be_within_policy")
        if route.get("key_scope") not in _ALLOWED_SCOPES:
            violations.append(f"route_{index}:key_scope_must_be_route_or_consumer_bound")
        if route.get("request_body_fingerprint") is not True:
            violations.append(f"route_{index}:request_body_fingerprint_is_required")
        if route.get("replay_response_enabled") is not True:
            violations.append(f"route_{index}:replay_response_must_be_enabled")
        if route.get("payload_conflict_status") != 409:
            violations.append(f"route_{index}:payload_conflict_status_must_be_409")
    return tuple(violations)


def idempotency_replay_contract_is_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not idempotency_replay_violations(routes, **policy)
