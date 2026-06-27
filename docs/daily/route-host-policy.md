# Add route host policy

<!-- daily-pr-task: route-host-policy -->

Gateway routes should define host and path constraints so services are not accidentally exposed through broad catch-all routes.

Policy checks:

- route has a host
- route has a path
- wildcard host requires explicit approval
- strip path behavior is documented

## Portfolio Value

Keeps gateway route exposure intentional by requiring host and path constraints.

## Validation

Run the unit test and confirm wildcard routes are rejected unless explicitly allowed.
