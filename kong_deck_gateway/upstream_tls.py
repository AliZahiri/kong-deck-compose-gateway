from __future__ import annotations


def upstream_tls_violations(service: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if str(service.get("protocol", "")).strip().lower() != "https":
        violations.append("upstream_protocol_must_be_https")
    if not str(service.get("host", "")).strip():
        violations.append("upstream_host_is_required")
    if service.get("tls_verify") is not True:
        violations.append("tls_verification_must_be_enabled")
    depth = service.get("tls_verify_depth")
    if not isinstance(depth, int) or isinstance(depth, bool) or not 1 <= depth <= 9:
        violations.append("tls_verify_depth_must_be_between_1_and_9")
    ca_certificates = service.get("ca_certificates")
    if not isinstance(ca_certificates, list) or not any(str(item).strip() for item in ca_certificates):
        violations.append("trusted_ca_reference_is_required")
    return tuple(violations)


def upstream_tls_is_safe(service: dict[str, object]) -> bool:
    return not upstream_tls_violations(service)
