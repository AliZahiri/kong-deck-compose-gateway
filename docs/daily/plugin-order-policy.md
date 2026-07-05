# Add gateway plugin order policy

<!-- daily-pr-task: plugin-order-policy -->

Gateway plugin order policy should ensure security plugins run before request transformation or upstream routing behavior changes.

Policy checks:

- authentication plugin is present
- rate limiting runs after authentication
- request transformer runs after authentication
- plugin list is not empty

## Portfolio Value

Shows Kong plugin chains are validated so auth and rate limits run before transformations.

## Validation

Run the unit test and confirm auth precedes request transformation plugins.
