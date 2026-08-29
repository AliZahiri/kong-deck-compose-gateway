from __future__ import annotations


def keepalive_contract_violations(config: dict[str, object], *, maximum_pool_size: int = 512, maximum_idle_timeout_ms: int = 60000) -> tuple[str, ...]:
    for name, value in (("maximum_pool_size", maximum_pool_size), ("maximum_idle_timeout_ms", maximum_idle_timeout_ms)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    violations: list[str] = []
    if not isinstance(config.get("service"), str) or not config["service"].strip():
        violations.append("service_is_required")
    pool_size = config.get("pool_size")
    if not isinstance(pool_size, int) or isinstance(pool_size, bool) or not 1 <= pool_size <= maximum_pool_size:
        violations.append("pool_size_must_be_within_policy")
    idle_timeout = config.get("idle_timeout_ms")
    if not isinstance(idle_timeout, int) or isinstance(idle_timeout, bool) or not 1 <= idle_timeout <= maximum_idle_timeout_ms:
        violations.append("idle_timeout_ms_must_be_within_policy")
    reuse_limit = config.get("maximum_requests_per_connection")
    if not isinstance(reuse_limit, int) or isinstance(reuse_limit, bool) or reuse_limit < 1:
        violations.append("maximum_requests_per_connection_must_be_positive")
    connect_timeout = config.get("connect_timeout_ms")
    request_timeout = config.get("request_timeout_ms")
    if not isinstance(connect_timeout, int) or isinstance(connect_timeout, bool) or connect_timeout < 1:
        violations.append("connect_timeout_ms_must_be_positive")
    if not isinstance(request_timeout, int) or isinstance(request_timeout, bool) or request_timeout < 1:
        violations.append("request_timeout_ms_must_be_positive")
    elif isinstance(connect_timeout, int) and not isinstance(connect_timeout, bool) and connect_timeout > request_timeout:
        violations.append("connect_timeout_must_not_exceed_request_timeout")
    return tuple(violations)


def keepalive_contract_is_safe(config: dict[str, object], **policy: object) -> bool:
    return not keepalive_contract_violations(config, **policy)
