from __future__ import annotations


_REQUIRED_HEADERS = frozenset({"authorization", "cookie", "x-api-key"})


def header_redaction_violations(policy: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    headers = policy.get("headers")
    if not isinstance(headers, (list, tuple, set)) or not all(isinstance(header, str) for header in headers):
        violations.append("headers_must_be_string_collection")
    else:
        missing = _REQUIRED_HEADERS.difference(header.strip().lower() for header in headers)
        if missing:
            violations.append("required_sensitive_headers_are_missing")
    if policy.get("case_insensitive") is not True:
        violations.append("case_insensitive_matching_is_required")
    if policy.get("retain_request_id") is not True:
        violations.append("request_id_retention_is_required")
    return tuple(violations)


def header_redaction_is_safe(policy: dict[str, object]) -> bool:
    return not header_redaction_violations(policy)
