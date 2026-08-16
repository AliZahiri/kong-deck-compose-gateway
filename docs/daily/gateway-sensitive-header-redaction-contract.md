# Add gateway sensitive header redaction contract

<!-- daily-pr-task: gateway-sensitive-header-redaction-contract -->

Gateway request logging requires an explicit sensitive-header redaction policy. This offline contract validates that authentication and client credential headers are listed, header matching is case-insensitive, and logs retain a request ID for safe traceability without storing secrets.

## Portfolio Value

Adds a practical privacy and security control to gateway observability without logging credentials or requiring a live Kong instance.

## Validation

Run `python3 -m unittest discover -s tests` and confirm case-insensitive policies redact Authorization, Cookie, and X-API-Key while retaining request IDs.
