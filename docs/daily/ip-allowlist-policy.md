# Add IP allowlist policy

<!-- daily-pr-task: ip-allowlist-policy -->

IP allowlist policy should keep sensitive routes reachable only from trusted networks. Public ranges should require explicit review before sync.

Policy checks:

- at least one CIDR
- no public catch-all without approval
- owner is declared

## Portfolio Value

Shows sensitive gateway routes can be protected by explicit source network controls.

## Validation

Run the unit test and confirm public allowlists are rejected unless approved.
