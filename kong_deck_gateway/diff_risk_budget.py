from __future__ import annotations


def diff_risk_budget_violations(summary: dict[str, object], *, max_total_changes: int = 20, max_deletions: int = 0) -> tuple[str, ...]:
    for name, value in (("max_total_changes", max_total_changes), ("max_deletions", max_deletions)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    violations: list[str] = []
    counts: dict[str, int] = {}
    for field in ("created", "updated", "deleted"):
        value = summary.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            violations.append(f"{field}_must_be_non_negative")
        else:
            counts[field] = value
    if len(counts) == 3 and sum(counts.values()) > max_total_changes:
        violations.append("total_changes_exceed_risk_budget")
    if counts.get("deleted", 0) > max_deletions:
        violations.append("deletions_exceed_risk_budget")
    protected = summary.get("protected_changes")
    if not isinstance(protected, list) or any(not isinstance(item, str) or not item.strip() for item in protected):
        violations.append("protected_changes_must_be_a_string_list")
    elif protected and summary.get("protected_change_approved") is not True:
        violations.append("protected_changes_require_approval")
    return tuple(violations)


def diff_is_within_risk_budget(summary: dict[str, object], **policy: object) -> bool:
    return not diff_risk_budget_violations(summary, **policy)
