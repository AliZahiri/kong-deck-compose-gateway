from __future__ import annotations

from datetime import datetime
import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def data_plane_freshness_violations(nodes: list[dict[str, object]], *, expected_config_digest: str, now: datetime, minimum_ready_nodes: int = 2, maximum_age_seconds: int = 300) -> tuple[str, ...]:
    if _DIGEST.fullmatch(expected_config_digest) is None:
        raise ValueError("expected_config_digest must be an immutable sha256 digest")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    for name, value in (("minimum_ready_nodes", minimum_ready_nodes), ("maximum_age_seconds", maximum_age_seconds)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if not isinstance(nodes, list) or not nodes:
        return ("at_least_one_data_plane_node_is_required",)
    violations: list[str] = []
    seen_nodes: set[str] = set()
    ready_nodes = 0
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            violations.append(f"node_{index}:must_be_an_object")
            continue
        node_id = node.get("node_id")
        if not isinstance(node_id, str) or not node_id.strip():
            violations.append(f"node_{index}:node_id_is_required")
        elif node_id in seen_nodes:
            violations.append(f"node_{index}:node_id_must_be_unique")
        else:
            seen_nodes.add(node_id)
        if not isinstance(node.get("control_plane_id"), str) or not node["control_plane_id"].strip():
            violations.append(f"node_{index}:control_plane_id_is_required")
        if node.get("sync_status") != "ready":
            violations.append(f"node_{index}:sync_status_must_be_ready")
        else:
            ready_nodes += 1
        digest = node.get("config_digest")
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            violations.append(f"node_{index}:config_digest_must_be_immutable")
        elif digest != expected_config_digest:
            violations.append(f"node_{index}:config_digest_does_not_match_control_plane")
        if node.get("plugin_schema_compatible") is not True:
            violations.append(f"node_{index}:plugin_schema_must_be_compatible")
        observed_at = _timestamp(node.get("observed_at"))
        if observed_at is None:
            violations.append(f"node_{index}:observed_at_must_be_timezone_aware")
        else:
            age = (now - observed_at).total_seconds()
            if age < 0:
                violations.append(f"node_{index}:observation_must_not_be_in_the_future")
            elif age > maximum_age_seconds:
                violations.append(f"node_{index}:observation_is_stale")
    if ready_nodes < minimum_ready_nodes:
        violations.append("ready_data_plane_quorum_is_below_policy")
    return tuple(violations)


def data_plane_configuration_is_fresh(nodes: list[dict[str, object]], **policy: object) -> bool:
    return not data_plane_freshness_violations(nodes, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
