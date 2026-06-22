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


def promotion_plan_is_complete(steps: list[str] | tuple[str, ...] | set[str]) -> bool:
    return not missing_promotion_steps(steps)
