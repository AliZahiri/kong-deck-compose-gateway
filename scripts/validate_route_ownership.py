from __future__ import annotations

def route_ownership_violations(routes: object, *, required_environment: str) -> tuple[str, ...]:
    if not isinstance(required_environment, str) or not required_environment.strip(): raise ValueError('required_environment must be nonempty')
    if not isinstance(routes, list) or not routes: return ('route_catalog_must_be_a_nonempty_list',)
    violations: list[str] = []; route_ids: set[str] = set(); paths: set[str] = set()
    for index, route in enumerate(routes):
        prefix=f'route_{index}'
        if not isinstance(route, dict): violations.append(f'{prefix}:must_be_an_object'); continue
        route_id, path, owner = route.get('id'), route.get('path'), route.get('owner')
        if not isinstance(route_id,str) or not route_id.strip() or route_id in route_ids: violations.append(f'{prefix}:id_must_be_nonempty_and_unique')
        else: route_ids.add(route_id)
        if not isinstance(path,str) or not path.startswith('/') or path in paths: violations.append(f'{prefix}:path_must_be_absolute_and_unique')
        else: paths.add(path)
        if not isinstance(owner,str) or not owner.strip(): violations.append(f'{prefix}:owner_must_be_nonempty')
        if route.get('environment') != required_environment: violations.append(f'{prefix}:environment_must_match_promotion_target')
    return tuple(violations)
