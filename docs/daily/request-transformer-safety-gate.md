# Add request transformer safety gate

<!-- daily-pr-task: request-transformer-safety-gate -->

Gateway request transformations can silently remove traceability or forge security-relevant identity headers. This offline gate validates a route's requested header changes before decK sync: protected headers may not be removed or overwritten, header names are unique case-insensitively, and a request ID preservation rule is required. It evaluates desired configuration only and does not contact Kong.

## Portfolio Value

Adds a configuration-as-code control for a subtle gateway risk: transformations must not erase tracing or rewrite protected client identity and authorization context.

## Validation

Run `python3 -m unittest discover -s tests` and confirm safe header additions pass while non-list policies, protected header modification, case-insensitive duplicates, invalid operations, and missing request-ID preservation fail.
