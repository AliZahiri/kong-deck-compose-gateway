# Add service owner tag policy

<!-- daily-pr-task: service-owner-tag-policy -->

Service owner tag policy should keep Kong entities traceable to an owner and runbook. This helps incident response when route behavior changes.

Required tags:

- owner
- environment
- runbook
- criticality

## Portfolio Value

Shows gateway-as-code keeps ownership metadata for routes and services.

## Validation

Run the unit test and confirm service owner, environment, and runbook tags are required.
