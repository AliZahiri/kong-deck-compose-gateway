from __future__ import annotations

import re

_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_ALLOWED_ENVIRONMENTS = frozenset({"staging", "production"})


def config_provenance_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    digest = evidence.get("config_sha256")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        violations.append("config_sha256_is_invalid")
    if not isinstance(evidence.get("reviewed_by"), str) or not evidence["reviewed_by"].strip():
        violations.append("reviewed_by_is_required")
    if evidence.get("target_environment") not in _ALLOWED_ENVIRONMENTS:
        violations.append("target_environment_is_not_allowed")
    if evidence.get("deck_diff_reviewed") is not True:
        violations.append("deck_diff_must_be_reviewed")
    return tuple(violations)


def config_provenance_is_valid(evidence: dict[str, object]) -> bool:
    return not config_provenance_violations(evidence)
