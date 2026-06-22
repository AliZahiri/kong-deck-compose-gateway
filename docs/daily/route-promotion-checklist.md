# Add route promotion checklist

<!-- daily-pr-task: route-promotion-checklist -->

Route promotion should happen only after the target backend is running and healthy.

Checklist:

- start inactive backend color
- wait for container health
- render decK state to target color
- run decK diff
- sync gateway state
- verify traffic through Kong proxy
- stop old color only after verification

## Portfolio Value

Makes the zero-downtime gateway story reviewable and repeatable.

## Validation

Review the markdown file and confirm it preserves the old backend until after verification.
