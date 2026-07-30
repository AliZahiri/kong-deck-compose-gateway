# Add gateway certificate readiness gate

<!-- daily-pr-task: gateway-certificate-readiness-gate -->

TLS verification policy does not prove that the certificate selected for a gateway promotion is identifiable, unexpired, and valid for every promoted hostname. This metadata-only gate requires a complete SHA-256 fingerprint, timezone-aware expiry, a configurable validity margin, and explicit hostname coverage before decK sync. It never reads private keys or contacts the Admin API.

## Portfolio Value

Adds pre-sync certificate evidence so gateway promotion cannot proceed with an unidentified, expiring, malformed, or hostname-incomplete TLS certificate.

## Validation

Run `python3 -m unittest discover -s tests` and confirm ready certificates pass while missing identity, malformed fingerprints, naive expiry, insufficient validity, missing SAN metadata, uncovered hosts, and invalid policy values fail.
