from __future__ import annotations

from datetime import datetime


def data_plane_convergence_violations(expected_digest: str, observations: list[dict[str, object]], *, promoted_at: datetime, maximum_convergence_seconds: int = 120) -> tuple[str, ...]:
    if promoted_at.tzinfo is None or promoted_at.utcoffset() is None:
        raise ValueError("promoted_at must be timezone-aware")
    if not isinstance(maximum_convergence_seconds, int) or isinstance(maximum_convergence_seconds, bool) or maximum_convergence_seconds < 1:
        raise ValueError("maximum_convergence_seconds must be a positive integer")
    if not isinstance(expected_digest, str) or not expected_digest.strip():
        return ("expected_digest_is_required",)
    if not isinstance(observations, list) or not observations:
        return ("at_least_one_data_plane_observation_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            violations.append(f"node_{index}:observation_must_be_an_object")
            continue
        node_id = observation.get("node_id")
        if not isinstance(node_id, str) or not node_id.strip():
            violations.append(f"node_{index}:node_id_is_required")
        elif node_id in seen:
            violations.append(f"node_{index}:node_id_must_be_unique")
        else:
            seen.add(node_id)
        if observation.get("ready") is not True:
            violations.append(f"node_{index}:node_must_be_ready")
        if observation.get("config_digest") != expected_digest:
            violations.append(f"node_{index}:config_digest_does_not_match")
        observed_at = _timestamp(observation.get("observed_at"))
        if observed_at is None:
            violations.append(f"node_{index}:observed_at_must_be_timezone_aware")
        elif not 0 <= (observed_at - promoted_at).total_seconds() <= maximum_convergence_seconds:
            violations.append(f"node_{index}:observation_is_outside_convergence_window")
    return tuple(violations)


def data_plane_has_converged(expected_digest: str, observations: list[dict[str, object]], **policy: object) -> bool:
    return not data_plane_convergence_violations(expected_digest, observations, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
