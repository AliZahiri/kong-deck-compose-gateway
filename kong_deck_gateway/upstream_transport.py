from __future__ import annotations


def upstream_transport_violations(
    upstreams: object, *, maximum_timeout_ms: int = 30_000
) -> tuple[str, ...]:
    if not isinstance(maximum_timeout_ms, int) or isinstance(maximum_timeout_ms, bool) or maximum_timeout_ms < 1:
        raise ValueError("maximum_timeout_ms must be a positive integer")
    if not isinstance(upstreams, list) or not upstreams:
        return ("upstreams_must_be_a_non_empty_list",)

    violations: list[str] = []
    seen_names: set[str] = set()
    for position, upstream in enumerate(upstreams):
        prefix = f"upstream_{position}"
        if not isinstance(upstream, dict):
            violations.append(f"{prefix}:upstream_must_be_an_object")
            continue
        name = upstream.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"{prefix}:name_is_required")
        elif name in seen_names:
            violations.append(f"{prefix}:name_must_be_unique")
        else:
            seen_names.add(name)
        if upstream.get("protocol") != "https":
            violations.append(f"{prefix}:protocol_must_be_https")
        if upstream.get("tls_verify") is not True:
            violations.append(f"{prefix}:tls_verify_must_be_enabled")
        for timeout_name in ("connect_timeout_ms", "read_timeout_ms", "write_timeout_ms"):
            timeout = upstream.get(timeout_name)
            if not isinstance(timeout, int) or isinstance(timeout, bool) or not 0 < timeout <= maximum_timeout_ms:
                violations.append(f"{prefix}:{timeout_name}_must_be_within_budget")
    return tuple(violations)


def upstream_transport_is_safe(upstreams: object, **policy: object) -> bool:
    return not upstream_transport_violations(upstreams, **policy)
