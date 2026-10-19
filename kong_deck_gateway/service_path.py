from __future__ import annotations


def service_path_violations(services: object) -> tuple[str, ...]:
    if not isinstance(services, list) or not services: return ('services_must_be_a_non_empty_list',)
    violations: list[str] = []
    names: set[str] = set()
    for position, service in enumerate(services):
        prefix = f'service_{position}'
        if not isinstance(service, dict): violations.append(f'{prefix}:service_must_be_an_object'); continue
        name = service.get('name')
        if not isinstance(name, str) or not name.strip(): violations.append(f'{prefix}:name_is_required')
        elif name in names: violations.append(f'{prefix}:name_must_be_unique')
        else: names.add(name)
        path = service.get('path')
        if not isinstance(path, str) or not path.startswith('/') or '//' in path or '?' in path or '#' in path or any(part in {'.', '..'} for part in path.split('/')): violations.append(f'{prefix}:path_must_be_canonical_and_absolute')
    return tuple(violations)
