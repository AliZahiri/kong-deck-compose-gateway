from __future__ import annotations


def upstream_port_policy_violations(upstreams: object, *, allowed_ports: frozenset[int] = frozenset({443, 8443})) -> tuple[str, ...]:
    if not isinstance(allowed_ports, frozenset) or not allowed_ports or any(not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535 for port in allowed_ports): raise ValueError('allowed_ports must be a non-empty frozenset of valid ports')
    if not isinstance(upstreams, list) or not upstreams: return ('upstreams_must_be_a_non_empty_list',)
    violations: list[str] = []; seen: set[tuple[str, int]] = set()
    for position, upstream in enumerate(upstreams):
        prefix = f'upstream_{position}'
        if not isinstance(upstream, dict): violations.append(f'{prefix}:upstream_must_be_an_object'); continue
        name, port = upstream.get('name'), upstream.get('port')
        if not isinstance(name, str) or not name.strip(): violations.append(f'{prefix}:name_is_required')
        if not isinstance(port, int) or isinstance(port, bool) or port not in allowed_ports: violations.append(f'{prefix}:port_is_not_allowed')
        elif isinstance(name, str) and name.strip():
            endpoint = (name, port)
            if endpoint in seen: violations.append(f'{prefix}:endpoint_must_be_unique')
            seen.add(endpoint)
    return tuple(violations)
