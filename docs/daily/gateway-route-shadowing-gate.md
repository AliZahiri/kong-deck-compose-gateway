# Add gateway route shadowing gate

<!-- daily-pr-task: gateway-route-shadowing-gate -->

Detect duplicate route identity declarations before decK promotion so a broad or repeated route cannot silently shadow its intended owner.

## Portfolio Value

Adds a deterministic pre-promotion safety check for route ownership and accidental duplicate declarations.

## Validation

Run `python3 -m unittest discover -s tests` and confirm malformed or duplicate route identities fail.
