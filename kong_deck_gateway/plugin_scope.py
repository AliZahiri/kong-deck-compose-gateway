from __future__ import annotations

SCOPED_PLUGIN_KEYS = ("route", "service", "consumer")


def plugin_scope_warnings(plugin: dict[str, object], *, allow_global: bool = False) -> tuple[str, ...]:
    if any(plugin.get(key) for key in SCOPED_PLUGIN_KEYS):
        return ()
    return () if allow_global else ("plugin_scope_missing",)


def plugin_scope_is_safe(plugin: dict[str, object], *, allow_global: bool = False) -> bool:
    return not plugin_scope_warnings(plugin, allow_global=allow_global)
