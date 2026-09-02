# Add gateway control-plane backup evidence gate

<!-- daily-pr-task: gateway-control-plane-backup-evidence-gate -->

A decK state export is not recovery evidence unless it is recent, integrity-protected, encrypted at rest, schema-compatible, and successfully parsed by a restore rehearsal. This offline gate validates aggregate backup metadata without reading gateway credentials or contacting a control plane.

## Portfolio Value

Adds reviewable disaster-recovery evidence for gateway-as-code state before promotion depends on an untested export.

## Validation

Run python3 -m unittest discover -s tests and confirm fresh encrypted schema-compatible backups with valid digests and restore parsing pass while stale, empty, unverified, incompatible, or malformed evidence fails.
