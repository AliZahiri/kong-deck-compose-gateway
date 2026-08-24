from __future__ import annotations


def client_mtls_violations(route: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(route.get("route_id"), str) or not route["route_id"].strip():
        violations.append("route_id_is_required")
    if route.get("mtls_enabled") is not True:
        violations.append("client_mtls_must_be_enabled")
    ca_ref = route.get("ca_bundle_ref")
    if not isinstance(ca_ref, str) or not ca_ref.startswith(("secret://", "vault://")):
        violations.append("ca_bundle_must_use_an_external_secret_reference")
    depth = route.get("verify_depth")
    if not isinstance(depth, int) or isinstance(depth, bool) or not 1 <= depth <= 10:
        violations.append("verify_depth_must_be_between_1_and_10")
    if route.get("revocation_check") is not True:
        violations.append("certificate_revocation_check_is_required")
    subjects = route.get("allowed_subjects")
    if not isinstance(subjects, list) or not subjects or any(not isinstance(item, str) or not item.strip() for item in subjects):
        violations.append("allowed_subjects_must_be_a_non_empty_string_list")
    return tuple(violations)


def client_mtls_contract_is_valid(route: dict[str, object]) -> bool:
    return not client_mtls_violations(route)
