# Add decK change summary helper

<!-- daily-pr-task: deck-change-summary -->

decK diff output should be summarized for reviewers so route, service, and plugin changes are visible before sync. A small summary helper can make CI output easier to scan.

Summary fields:

- routes changed
- services changed
- plugins changed
- upstreams changed

## Portfolio Value

Makes gateway-as-code changes easier to review before sync.

## Validation

Run the unit test and confirm route, service, and plugin counts are summarized.
