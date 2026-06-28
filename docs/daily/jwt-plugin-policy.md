# Add JWT plugin policy

<!-- daily-pr-task: jwt-plugin-policy -->

JWT plugin policy should define expected claims and allowed algorithms before a route is exposed. This keeps auth behavior reviewable in gateway-as-code.

Policy checks:

- required claims
- allowed algorithms
- anonymous access setting
- clock skew tolerance

## Portfolio Value

Shows gateway authentication plugins are configured with explicit claims and algorithms.

## Validation

Run the unit test and confirm weak JWT policies are rejected.
