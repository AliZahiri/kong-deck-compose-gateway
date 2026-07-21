# Add upstream TLS verification policy

<!-- daily-pr-task: upstream-tls-verification-policy -->

Gateway-to-upstream encryption is incomplete when certificate verification, trusted CA references, or a bounded verification depth are omitted. This policy validates the declarative service TLS contract before decK sync and keeps private certificates outside the repository by checking only certificate identifiers.

## Portfolio Value

Adds a production gateway security contract for authenticated upstream transport without storing certificate material or making live network calls.

## Validation

Run `python3 -m unittest discover -s tests` and confirm plaintext, disabled verification, invalid depth, and missing CA references fail validation.
