# Add gateway error budget policy

<!-- daily-pr-task: gateway-error-budget-policy -->

Gateway error budget policy should define acceptable 5xx and upstream failure rates per route. This turns observability signals into an operational threshold.

Policy fields:

- route name
- max 5xx rate
- max upstream failure rate
- alert owner

## Portfolio Value

Connects gateway observability with explicit reliability thresholds.

## Validation

Run the unit test and confirm error budget thresholds are bounded.
