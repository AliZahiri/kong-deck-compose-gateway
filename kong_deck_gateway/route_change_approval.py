from __future__ import annotations

import re


_TICKET = re.compile(r"[A-Z][A-Z0-9]+-\d+\Z")
_ALLOWED_METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"})


def route_change_approval_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    for field in ("route_id", "reviewed_by"):
        if not isinstance(evidence.get(field), str) or not evidence[field].strip():
            violations.append(f"{field}_is_required")
    ticket = evidence.get("change_ticket")
    if not isinstance(ticket, str) or not _TICKET.fullmatch(ticket):
        violations.append("change_ticket_is_invalid")
    methods = evidence.get("methods")
    if not isinstance(methods, list) or not methods:
        violations.append("methods_must_be_a_non_empty_list")
    elif any(not isinstance(method, str) or method not in _ALLOWED_METHODS for method in methods):
        violations.append("methods_contain_an_unsupported_value")
    if evidence.get("risk_reviewed") is not True:
        violations.append("risk_review_must_pass")
    if evidence.get("rollback_plan_ready") is not True:
        violations.append("rollback_plan_must_be_ready")
    return tuple(violations)


def route_change_is_approved(evidence: dict[str, object]) -> bool:
    return not route_change_approval_violations(evidence)
