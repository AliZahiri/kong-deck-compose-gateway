# Document decK diff before sync

<!-- daily-pr-task: deck-diff-flow -->

A production gateway workflow should run `deck gateway diff` before `deck gateway sync`. The diff gives operators a chance to review route, service, plugin, and upstream changes before applying them.

Recommended flow:

- render desired Kong state
- run decK diff against the target gateway
- review changes in CI logs or PR output
- apply sync only after the target backend is healthy

## Portfolio Value

Shows gateway-as-code discipline and avoids blind configuration pushes.

## Validation

Review the markdown file and confirm diff happens before sync.
