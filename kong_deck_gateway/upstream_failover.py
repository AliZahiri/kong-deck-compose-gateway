from __future__ import annotations


def upstream_failover_violations(upstream: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    targets = upstream.get("targets")
    if not isinstance(targets, list) or not targets:
        return ("at_least_one_upstream_target_is_required",)
    seen_addresses: set[str] = set()
    total_weight = 0
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            violations.append(f"target_{index}:must_be_an_object")
            continue
        address = target.get("address")
        if not isinstance(address, str) or not address.strip() or ":" not in address:
            violations.append(f"target_{index}:address_must_include_host_and_port")
        elif address in seen_addresses:
            violations.append(f"target_{index}:address_must_be_unique")
        else:
            seen_addresses.add(address)
        weight = target.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            violations.append(f"target_{index}:weight_must_be_positive")
        else:
            total_weight += weight
    if total_weight != 100:
        violations.append("target_weights_must_total_100")
    if upstream.get("failover_enabled") is True and len(targets) < 2:
        violations.append("failover_requires_at_least_two_targets")
    retries = upstream.get("retries")
    if not isinstance(retries, int) or isinstance(retries, bool) or not 0 <= retries <= 3:
        violations.append("retries_must_be_between_0_and_3")
    return tuple(violations)


def upstream_failover_is_safe(upstream: dict[str, object]) -> bool:
    return not upstream_failover_violations(upstream)
