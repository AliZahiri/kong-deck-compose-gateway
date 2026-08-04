from __future__ import annotations

import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def state_snapshot_integrity_violations(snapshot: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not str(snapshot.get("snapshot_id", "")).strip():
        violations.append("snapshot_id_is_required")
    if not str(snapshot.get("kong_version", "")).strip():
        violations.append("kong_version_is_required")
    expected = snapshot.get("expected_sha256")
    stored = snapshot.get("stored_sha256")
    for field, value in (("expected_sha256", expected), ("stored_sha256", stored)):
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            violations.append(f"{field}_is_invalid")
    if isinstance(expected, str) and isinstance(stored, str) and _SHA256.fullmatch(expected) and _SHA256.fullmatch(stored) and expected != stored:
        violations.append("stored_snapshot_digest_mismatch")
    if snapshot.get("encrypted_at_rest") is not True:
        violations.append("snapshot_must_be_encrypted_at_rest")
    if snapshot.get("restore_verified") is not True:
        violations.append("snapshot_restore_must_be_verified")
    return tuple(violations)


def deck_state_snapshot_is_rollback_ready(snapshot: dict[str, object]) -> bool:
    return not state_snapshot_integrity_violations(snapshot)
