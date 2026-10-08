from __future__ import annotations

_ALLOWED_HEADERS = frozenset({"RateLimit-Limit", "RateLimit-Remaining", "RateLimit-Reset", "Retry-After"})

def rate_limit_response_violations(contract: object) -> tuple[str, ...]:
    if not isinstance(contract, dict): return ("response_contract_must_be_an_object",)
    violations: list[str] = []
    if contract.get("status_code") != 429: violations.append("status_code_must_be_429")
    headers = contract.get("headers")
    if not isinstance(headers, list) or not headers: violations.append("headers_must_be_a_non_empty_list")
    elif any(not isinstance(value, str) or value not in _ALLOWED_HEADERS for value in headers) or len(set(headers)) != len(headers): violations.append("headers_must_be_unique_allowlisted_values")
    return tuple(violations)

def rate_limit_response_is_safe(contract: object) -> bool: return not rate_limit_response_violations(contract)
