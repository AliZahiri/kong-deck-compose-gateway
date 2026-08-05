# Add gateway workspace contract gate

<!-- daily-pr-task: gateway-workspace-contract-gate -->

Shared Kong control planes need a clear boundary between staging and production resources. This offline gate validates supplied declarative resource metadata: every resource must target the intended workspace, carry exactly one matching env tag, and use a unique resource-type/name identity. It does not query workspaces or sync configuration.

## Portfolio Value

Prevents a reviewed gateway resource from silently targeting the wrong workspace or carrying ambiguous environment ownership before decK promotion.

## Validation

Run `python3 -m unittest discover -s tests` and confirm unique resources with a matching workspace and env tag pass while empty input, cross-environment resources, duplicate identities, ambiguous tags, and invalid policy values fail.
