# Add upstream change ticket gate

<!-- daily-pr-task: gateway-upstream-change-ticket-gate -->

This offline gate makes upstream changes reviewable before decK promotion. It requires a change ticket, accountable owner, and a non-empty unique list of affected upstreams. Removing an upstream also requires a rollback reference; this complements decK diff, health, and traffic-drain checks.

## Portfolio Value

Connects decK upstream promotion with traceable operational change ownership.

## Validation

Run python3 -m unittest discover -s tests. Tests cover a ticketed update plus missing ownership, duplicate or malformed upstream scope, and removals without a rollback reference.
