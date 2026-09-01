# Add consumer credential revocation evidence gate

<!-- daily-pr-task: consumer-credential-revocation-evidence-gate -->

Deleting a consumer credential in the control plane is incomplete until data planes reject it and cached authentication state is purged. This offline gate requires a ticketed revocation, bounded rejection evidence, cache invalidation, and an audit event without recording credential material.

## Portfolio Value

Adds a testable credential-offboarding contract across Kong control and data planes while keeping secret values out of repository fixtures.

## Validation

Run python3 -m unittest discover -s tests and confirm bounded audited revocation passes while missing metadata, naive timestamps, late rejection, stale caches, acceptance of revoked credentials, and invalid policy fail.
