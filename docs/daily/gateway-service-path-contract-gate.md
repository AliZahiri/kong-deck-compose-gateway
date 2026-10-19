# Add gateway service path contract gate

<!-- daily-pr-task: gateway-service-path-contract-gate -->

Service path rewriting can unintentionally escape an intended upstream prefix or create ambiguous route behavior. This offline gate validates canonical absolute service paths, rejects dot-segments and query fragments, and requires unique service names before a decK configuration is promoted. It does not contact Kong or an upstream.

## Portfolio Value

Reduces route-rewrite ambiguity by checking that service paths are canonical, bounded to their intended prefix, and uniquely attributable before gateway promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm canonical absolute paths pass while duplicate names, dot-segments, duplicated slashes, or query fragments fail.
