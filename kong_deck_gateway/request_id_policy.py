from __future__ import annotations


def request_id_warnings(header_name: str, value: str, *, max_length: int = 128) -> tuple[str, ...]:
    warnings: list[str] = []
    if header_name.lower() != "x-request-id":
        warnings.append("request_id_header_must_be_x_request_id")
    if not value.strip():
        warnings.append("request_id_value_is_required")
    elif len(value) > max_length:
        warnings.append("request_id_value_exceeds_max_length")
    return tuple(warnings)


def request_id_is_safe(header_name: str, value: str, *, max_length: int = 128) -> bool:
    return not request_id_warnings(header_name, value, max_length=max_length)
