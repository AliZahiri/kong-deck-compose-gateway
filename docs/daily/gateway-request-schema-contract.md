# Add gateway request schema contract

<!-- daily-pr-task: gateway-request-schema-contract -->

Request-size limits do not guarantee that a route receives the intended media type and body shape. This offline gate validates a route request contract: non-empty allowed content types, JSON-only schema enforcement, a positive bounded request limit, and required fields with unique names. It evaluates configuration metadata without parsing live requests.

## Portfolio Value

Extends route policy beyond size and authentication controls to a reviewable input contract for API consumers.

## Validation

Run `python3 -m unittest discover -s tests` and confirm bounded JSON contracts pass while invalid content types, non-JSON schema enforcement, unbounded bodies, duplicate fields, and invalid limits fail.
