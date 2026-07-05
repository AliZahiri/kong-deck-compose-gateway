from __future__ import annotations

AUTH_PLUGINS = {"jwt", "key-auth", "openid-connect"}


def plugin_order_warnings(plugins: list[str]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not plugins:
        return ("plugins_missing",)
    auth_positions = [index for index, plugin in enumerate(plugins) if plugin in AUTH_PLUGINS]
    if not auth_positions:
        warnings.append("auth_plugin_missing")
        return tuple(warnings)
    auth_index = min(auth_positions)
    for plugin in ("rate-limiting", "request-transformer"):
        if plugin in plugins and plugins.index(plugin) < auth_index:
            warnings.append(f"{plugin}_runs_before_auth")
    return tuple(warnings)


def plugin_order_is_safe(plugins: list[str]) -> bool:
    return not plugin_order_warnings(plugins)
