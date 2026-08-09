from __future__ import annotations

from ipaddress import ip_network


def forwarded_header_trust_violations(services: list[dict[str, object]], *, trusted_proxy_cidrs: list[str]) -> tuple[str, ...]:
    if not trusted_proxy_cidrs:
        raise ValueError("at least one trusted proxy CIDR is required")
    normalized: set[str] = set()
    for value in trusted_proxy_cidrs:
        try:
            network = ip_network(value, strict=True)
        except (TypeError, ValueError) as error:
            raise ValueError("trusted proxy CIDRs must be canonical networks") from error
        normalized.add(str(network))
    if len(normalized) != len(trusted_proxy_cidrs):
        raise ValueError("trusted proxy CIDRs must be unique")
    if not services:
        return ("at_least_one_service_header_policy_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, service in enumerate(services):
        name = str(service.get("service", "")).strip()
        if not name:
            violations.append(f"service_{position}:name_is_required")
        elif name in seen:
            violations.append(f"service_{position}:name_must_be_unique")
        seen.add(name)
        for field in ("strip_incoming_forwarded_headers", "replace_x_forwarded_for", "replace_x_forwarded_proto", "generate_request_id"):
            if service.get(field) is not True:
                violations.append(f"service_{position}:{field}_must_be_enabled")
    return tuple(violations)


def forwarded_header_trust_is_safe(services: list[dict[str, object]], **policy: object) -> bool:
    return not forwarded_header_trust_violations(services, **policy)
