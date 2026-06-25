# Add gateway plugin scope policy

<!-- daily-pr-task: plugin-scope-policy -->

Gateway plugins should have an intentional scope. Unscoped plugins can change global gateway behavior and should require explicit review.

Accepted scopes:

- route
- service
- consumer
- global only with explicit approval

## Portfolio Value

Shows production API gateway controls are attached deliberately to route, service, or consumer scope.

## Validation

Run the unit test and confirm unscoped plugins are rejected.
