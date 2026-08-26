# Add gateway plugin instance identity contract gate

<!-- daily-pr-task: gateway-plugin-instance-identity-contract-gate -->

Named Kong plugin instances make declarative diffs, ownership, and drift evidence traceable. This offline gate requires unique instance names, explicit plugin names, exactly one supported scope, and an owner tag without contacting Kong.

## Portfolio Value

Makes plugin drift and promotion reviews address stable, owned plugin instances instead of ambiguous name-and-scope combinations.

## Validation

Run python3 -m unittest discover -s tests and confirm duplicate identities, ambiguous scopes, and missing ownership fail.
