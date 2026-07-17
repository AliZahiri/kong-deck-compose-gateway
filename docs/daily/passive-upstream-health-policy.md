# Add passive upstream health policy

<!-- daily-pr-task: passive-upstream-health-policy -->

Passive upstream health checks should use bounded failure and recovery thresholds so Kong can eject an unhealthy target without making recovery impossible. The policy validates explicit TCP and HTTP failure thresholds plus the number of successful responses required for recovery.

## Portfolio Value

Adds a testable gateway resilience contract for automatic target ejection and recovery.

## Validation

Run `python3 -m unittest discover -s tests` and confirm missing or unbounded passive health thresholds fail validation.
