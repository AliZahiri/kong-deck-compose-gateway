from __future__ import annotations


def gateway_request_schema_violations(contract: dict[str, object], *, maximum_body_bytes: int = 10_000_000) -> tuple[str, ...]:
    if not isinstance(maximum_body_bytes, int) or isinstance(maximum_body_bytes, bool) or maximum_body_bytes <= 0:
        raise ValueError("maximum body bytes must be positive")
    violations: list[str] = []
    content_types = contract.get("content_types")
    if not isinstance(content_types, list) or not content_types or not all(isinstance(item, str) and item.strip() for item in content_types):
        violations.append("content_types_must_be_a_non_empty_string_list")
    if contract.get("schema_enforced") is True and content_types != ["application/json"]:
        violations.append("schema_enforcement_requires_json_only")
    limit = contract.get("max_body_bytes")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 0 < limit <= maximum_body_bytes:
        violations.append("max_body_bytes_must_be_bounded")
    fields = contract.get("required_fields")
    if not isinstance(fields, list) or not all(isinstance(field, str) and field.strip() for field in fields) or len(set(fields)) != len(fields):
        violations.append("required_fields_must_be_unique_non_empty_strings")
    return tuple(violations)


def gateway_request_schema_is_safe(contract: dict[str, object], **limits: object) -> bool:
    return not gateway_request_schema_violations(contract, **limits)
