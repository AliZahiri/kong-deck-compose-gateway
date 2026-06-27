# Add consumer quota policy

<!-- daily-pr-task: consumer-quota-policy -->

Consumer quota policy should define per-consumer request budgets before plugins are applied. This keeps shared API limits predictable and auditable.

Policy fields:

- consumer name
- requests per minute
- burst allowance
- alert threshold

## Portfolio Value

Shows gateway governance for shared APIs and tenant-aware traffic protection.

## Validation

Run the unit test and confirm quota limits must be positive.
