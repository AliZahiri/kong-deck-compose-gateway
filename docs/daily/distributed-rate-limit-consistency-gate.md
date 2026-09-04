# Add distributed rate-limit consistency gate

<!-- daily-pr-task: distributed-rate-limit-consistency-gate -->

Local counters let clients multiply an intended limit across gateway replicas. This offline policy gate requires protected routes to use a distributed Redis-backed counter, a secret-free environment reference, bounded connection timeouts, fail-closed behavior, and a unique counter namespace before decK sync.

## Portfolio Value

Prevents per-node counter multiplication and silent fail-open behavior in horizontally scaled Kong deployments while keeping connection details out of source control.

## Validation

Run python3 -m unittest discover -s tests and confirm rate limits use Redis, environment references, bounded timeouts, fail-closed behavior, and unique namespaces.
