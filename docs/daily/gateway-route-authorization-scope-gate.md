# Add gateway route authorization scope gate

<!-- daily-pr-task: gateway-route-authorization-scope-gate -->

Authentication proves who a caller is but does not limit what an authenticated identity may do. This offline decK preflight requires sensitive route paths to declare authentication and explicit, non-wildcard authorization scopes. Public routes remain possible when they do not match a configured sensitive prefix.

## Portfolio Value

Adds an authorization boundary after authentication so sensitive gateway routes cannot be promoted with identity checks but no least-privilege scope contract.

## Validation

Run python3 -m unittest discover -s tests and confirm sensitive routes require authentication plus unique explicit scopes while public routes remain valid and wildcard scopes fail.
