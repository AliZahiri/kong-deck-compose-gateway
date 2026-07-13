from __future__ import annotations


def upstream_weight_warnings(targets: list[dict[str, object]]) -> tuple[str, ...]:
    if not targets:
        return ("upstream_targets_are_required",)
    warnings: list[str] = []
    names = [str(target.get("target", "")).strip() for target in targets]
    if any(not name for name in names):
        warnings.append("target_name_is_required")
    if len(set(names)) != len(names):
        warnings.append("target_names_must_be_unique")
    weights = [target.get("weight") for target in targets]
    if any(not isinstance(weight, int) or weight <= 0 for weight in weights):
        warnings.append("target_weights_must_be_positive_integers")
    elif sum(weights) != 100:
        warnings.append("target_weights_must_total_100")
    return tuple(warnings)


def upstream_weights_are_safe(targets: list[dict[str, object]]) -> bool:
    return not upstream_weight_warnings(targets)
