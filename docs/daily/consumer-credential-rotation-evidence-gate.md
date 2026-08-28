# Add consumer credential rotation evidence gate

<!-- daily-pr-task: consumer-credential-rotation-evidence-gate -->

Credential expiry policy does not prove that a rotation completed safely. This offline gate validates a metadata-only consumer rotation record: distinct old and new credential identities, verification of the replacement before revocation, a bounded overlap window, zero post-rotation authentication failures, and absence of raw credential material.

## Portfolio Value

Completes the credential lifecycle story by validating safe replacement, bounded overlap, revocation, and post-rotation health without storing secrets.

## Validation

Run python3 -m unittest discover -s tests and confirm premature revocation, excessive overlap, reused identities, raw credential fields, incomplete state, and authentication failures fail.
