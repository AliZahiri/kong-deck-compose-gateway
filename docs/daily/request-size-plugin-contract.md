# Add request size plugin contract

<!-- daily-pr-task: request-size-plugin-contract -->

Routes accepting request bodies should declare a bounded request-size-limiting plugin configuration. The validator requires a positive megabyte limit within a platform maximum and rejects body-capable routes with no plugin, while read-only routes remain unaffected.

## Portfolio Value

Turns request-size documentation into a testable route contract that reduces gateway memory and abuse risk before decK sync.

## Validation

Run `python3 -m unittest discover -s tests` and confirm body methods require positive bounded limits while read-only routes pass.
