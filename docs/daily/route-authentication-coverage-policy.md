# Add route authentication coverage policy

<!-- daily-pr-task: route-authentication-coverage-policy -->

Every externally reachable route should either inherit an approved authentication plugin or carry an explicit public-route exception with an owner and rationale. This policy evaluates normalized route metadata before decK sync and reports route-specific violations; it does not contain credentials or assume one authentication mechanism for all services.

## Portfolio Value

Adds an auditable pre-sync security gate that prevents unintentionally anonymous routes while supporting explicitly owned public health endpoints.

## Validation

Run `python3 -m unittest discover -s tests` and confirm approved plugins pass, unprotected routes fail, and public exceptions require ownership and rationale.
