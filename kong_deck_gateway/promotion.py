from __future__ import annotations

REQUIRED_PROMOTION_STEPS = (
    "start_inactive_backend",
    "wait_for_health",
    "render_deck_state",
    "run_deck_diff",
    "sync_gateway_state",
    "verify_proxy_traffic",
    "stop_old_backend_after_verification",
)


def missing_promotion_steps(steps: list[str] | tuple[str, ...] | set[str]) -> tuple[str, ...]:
    present = set(steps)
    return tuple(step for step in REQUIRED_PROMOTION_STEPS if step not in present)


def promotion_order_warnings(steps: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    position = {step: index for index, step in enumerate(steps)}
    warnings: list[str] = []
    if position.get("run_deck_diff", -1) > position.get("sync_gateway_state", 10**6):
        warnings.append("deck_diff_must_run_before_sync")
    if position.get("verify_proxy_traffic", -1) > position.get("stop_old_backend_after_verification", 10**6):
        warnings.append("proxy_verification_must_happen_before_stopping_old_backend")
    return tuple(warnings)


def promotion_plan_is_complete(steps: list[str] | tuple[str, ...] | set[str]) -> bool:
    if missing_promotion_steps(steps):
        return False
    if not isinstance(steps, set) and promotion_order_warnings(steps):
        return False
    return True
