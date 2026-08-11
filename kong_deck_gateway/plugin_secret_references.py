from __future__ import annotations

import re


_ENV_REFERENCE = re.compile(r"\$\{[A-Z][A-Z0-9_]*\}\Z")


def plugin_secret_reference_violations(settings: list[dict[str, object]]) -> tuple[str, ...]:
    if not settings:
        return ("at_least_one_setting_is_required",)
    violations: list[str] = []
    seen_references: set[str] = set()
    for index, setting in enumerate(settings):
        if setting.get("sensitive") is not True:
            continue
        value = setting.get("value")
        if not isinstance(value, str) or not _ENV_REFERENCE.fullmatch(value):
            violations.append(f"setting_{index}:sensitive_value_must_be_environment_reference")
            continue
        if value in seen_references:
            violations.append(f"setting_{index}:secret_reference_must_be_unique")
        seen_references.add(value)
    return tuple(violations)


def plugin_secret_references_are_safe(settings: list[dict[str, object]]) -> bool:
    return not plugin_secret_reference_violations(settings)
