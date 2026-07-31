from __future__ import annotations


def upstream_capacity_violations(targets: list[dict[str, object]], *, minimum_healthy_targets: int = 2, minimum_healthy_weight: int = 200, minimum_healthy_zones: int = 2) -> tuple[str, ...]:
    for name, value in (("minimum healthy targets", minimum_healthy_targets), ("minimum healthy weight", minimum_healthy_weight), ("minimum healthy zones", minimum_healthy_zones)):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    if not targets:
        return ("at_least_one_upstream_target_is_required",)
    violations: list[str] = []
    seen_names: set[str] = set()
    healthy_targets = 0
    healthy_weight = 0
    healthy_zones: set[str] = set()
    for index, target in enumerate(targets):
        name = str(target.get("name", "")).strip()
        zone = str(target.get("zone", "")).strip()
        healthy = target.get("healthy")
        weight = target.get("weight")
        if not name:
            violations.append(f"target_{index}:name_is_required")
        elif name in seen_names:
            violations.append(f"target_{index}:name_must_be_unique")
        seen_names.add(name)
        if not zone:
            violations.append(f"target_{index}:zone_is_required")
        if not isinstance(healthy, bool):
            violations.append(f"target_{index}:healthy_must_be_boolean")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight < 0:
            violations.append(f"target_{index}:weight_must_be_a_non_negative_integer")
        if healthy is True and isinstance(weight, int) and not isinstance(weight, bool) and weight >= 0:
            healthy_targets += 1
            healthy_weight += weight
            if zone:
                healthy_zones.add(zone)
    if healthy_targets < minimum_healthy_targets:
        violations.append("healthy_target_count_below_minimum")
    if healthy_weight < minimum_healthy_weight:
        violations.append("healthy_target_weight_below_minimum")
    if len(healthy_zones) < minimum_healthy_zones:
        violations.append("healthy_target_zone_diversity_below_minimum")
    return tuple(violations)


def upstream_has_failover_capacity(targets: list[dict[str, object]], **policy: object) -> bool:
    return not upstream_capacity_violations(targets, **policy)
