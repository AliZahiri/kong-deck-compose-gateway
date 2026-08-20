from __future__ import annotations

import re


_DIGEST = re.compile(r"[a-f0-9]{64}\Z")
_VERSION = re.compile(r"v[1-9]\d*\Z")


def config_schema_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    declared = evidence.get("declared_schema_version")
    supported = evidence.get("supported_schema_version")
    if not isinstance(declared, str) or not _VERSION.fullmatch(declared):
        violations.append("declared_schema_version_is_invalid")
    if not isinstance(supported, str) or not _VERSION.fullmatch(supported):
        violations.append("supported_schema_version_is_invalid")
    elif isinstance(declared, str) and _VERSION.fullmatch(declared) and declared != supported:
        violations.append("declared_schema_version_is_not_supported")
    for field in ("config_sha256", "rollback_snapshot_sha256"):
        value = evidence.get(field)
        if not isinstance(value, str) or not _DIGEST.fullmatch(value):
            violations.append(f"{field}_is_invalid")
    if evidence.get("deck_diff_reviewed") is not True:
        violations.append("deck_diff_must_be_reviewed")
    return tuple(violations)


def config_schema_is_compatible(evidence: dict[str, object]) -> bool:
    return not config_schema_violations(evidence)
