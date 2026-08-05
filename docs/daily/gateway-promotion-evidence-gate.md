# Add gateway promotion evidence gate

<!-- daily-pr-task: gateway-promotion-evidence-gate -->

A successful decK command alone does not provide enough evidence that the reviewed declarative state was applied and remained healthy. This offline gate validates a supplied promotion record: immutable desired and applied state digests, source revision and decK version, review/sync/post-sync health outcomes, and fresh ordered timestamps. It consumes evidence only and never contacts a Kong Admin API.

## Portfolio Value

Makes a gateway promotion auditable by tying the reviewed declarative state to the applied state and a fresh post-sync health result.

## Validation

Run `python3 -m unittest discover -s tests` and confirm matching reviewed/applied state passes while malformed identity, mismatched state, failed review/sync/health checks, naive or stale timestamps, and invalid policy values fail.
