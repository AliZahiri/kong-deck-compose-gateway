from __future__ import annotations


def admin_audit_retention_violations(policy: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    retention = policy.get("retention_days")
    if not isinstance(retention, int) or isinstance(retention, bool) or not 7 <= retention <= 365:
        violations.append("retention_days_must_be_between_7_and_365")
    if policy.get("capture_actor") is not True:
        violations.append("actor_capture_is_required")
    if policy.get("capture_request_id") is not True:
        violations.append("request_id_capture_is_required")
    if policy.get("redact_credentials") is not True:
        violations.append("credential_redaction_is_required")
    sink = policy.get("sink")
    if sink not in {"stdout-json", "http", "syslog"}:
        violations.append("audit_sink_must_be_supported")
    return tuple(violations)


def admin_audit_retention_is_safe(policy: dict[str, object]) -> bool:
    return not admin_audit_retention_violations(policy)
