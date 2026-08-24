from __future__ import annotations


def _sni_covers(host: str, sni: str) -> bool:
    host, sni = host.lower().rstrip("."), sni.lower().rstrip(".")
    if host == sni:
        return True
    if not sni.startswith("*."):
        return False
    suffix = sni[2:]
    return host.endswith("." + suffix) and host.count(".") == suffix.count(".") + 1


def route_sni_coverage_violations(routes: list[dict[str, object]], active_snis: list[str]) -> tuple[str, ...]:
    snis = [item for item in active_snis if isinstance(item, str) and item.strip()]
    if not snis:
        return ("at_least_one_active_sni_is_required",)
    violations: list[str] = []
    seen_names: set[str] = set()
    for index, route in enumerate(routes):
        name, hosts = route.get("name"), route.get("hosts")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"route_{index}:name_is_required")
        elif name in seen_names:
            violations.append(f"route_{index}:name_must_be_unique")
        else:
            seen_names.add(name)
        if not isinstance(hosts, list) or not hosts or any(not isinstance(host, str) or not host.strip() for host in hosts):
            violations.append(f"route_{index}:hosts_must_be_a_non_empty_string_list")
            continue
        for host in hosts:
            if not any(_sni_covers(host, sni) for sni in snis):
                violations.append(f"route_{index}:host_{host}_has_no_active_sni")
    return tuple(violations)


def routes_have_sni_coverage(routes: list[dict[str, object]], active_snis: list[str]) -> bool:
    return not route_sni_coverage_violations(routes, active_snis)
