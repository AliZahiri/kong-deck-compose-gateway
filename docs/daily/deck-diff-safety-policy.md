# Add decK diff safety policy

<!-- daily-pr-task: deck-diff-safety-policy -->

decK diff safety policy should classify gateway changes before sync. Deletes and plugin removals should require explicit approval during production promotion.

Policy checks:

- diff contains only known action types
- destructive actions are approved
- reviewer is declared
- target environment is declared

## Portfolio Value

Shows gateway changes are reviewed for destructive drift before sync.

## Validation

Run the unit test and confirm destructive diff actions require approval.
