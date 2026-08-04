# Add decK state snapshot integrity gate

<!-- daily-pr-task: deck-state-snapshot-integrity-gate -->

A backup reference on a destructive change is not useful unless the saved decK state is immutable, protected, and proven restorable. This metadata-only gate validates snapshot identity, matching SHA-256 digests, encryption, Kong version metadata, and successful restore verification before promotion.

## Portfolio Value

Makes gateway rollback evidence operationally credible by requiring an immutable, encrypted, versioned, and restore-tested decK state snapshot instead of a free-form backup label.

## Validation

Run `python3 -m unittest discover -s tests` and confirm protected matching snapshots pass while missing identity/version, malformed or mismatched digests, absent encryption, and unverified restore evidence fail.
