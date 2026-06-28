# Add gateway timeout policy

<!-- daily-pr-task: gateway-timeout-policy -->

Gateway timeout policy protects callers and upstreams from unbounded waits. Route and service definitions should keep connect, read, and write timeouts explicit.

Policy fields:

- connect timeout
- read timeout
- write timeout
- maximum allowed timeout

## Portfolio Value

Shows route protection includes bounded upstream timeouts.

## Validation

Run the unit test and confirm missing or excessive timeouts are reported.
