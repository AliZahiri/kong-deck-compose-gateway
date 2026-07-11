from __future__ import annotations

REQUIRED_OWNER_FIELDS = ("route", "owner", "escalation", "tier")
VALID_TIERS = {"critical", "standard", "internal"}


def route_owner_warnings(metadata: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    for field in REQUIRED_OWNER_FIELDS:
        if not str(metadata.get(field, "")).strip():
            warnings.append(f"{field}_is_required")
    tier = str(metadata.get("tier", "")).strip()
    if tier and tier not in VALID_TIERS:
        warnings.append("tier_is_unknown")
    return tuple(warnings)


def route_owner_is_valid(metadata: dict[str, object]) -> bool:
    return not route_owner_warnings(metadata)
