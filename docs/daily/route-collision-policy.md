# Add route collision detection policy

<!-- daily-pr-task: route-collision-policy -->

Two gateway routes that claim the same host, path, and overlapping HTTP methods can make traffic ownership depend on router precedence. This policy detects exact routing-space collisions before decK sync, treating a route without explicit methods as matching every method. The result can be surfaced in promotion review without contacting the Admin API.

## Portfolio Value

Adds a deterministic gateway promotion guard against ambiguous route ownership and precedence-sensitive traffic behavior.

## Validation

Run `python3 -m unittest discover -s tests` and confirm overlapping host/path/method space is reported while disjoint methods remain valid.
