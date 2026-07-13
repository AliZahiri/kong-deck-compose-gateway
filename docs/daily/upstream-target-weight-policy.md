# Add upstream target weight policy

<!-- daily-pr-task: upstream-target-weight-policy -->

Kong upstream targets need predictable traffic weights during blue-green promotion. The policy validates that every target is named, weights are positive, and the intended distribution adds up to the configured total.

Validation signals:

- target host is present
- weights are positive integers
- no duplicate targets
- total traffic weight is exactly 100

## Portfolio Value

Connects decK gateway configuration to measurable blue-green traffic safety rather than only declarative sync.

## Validation

Run `python3 -m unittest discover -s tests` and confirm target weights must be complete and deterministic.
