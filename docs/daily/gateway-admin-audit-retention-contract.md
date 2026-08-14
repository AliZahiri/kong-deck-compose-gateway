# Add gateway admin audit retention contract

<!-- daily-pr-task: gateway-admin-audit-retention-contract -->

Restricting the admin API is insufficient if configuration changes cannot be investigated. This offline contract checks that audit events are retained for a bounded positive period, include an actor and request ID, and redact credentials before storage.

## Portfolio Value

Complements admin API exposure controls with traceability and credential-redaction requirements for configuration-changing operations.

## Validation

Run `python3 -m unittest discover -s tests` and confirm a reviewable audit policy passes while invalid retention, absent actor or request IDs, missing redaction, and unsupported sinks fail.
