# Add upstream failover capacity gate

<!-- daily-pr-task: upstream-failover-capacity-gate -->

A valid Kong upstream can still be unsafe to promote when all healthy weight is concentrated in one failure domain or cannot satisfy the required serving capacity. This offline gate validates unique target identities, zones, health flags, and non-negative weights, then requires minimum healthy target count, aggregate weight, and zone diversity before promotion.

## Portfolio Value

Prevents gateway promotion with nominally healthy but under-capacity or single-zone upstreams by enforcing deterministic serving-weight and failure-domain evidence.

## Validation

Run `python3 -m unittest discover -s tests` and confirm diversified healthy capacity passes while empty targets, invalid metadata, duplicate identities, insufficient count/weight/zones, and invalid policy values fail.
