from __future__ import annotations


_REQUIRED_HEADERS = {"x-content-type-options", "x-frame-options"}


def response_security_header_violations(route: dict[str, object]) -> tuple[str, ...]:
    headers = route.get("headers")
    if not isinstance(headers, dict):
        return ("headers_must_be_a_mapping",)
    normalized = {str(name).lower(): value for name, value in headers.items()}
    violations: list[str] = []
    if len(normalized) != len(headers):
        violations.append("header_names_must_be_unique_case_insensitively")
    for header in _REQUIRED_HEADERS:
        if not isinstance(normalized.get(header), str) or not normalized[header].strip():
            violations.append(f"{header}_is_required")
    if route.get("public_https") is True and not isinstance(normalized.get("strict-transport-security"), str):
        violations.append("strict_transport_security_is_required_for_public_https")
    return tuple(violations)


def response_security_headers_are_safe(route: dict[str, object]) -> bool:
    return not response_security_header_violations(route)
