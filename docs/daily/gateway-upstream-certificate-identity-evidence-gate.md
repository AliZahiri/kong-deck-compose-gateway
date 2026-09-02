# Add upstream certificate identity evidence gate

<!-- daily-pr-task: gateway-upstream-certificate-identity-evidence-gate -->

Enabling TLS verification is insufficient when the certificate identity does not match the promoted upstream. This offline gate validates SNI/SAN coverage, a SHA-256 fingerprint, trusted-chain status, revocation-check evidence, and a bounded expiry margin without making network calls in default CI.

## Portfolio Value

Extends upstream TLS policy from a boolean verification flag to auditable endpoint identity, trust, revocation, and expiry evidence.

## Validation

Run python3 -m unittest discover -s tests and confirm matching trusted certificates with revocation evidence and expiry margin pass while identity, fingerprint, chain, revocation, timestamp, and policy failures fail.
