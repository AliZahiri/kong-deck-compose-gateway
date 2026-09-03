# Add gateway regex route safety gate

<!-- daily-pr-task: gateway-regex-route-safety-gate -->

Regex route precedence alone does not prevent an expensive pattern from consuming proxy capacity. This offline gate applies conservative static checks to decK-style regex paths: an absolute pattern, bounded length, and no obvious nested unbounded quantifiers. It is a review aid, not a runtime performance guarantee, and makes no requests to Kong.

## Portfolio Value

Adds a conservative gateway-as-code review gate for an avoidable source of route-level CPU exhaustion before configuration reaches a data plane.

## Validation

Run python3 -m unittest discover -s tests and confirm bounded absolute regex routes pass while relative, nested-quantifier, oversized, malformed, and invalid-policy cases fail.
