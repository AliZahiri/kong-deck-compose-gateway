from __future__ import annotations


def consumer_rate_limit_identity_violations(policies: object, *, approved_identity_keys: frozenset[str] = frozenset({"consumer", "credential", "ip"})) -> tuple[str, ...]:
    if not isinstance(approved_identity_keys, frozenset) or not approved_identity_keys or any(not isinstance(value, str) or not value for value in approved_identity_keys):
        raise ValueError("approved_identity_keys must be a non-empty frozenset of strings")
    if not isinstance(policies, list) or not policies:
        return ("at_least_one_consumer_rate_limit_policy_is_required",)
    violations: list[str] = []
    consumer_ids: set[str] = set()
    for index, policy in enumerate(policies):
        prefix = f"policy_{index}"
        if not isinstance(policy, dict):
            violations.append(f"{prefix}:must_be_an_object")
            continue
        consumer_id = policy.get("consumer_id")
        if not isinstance(consumer_id, str) or not consumer_id.strip():
            violations.append(f"{prefix}:consumer_id_is_required")
        elif consumer_id in consumer_ids:
            violations.append(f"{prefix}:consumer_id_must_be_unique")
        else:
            consumer_ids.add(consumer_id)
        if policy.get("identity_key") not in approved_identity_keys:
            violations.append(f"{prefix}:identity_key_is_not_approved")
        limit = policy.get("limit")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            violations.append(f"{prefix}:limit_must_be_positive")
        if policy.get("window") not in {"second", "minute", "hour", "day"}:
            violations.append(f"{prefix}:window_must_be_explicit")
    return tuple(violations)


def consumer_rate_limits_are_safe(policies: object, **policy: object) -> bool:
    return not consumer_rate_limit_identity_violations(policies, **policy)
