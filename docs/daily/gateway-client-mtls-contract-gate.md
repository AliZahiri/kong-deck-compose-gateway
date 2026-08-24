# Add gateway client mTLS contract gate

<!-- daily-pr-task: gateway-client-mtls-contract-gate -->

Sensitive routes should declare a reviewable client mTLS contract. This offline gate requires mTLS enablement, an external CA reference, bounded verification depth, revocation checking, and at least one allowed client subject without embedding certificates.

## Portfolio Value

Extends gateway authentication controls with certificate-based client identity while preserving secret hygiene and offline CI validation.

## Validation

Run python3 -m unittest discover -s tests and confirm routes without external CA references, revocation checks, or explicit client subjects fail.
