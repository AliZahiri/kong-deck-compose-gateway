from __future__ import annotations

PROTECTED_PLUGINS = {"jwt", "rate-limiting", "request-size-limiting", "ip-restriction"}


def plugin_drift_warnings(desired: set[str], live: set[str]) -> tuple[str, ...]:
    warnings: list[str] = []
    missing_live = sorted(desired - live)
    unmanaged_live = sorted(live - desired)
    for plugin in missing_live:
        warnings.append(f"missing_live_plugin:{plugin}")
    for plugin in unmanaged_live:
        warnings.append(f"unmanaged_live_plugin:{plugin}")
    for plugin in sorted((desired ^ live) & PROTECTED_PLUGINS):
        warnings.append(f"protected_plugin_drift:{plugin}")
    return tuple(warnings)


def plugin_state_matches(desired: set[str], live: set[str]) -> bool:
    return not plugin_drift_warnings(desired, live)
