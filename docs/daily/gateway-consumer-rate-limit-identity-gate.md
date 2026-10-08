# Add gateway consumer rate-limit identity gate

<!-- daily-pr-task: gateway-consumer-rate-limit-identity-gate -->

Rate limits only protect fairly when their identity scope is explicit. This offline gate validates that each consumer policy has a unique opaque consumer identifier, an approved identity key, positive limits, and an explicit window. It does not query Kong, process credentials, or mutate gateway configuration.

## Portfolio Value

Makes per-consumer gateway fairness reviewable by rejecting ambiguous identity scopes and invalid rate-limit declarations before promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm each consumer policy needs a unique identifier, approved identity key, positive limit, and explicit supported window.
