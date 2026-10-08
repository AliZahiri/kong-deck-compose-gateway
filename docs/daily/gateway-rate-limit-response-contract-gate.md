# Add gateway rate-limit response contract gate

<!-- daily-pr-task: gateway-rate-limit-response-contract-gate -->

Clients need deterministic, non-sensitive feedback when a gateway applies a rate limit. This offline gate validates a declared status code and a small allowlist of response headers without contacting a gateway.

## Portfolio Value

Keeps rate-limit behavior predictable for clients while preventing a policy from accidentally disclosing sensitive response metadata.

## Validation

Run python3 -m unittest discover -s tests and confirm a 429 response with unique allowlisted headers passes.
