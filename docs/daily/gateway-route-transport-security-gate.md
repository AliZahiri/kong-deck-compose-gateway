# Add gateway route transport security gate

<!-- daily-pr-task: gateway-route-transport-security-gate -->

A public gateway route should not accidentally retain a plaintext listener after a declarative update. This offline gate validates route metadata: unique names, an explicit public or internal exposure class, a non-empty supported protocol list, and encrypted-only protocols for public routes. It validates supplied decK-style metadata; it does not configure certificates or terminate TLS.

## Portfolio Value

Turns a common declarative gateway regression—leaving plaintext protocol access on a public route—into a focused, reviewable policy check without making unsupported certificate claims.

## Validation

Run `python3 -m unittest discover -s tests` and confirm encrypted public routes pass while empty, duplicate, invalid-exposure, unsupported-protocol, plaintext-public, and strict-internal-policy cases fail.
