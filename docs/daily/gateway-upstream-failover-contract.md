# Add gateway upstream failover contract

<!-- daily-pr-task: gateway-upstream-failover-contract -->

Upstream failover needs a declared target set and health policy before traffic is promoted. This offline gate validates unique addressable targets, positive weights totaling 100, at least two targets for a failover-enabled upstream, and bounded retry behavior. It does not contact Kong or upstreams.

## Portfolio Value

Adds an explicit, testable upstream failover policy to gateway-as-code without claiming that a static configuration alone guarantees availability.

## Validation

Run `python3 -m unittest discover -s tests` and confirm balanced targets pass while empty, malformed, duplicate, unbalanced, single-target failover, and unbounded retry configurations fail.
