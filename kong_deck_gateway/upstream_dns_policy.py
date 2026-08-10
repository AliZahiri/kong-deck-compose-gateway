from __future__ import annotations

import ipaddress
import re


_HOSTNAME = re.compile(r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\Z", re.IGNORECASE)


def upstream_dns_policy_violations(policy: dict[str, object], *, maximum_ttl_seconds: int = 3600) -> tuple[str, ...]:
    if not isinstance(maximum_ttl_seconds, int) or isinstance(maximum_ttl_seconds, bool) or maximum_ttl_seconds <= 0:
        raise ValueError("maximum TTL must be a positive integer")
    violations: list[str] = []
    hostname = policy.get("hostname")
    if not isinstance(hostname, str) or not _HOSTNAME.fullmatch(hostname):
        violations.append("hostname_must_be_a_valid_dns_name")
    resolver = policy.get("resolver")
    try:
        parsed = ipaddress.ip_address(resolver)
        if parsed.is_loopback or parsed.is_unspecified:
            violations.append("resolver_must_not_be_loopback_or_unspecified")
    except ValueError:
        violations.append("resolver_must_be_an_ip_address")
    timeout = policy.get("timeout_seconds")
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
        violations.append("timeout_seconds_must_be_positive")
    ttl = policy.get("ttl_seconds")
    if not isinstance(ttl, int) or isinstance(ttl, bool) or not 0 < ttl <= maximum_ttl_seconds:
        violations.append("ttl_seconds_must_be_bounded")
    return tuple(violations)


def upstream_dns_policy_is_safe(policy: dict[str, object], **limits: object) -> bool:
    return not upstream_dns_policy_violations(policy, **limits)
