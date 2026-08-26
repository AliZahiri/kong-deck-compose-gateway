from __future__ import annotations


def plugin_instance_identity_violations(plugins: list[dict[str, object]]) -> tuple[str, ...]:
    if not isinstance(plugins, list) or not plugins:
        return ("at_least_one_plugin_instance_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin.get("name"), str) or not plugin["name"].strip():
            violations.append(f"plugin_{index}:name_is_required")
        instance = plugin.get("instance_name")
        if not isinstance(instance, str) or not instance.strip():
            violations.append(f"plugin_{index}:instance_name_is_required")
        elif instance.casefold() in seen:
            violations.append(f"plugin_{index}:instance_name_must_be_unique")
        else:
            seen.add(instance.casefold())
        scopes = [field for field in ("route", "service", "consumer", "global") if plugin.get(field)]
        if len(scopes) != 1:
            violations.append(f"plugin_{index}:exactly_one_scope_is_required")
        tags = plugin.get("tags")
        if not isinstance(tags, list) or not any(isinstance(tag, str) and tag.startswith("owner:") and tag[6:].strip() for tag in tags):
            violations.append(f"plugin_{index}:owner_tag_is_required")
    return tuple(violations)


def plugin_instance_identities_are_valid(plugins: list[dict[str, object]]) -> bool:
    return not plugin_instance_identity_violations(plugins)
