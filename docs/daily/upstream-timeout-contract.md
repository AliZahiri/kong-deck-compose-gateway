# Add upstream timeout contract

<!-- daily-pr-task: upstream-timeout-contract -->

Gateway timeouts should be explicit and bounded so an unhealthy upstream cannot consume all client connections. This policy validates the connect, read, and write timeout contract before a route is promoted.

## Portfolio Value

Adds an operationally meaningful gateway safety check around upstream latency and connection exhaustion.

## Validation

Run `python3 -m unittest discover -s tests` and confirm incomplete timeout contracts fail validation.
