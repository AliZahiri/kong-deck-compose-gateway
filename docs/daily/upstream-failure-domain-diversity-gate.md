# Add upstream failure-domain diversity gate

<!-- daily-pr-task: upstream-failure-domain-diversity-gate -->

Healthy Kong targets should not all share one host or failure domain. This offline gate validates declarative target evidence, unique target identities and addresses, positive weights, explicit health, and a policy-defined minimum number of represented failure domains before promotion.

## Portfolio Value

Extends target weight and health checks with failure-domain evidence so a nominally healthy upstream is not silently concentrated on one infrastructure boundary.

## Validation

Run python3 -m unittest discover -s tests and confirm empty targets, duplicate IDs or addresses, invalid weights, unhealthy targets, missing domains, insufficient domain coverage, and invalid policy fail.
