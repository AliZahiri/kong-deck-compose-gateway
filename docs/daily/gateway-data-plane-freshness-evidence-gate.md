# Add gateway data-plane freshness evidence gate

<!-- daily-pr-task: gateway-data-plane-freshness-evidence-gate -->

A successful control-plane sync is not sufficient evidence that hybrid Kong data planes are serving the intended configuration. This offline gate validates a minimum node quorum, unique node identities, ready sync status, exact declarative configuration digest parity, plugin-schema compatibility, control-plane attribution, and fresh timezone-aware observations.

## Portfolio Value

Adds hybrid-gateway propagation evidence after decK promotion so control-plane success cannot be mistaken for fleet-wide convergence, while remaining deterministic and disconnected from production Admin APIs in default CI.

## Validation

Run python3 -m unittest discover -s tests and confirm a fresh matching node quorum passes while duplicate nodes, stale or future observations, digest drift, incompatible plugin schemas, unready nodes, and invalid policy fail.
