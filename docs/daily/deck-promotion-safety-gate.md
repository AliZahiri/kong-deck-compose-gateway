# Add decK promotion safety gate

<!-- daily-pr-task: deck-promotion-safety-gate -->

A decK promotion should combine diff approval, route preflight, and upstream timeout contracts in one deterministic report. The gate blocks destructive or unknown changes, unsafe routes, and unbounded service timeouts before sync.

## Portfolio Value

Builds a credible decK pre-sync gate spanning change review, route security, and upstream reliability.

## Validation

Run `python3 -m unittest discover -s tests` and confirm diff, route, and timeout violations block promotion together.
