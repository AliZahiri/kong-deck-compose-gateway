from __future__ import annotations

ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}


def route_method_warnings(methods: list[str]) -> tuple[str, ...]:
    if not methods:
        return ("route_methods_are_required",)
    normalized = [method.upper().strip() for method in methods]
    warnings: list[str] = []
    if any(method not in ALLOWED_METHODS for method in normalized):
        warnings.append("route_method_is_not_allowed")
    if len(set(normalized)) != len(normalized):
        warnings.append("route_methods_must_be_unique")
    return tuple(warnings)


def route_methods_are_safe(methods: list[str]) -> bool:
    return not route_method_warnings(methods)
