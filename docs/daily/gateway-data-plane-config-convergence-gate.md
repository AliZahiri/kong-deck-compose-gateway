# Add gateway data-plane config convergence gate

<!-- daily-pr-task: gateway-data-plane-config-convergence-gate -->

A successful decK sync is not sufficient evidence that every data-plane node serves the promoted configuration. This offline gate compares each ready node with the expected configuration digest and requires fresh timezone-aware observations within a bounded convergence interval.

## Portfolio Value

Extends gateway promotion safety beyond control-plane sync by requiring digest-level convergence evidence from every observed data-plane node.

## Validation

Run python3 -m unittest discover -s tests and confirm ready matching fresh nodes pass while missing nodes, duplicates, stale or naive observations, unready nodes, digest mismatch, and invalid policy fail.
