# Add gateway retry safety contract

<!-- daily-pr-task: gateway-retry-safety-contract -->

Gateway retries can amplify non-idempotent requests and duplicate side effects even when upstream timeouts are valid. This offline contract validates route identity, method metadata, bounded retry counts, and explicit idempotency-key enforcement for retried unsafe methods. It evaluates declarative policy only and never changes Kong configuration.

## Portfolio Value

Makes gateway retry behavior reviewable and side-effect aware by bounding retry amplification and requiring idempotency evidence for unsafe HTTP methods.

## Validation

Run `python3 -m unittest discover -s tests` and confirm safe methods and idempotency-protected unsafe methods pass while malformed routes, duplicate names, invalid or excessive retries, unprotected unsafe methods, and invalid policy values fail.
