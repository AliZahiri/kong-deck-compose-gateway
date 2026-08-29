from __future__ import annotations


def failure_domain_violations(targets: list[dict[str, object]], *, minimum_domains: int = 2) -> tuple[str, ...]:
    if not isinstance(minimum_domains, int) or isinstance(minimum_domains, bool) or minimum_domains < 1:
        raise ValueError("minimum_domains must be a positive integer")
    if not isinstance(targets, list) or not targets:
        return ("at_least_one_upstream_target_is_required",)
    violations: list[str] = []
    seen_ids: set[str] = set()
    seen_addresses: set[str] = set()
    healthy_domains: set[str] = set()
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            violations.append(f"target_{index}:must_be_an_object")
            continue
        target_id = target.get("id")
        if not isinstance(target_id, str) or not target_id.strip():
            violations.append(f"target_{index}:id_is_required")
        elif target_id in seen_ids:
            violations.append(f"target_{index}:id_must_be_unique")
        else:
            seen_ids.add(target_id)
        address = target.get("address")
        if not isinstance(address, str) or not address.strip():
            violations.append(f"target_{index}:address_is_required")
        elif address in seen_addresses:
            violations.append(f"target_{index}:address_must_be_unique")
        else:
            seen_addresses.add(address)
        domain = target.get("failure_domain")
        if not isinstance(domain, str) or not domain.strip():
            violations.append(f"target_{index}:failure_domain_is_required")
        weight = target.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight < 1:
            violations.append(f"target_{index}:weight_must_be_positive")
        healthy = target.get("healthy")
        if not isinstance(healthy, bool):
            violations.append(f"target_{index}:healthy_must_be_boolean")
        elif not healthy:
            violations.append(f"target_{index}:target_must_be_healthy")
        elif isinstance(domain, str) and domain.strip():
            healthy_domains.add(domain)
    if len(healthy_domains) < minimum_domains:
        violations.append("healthy_failure_domain_coverage_is_below_minimum")
    return tuple(violations)


def upstream_has_failure_domain_diversity(targets: list[dict[str, object]], **policy: object) -> bool:
    return not failure_domain_violations(targets, **policy)
