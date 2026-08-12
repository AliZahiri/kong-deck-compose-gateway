from __future__ import annotations


_SUPPORTED_PROTOCOLS = {"http", "https", "grpc", "grpcs", "tcp", "tls", "tls_passthrough", "udp"}
_ENCRYPTED_PROTOCOLS = {"https", "grpcs", "tls", "tls_passthrough"}
_INSECURE_PROTOCOLS = {"http", "grpc", "tcp", "udp"}


def route_transport_security_violations(routes: list[dict[str, object]], *, allow_insecure_internal: bool = True) -> tuple[str, ...]:
    if not isinstance(allow_insecure_internal, bool):
        raise ValueError("internal transport policy must be boolean")
    if not routes:
        return ("at_least_one_route_is_required",)

    violations: list[str] = []
    seen_names: set[str] = set()
    for index, route in enumerate(routes):
        name = route.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"route_{index}:name_is_required")
        elif name in seen_names:
            violations.append(f"route_{index}:name_must_be_unique")
        seen_names.add(name)
        exposure = route.get("exposure")
        if exposure not in {"public", "internal"}:
            violations.append(f"route_{index}:exposure_must_be_public_or_internal")
            continue
        protocols = route.get("protocols")
        if not isinstance(protocols, list) or not protocols or not all(isinstance(protocol, str) and protocol in _SUPPORTED_PROTOCOLS for protocol in protocols) or len(set(protocols)) != len(protocols):
            violations.append(f"route_{index}:protocols_must_be_a_unique_supported_list")
            continue
        insecure = set(protocols) & _INSECURE_PROTOCOLS
        encrypted = set(protocols) & _ENCRYPTED_PROTOCOLS
        if exposure == "public" and not encrypted:
            violations.append(f"route_{index}:public_route_requires_encrypted_protocol")
        if exposure == "public" and insecure:
            violations.append(f"route_{index}:public_route_must_not_allow_insecure_protocol")
        if exposure == "internal" and not allow_insecure_internal and insecure:
            violations.append(f"route_{index}:internal_route_must_not_allow_insecure_protocol")
    return tuple(violations)


def route_transport_security_is_safe(routes: list[dict[str, object]], **policy: object) -> bool:
    return not route_transport_security_violations(routes, **policy)
