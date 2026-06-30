from __future__ import annotations

PUBLIC_CATCH_ALL = {"0.0.0.0/0", "::/0"}


def ip_allowlist_warnings(policy: dict[str, object], *, allow_public: bool = False) -> tuple[str, ...]:
    warnings: list[str] = []
    cidrs = policy.get("cidrs")
    if not isinstance(cidrs, list) or not cidrs:
        warnings.append("cidrs_missing")
        cidrs = []
    if set(cidrs) & PUBLIC_CATCH_ALL and not allow_public:
        warnings.append("public_catch_all_requires_approval")
    if not policy.get("owner"):
        warnings.append("owner_missing")
    return tuple(warnings)


def ip_allowlist_is_safe(policy: dict[str, object], *, allow_public: bool = False) -> bool:
    return not ip_allowlist_warnings(policy, allow_public=allow_public)
