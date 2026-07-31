from __future__ import annotations


_SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def retry_safety_violations(routes: list[dict[str, object]], *, maximum_retries: int = 3) -> tuple[str, ...]:
    if not isinstance(maximum_retries, int) or isinstance(maximum_retries, bool) or maximum_retries < 0:
        raise ValueError("maximum retries must be a non-negative integer")
    violations: list[str] = []
    seen: set[str] = set()
    for index, route in enumerate(routes):
        name = str(route.get("name", "")).strip()
        if not name:
            violations.append(f"route_{index}:name_is_required")
        elif name in seen:
            violations.append(f"route_{index}:name_must_be_unique")
        seen.add(name)
        methods = route.get("methods")
        if not isinstance(methods, list) or not methods or any(not isinstance(method, str) or not method.strip() for method in methods):
            violations.append(f"route_{index}:methods_must_be_a_non_empty_list")
            normalized: set[str] = set()
        else:
            normalized = {method.upper() for method in methods}
        retries = route.get("retries")
        if not isinstance(retries, int) or isinstance(retries, bool) or retries < 0:
            violations.append(f"route_{index}:retries_must_be_a_non_negative_integer")
            continue
        if retries > maximum_retries:
            violations.append(f"route_{index}:retries_exceed_maximum")
        if retries > 0 and normalized - _SAFE_METHODS and route.get("idempotency_key_required") is not True:
            violations.append(f"route_{index}:unsafe_method_retries_require_idempotency_key")
    return tuple(violations)


def gateway_retry_policy_is_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not retry_safety_violations(routes, **policy)
