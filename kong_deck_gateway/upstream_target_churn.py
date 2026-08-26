from __future__ import annotations

from math import isfinite


def upstream_target_churn_violations(
    before: object,
    after: object,
    *,
    max_churn_percent: float = 50.0,
) -> tuple[str, ...]:
    """Validate and bound target additions, removals, and weight changes."""
    if (
        not isinstance(max_churn_percent, (int, float))
        or isinstance(max_churn_percent, bool)
        or not isfinite(float(max_churn_percent))
        or not 0 <= float(max_churn_percent) <= 100
    ):
        raise ValueError("max_churn_percent must be between 0 and 100")

    violations: list[str] = []
    before_targets = _target_weights(before, "before", violations)
    after_targets = _target_weights(after, "after", violations)
    union = set(before_targets) | set(after_targets)
    changed = {
        target
        for target in union
        if target not in before_targets
        or target not in after_targets
        or before_targets[target] != after_targets[target]
    }
    if union and (len(changed) * 100.0 / len(union)) > float(max_churn_percent):
        violations.append("upstream_target_churn_exceeds_budget")
    return tuple(violations)


def upstream_target_churn_is_safe(before: object, after: object, **policy: object) -> bool:
    return not upstream_target_churn_violations(before, after, **policy)


def _target_weights(targets: object, label: str, violations: list[str]) -> dict[str, int]:
    if not isinstance(targets, list) or not targets:
        violations.append(f"{label}_targets_must_be_a_non_empty_list")
        return {}
    weights: dict[str, int] = {}
    seen: set[str] = set()
    for index, item in enumerate(targets):
        if not isinstance(item, dict):
            violations.append(f"{label}_target_{index}:must_be_an_object")
            continue
        target = item.get("target")
        normalized = target.strip().casefold() if isinstance(target, str) else ""
        if not normalized:
            violations.append(f"{label}_target_{index}:target_is_required")
        elif normalized in seen:
            violations.append(f"{label}_target_{index}:target_must_be_unique")
        else:
            seen.add(normalized)
        weight = item.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or not 1 <= weight <= 65535:
            violations.append(f"{label}_target_{index}:weight_must_be_between_1_and_65535")
        elif normalized and normalized not in weights:
            weights[normalized] = weight
    return weights
