# Add gateway configuration schema version gate

<!-- daily-pr-task: gateway-config-schema-version-gate -->

A decK configuration should only be promoted when its declared schema version is supported and the exact rollback snapshot is identifiable. This provider-free gate validates version compatibility, immutable config and snapshot digests, and completion of a diff review before sync.

## Portfolio Value

Makes configuration promotion safer by binding a reviewed decK diff to a supported schema and an immutable rollback snapshot.

## Validation

Run `python3 -m unittest discover -s tests` and confirm only matching supported versions, immutable artifacts, and reviewed diffs pass.
