# Add gateway cache policy contract

<!-- daily-pr-task: gateway-cache-policy-contract -->

Caching at an API gateway must be explicit so private or mutating traffic is never served from a shared cache. This offline gate validates route cache contracts: only GET and HEAD methods may be cached, private routes must be no-store, cacheable routes need a bounded TTL, and authenticated routes may not use shared caching. It does not contact Kong.

## Portfolio Value

Adds a defensible cache-control policy to gateway-as-code, covering a common source of privacy and correctness regressions.

## Validation

Run `python3 -m unittest discover -s tests` and confirm bounded public GET caching passes while empty methods, mutating cached methods, private non-no-store responses, shared authenticated caching, invalid TTLs, and invalid policy limits fail.
