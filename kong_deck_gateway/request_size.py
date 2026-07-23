from __future__ import annotations


_BODY_METHODS = {"POST", "PUT", "PATCH"}


def request_size_violations(route: dict[str, object], *, platform_max_megabytes: int = 32) -> tuple[str, ...]:
    if not isinstance(platform_max_megabytes, int) or isinstance(platform_max_megabytes, bool) or platform_max_megabytes < 1:
        raise ValueError("platform maximum must be a positive integer")
    methods = {str(method).upper() for method in route.get("methods", [])} if isinstance(route.get("methods", []), (list, tuple, set)) else set()
    if not methods & _BODY_METHODS:
        return ()
    limit = route.get("allowed_payload_size_megabytes")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        return ("positive_request_size_limit_is_required",)
    if limit > platform_max_megabytes:
        return ("request_size_limit_exceeds_platform_maximum",)
    return ()


def request_size_contract_is_valid(route: dict[str, object], *, platform_max_megabytes: int = 32) -> bool:
    return not request_size_violations(route, platform_max_megabytes=platform_max_megabytes)
