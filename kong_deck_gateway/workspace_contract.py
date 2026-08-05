from __future__ import annotations


def gateway_workspace_contract_violations(resources: list[dict[str, object]], *, environment: str) -> tuple[str, ...]:
    if not isinstance(environment, str) or not environment.strip():
        raise ValueError("environment must be a non-empty string")
    expected_environment = environment.strip().lower()
    if not resources:
        return ("at_least_one_resource_is_required",)

    violations: list[str] = []
    identities: set[tuple[str, str]] = set()
    for index, resource in enumerate(resources):
        if not isinstance(resource, dict):
            violations.append(f"resource_{index}:metadata_is_required")
            continue
        resource_type = str(resource.get("type", "")).strip().lower()
        name = str(resource.get("name", "")).strip()
        if not resource_type:
            violations.append(f"resource_{index}:type_is_required")
        if not name:
            violations.append(f"resource_{index}:name_is_required")
        if resource_type and name:
            identity = (resource_type, name)
            if identity in identities:
                violations.append(f"resource_{index}:type_and_name_must_be_unique")
            identities.add(identity)
        if str(resource.get("workspace", "")).strip().lower() != expected_environment:
            violations.append(f"resource_{index}:workspace_must_match_environment")
        tags = resource.get("tags")
        environment_tags = [str(tag).strip().lower() for tag in tags if isinstance(tag, str) and str(tag).strip().lower().startswith("env:")] if isinstance(tags, list) else []
        if environment_tags != [f"env:{expected_environment}"]:
            violations.append(f"resource_{index}:must_have_one_matching_environment_tag")
    return tuple(violations)


def gateway_workspace_contract_is_satisfied(resources: list[dict[str, object]], **policy: object) -> bool:
    return not gateway_workspace_contract_violations(resources, **policy)
