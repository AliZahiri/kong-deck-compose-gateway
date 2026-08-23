# Add gateway decK diff risk budget gate

<!-- daily-pr-task: gateway-deck-diff-risk-budget-gate -->

A decK diff should be assessed against an explicit blast-radius budget before sync. This offline gate validates non-negative change counts, deletion and total-change limits, and approval evidence for protected changes.

## Portfolio Value

Turns decK diff review into a deterministic blast-radius control that blocks unexpectedly broad, destructive, or unapproved gateway promotions.

## Validation

Run python3 -m unittest discover -s tests and confirm excessive, destructive, malformed, or protected unapproved changes fail.
