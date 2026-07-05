from __future__ import annotations

REQUIRED_TAG_PREFIXES = ("owner:", "env:", "runbook:", "criticality:")


def missing_service_tag_prefixes(tags: list[str]) -> tuple[str, ...]:
    return tuple(prefix for prefix in REQUIRED_TAG_PREFIXES if not any(tag.startswith(prefix) for tag in tags))


def service_tags_are_complete(tags: list[str]) -> bool:
    return not missing_service_tag_prefixes(tags)
