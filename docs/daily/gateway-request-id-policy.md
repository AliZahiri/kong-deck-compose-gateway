# Add gateway request identifier policy

<!-- daily-pr-task: gateway-request-id-policy -->

Gateway traffic should carry a bounded request identifier for traceability across Kong, upstream services, and incident logs. The policy validates the header name and avoids accepting arbitrary oversized values.

## Portfolio Value

Adds a practical observability contract around request tracing at the API gateway boundary.

## Validation

Run `python3 -m unittest discover -s tests` and confirm oversized request identifiers are rejected.
