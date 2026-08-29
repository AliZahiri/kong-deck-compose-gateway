# Add upstream keepalive resource contract gate

<!-- daily-pr-task: upstream-keepalive-resource-contract-gate -->

Upstream keepalive settings should be explicit and bounded so connection reuse does not create an unbounded socket pool or stale idle connections. This offline contract validates per-service pool size, idle timeout, reuse limit, and timeout ordering from declarative configuration only.

## Portfolio Value

Adds deterministic gateway resource controls around connection reuse, complementing upstream health and timeout policies with bounded socket-pool behavior.

## Validation

Run python3 -m unittest discover -s tests and confirm missing services, oversized pools, excessive idle timeouts, invalid reuse limits, inverted request timeouts, and invalid policy fail.
