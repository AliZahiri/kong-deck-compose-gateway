from __future__ import annotations

import re

_HOST = re.compile(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+\Z')


def upstream_host_header_violations(services: object) -> tuple[str, ...]:
    if not isinstance(services, list) or not services: return ('services_must_be_a_non_empty_list',)
    violations: list[str] = []; names: set[str] = set()
    for position, service in enumerate(services):
        prefix=f'service_{position}'
        if not isinstance(service, dict): violations.append(f'{prefix}:service_must_be_an_object'); continue
        name=service.get('name')
        if not isinstance(name, str) or not name.strip(): violations.append(f'{prefix}:name_is_required')
        elif name in names: violations.append(f'{prefix}:name_must_be_unique')
        else: names.add(name)
        preserve=service.get('preserve_host')
        if not isinstance(preserve, bool): violations.append(f'{prefix}:preserve_host_must_be_explicit')
        elif not preserve and (not isinstance(service.get('upstream_host'), str) or not _HOST.fullmatch(service['upstream_host'].lower())): violations.append(f'{prefix}:rewritten_upstream_host_must_be_dns_name')
    return tuple(violations)
