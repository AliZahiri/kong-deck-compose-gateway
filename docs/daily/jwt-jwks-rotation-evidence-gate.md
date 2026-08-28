# Add JWT JWKS rotation evidence gate

<!-- daily-pr-task: jwt-jwks-rotation-evidence-gate -->

JWT validation can fail during signing-key rotation when a new key is used before JWKS publication or an old key is removed before token expiry. This offline gate validates unique public key identifiers, allowed algorithms, active and retiring key coverage, bounded overlap, timezone-aware validity, and absence of private key material.

## Portfolio Value

Adds deterministic JWT signing-key rollover evidence so gateway authentication stays verifiable throughout JWKS publication and retirement windows.

## Validation

Run python3 -m unittest discover -s tests and confirm duplicate kids, private material, disallowed algorithms, invalid validity, missing active/retiring coverage, and excessive retirement windows fail.
