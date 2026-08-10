from __future__ import annotations


_PROTECTED_HEADERS = {"x-request-id", "x-forwarded-for", "x-forwarded-proto", "authorization"}


def request_transformer_violations(policy: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    changes = policy.get("header_changes")
    if not isinstance(changes, list):
        return ("header_changes_must_be_a_list",)

    seen: set[str] = set()
    for index, change in enumerate(changes):
        if not isinstance(change, dict):
            violations.append(f"change_{index}:must_be_an_object")
            continue
        name = change.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"change_{index}:name_is_required")
            continue
        normalized = name.lower()
        if normalized in seen:
            violations.append(f"change_{index}:header_name_must_be_unique")
        seen.add(normalized)
        if change.get("operation") not in {"add", "replace", "remove"}:
            violations.append(f"change_{index}:operation_is_invalid")
        if normalized in _PROTECTED_HEADERS and change.get("operation") in {"replace", "remove"}:
            violations.append(f"change_{index}:protected_header_must_not_be_modified")
    if policy.get("preserve_request_id") is not True:
        violations.append("request_id_preservation_is_required")
    return tuple(violations)


def request_transformer_is_safe(policy: dict[str, object]) -> bool:
    return not request_transformer_violations(policy)
