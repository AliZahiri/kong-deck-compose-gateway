# Add upstream target drain policy

<!-- daily-pr-task: upstream-target-drain-policy -->

Removing a Kong upstream target should require explicit drain evidence rather than assuming a zero weight is sufficient. This policy requires the target weight to be zero, active connections to remain at zero across a configurable number of observations, a minimum drain interval to elapse, and a healthy replacement target to be available before removal.

## Portfolio Value

Adds evidence-based upstream removal safety so target deletion waits for traffic drain and healthy replacement capacity.

## Validation

Run `python3 -m unittest discover -s tests` and confirm fully drained targets pass while nonzero weight/connections, insufficient observations or duration, invalid counters, and missing replacement health fail.
