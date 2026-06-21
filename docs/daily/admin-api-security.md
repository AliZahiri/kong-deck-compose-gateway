# Document Kong Admin API security

<!-- daily-pr-task: admin-api-security -->

The Kong Admin API should never be exposed as a public endpoint. Automation should reach it through trusted networks or CI runners with controlled access.

Baseline controls:

- bind Admin API to localhost or private network
- restrict access by firewall or network policy
- avoid sharing admin credentials in repository files
- apply decK changes from trusted automation only

## Portfolio Value

Highlights a key production security boundary for Kong operations.

## Validation

Review the markdown file and confirm it does not suggest public Admin API exposure.
