# Add gateway route path canonicalization gate

<!-- daily-pr-task: gateway-route-path-canonicalization-gate -->

A route can be unambiguous in decK yet be interpreted differently by clients, proxies, and upstreams when it contains traversal segments, duplicate separators, or encoded path separators. This offline gate enforces a canonical non-regex path form before sync. Regex routes are intentionally delegated to the dedicated regex safety policy.

## Portfolio Value

Prevents a class of path interpretation and authorization mismatches before a decK sync can expose them at the edge.

## Validation

Run python3 -m unittest discover -s tests and confirm canonical paths pass while traversal, duplicate or encoded separators, implicit trailing slashes, malformed routes, and non-list input fail.
