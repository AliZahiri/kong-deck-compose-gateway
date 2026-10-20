# Add gateway upstream host-header contract gate

<!-- daily-pr-task: gateway-upstream-host-header-gate -->

A gateway promotion can reach the intended upstream yet deliver an unsafe or ambiguous Host header. This offline gate validates explicit per-service host-header behavior: preserve-host must be a boolean, a rewritten host must be a canonical DNS name, and service names must be unique. It does not send traffic or modify Kong.

## Portfolio Value

Makes upstream Host-header handling explicit, reducing routing ambiguity and virtual-host exposure during gateway promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm explicit preserve/rewrite behavior with canonical DNS hosts passes while implicit, duplicate, or malformed hosts fail.
