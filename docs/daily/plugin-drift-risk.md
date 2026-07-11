# Add plugin drift risk checks

<!-- daily-pr-task: plugin-drift-risk -->

Gateway plugin drift happens when live Kong configuration no longer matches the reviewed declarative state. Drift can weaken authentication, rate limiting, request size limits, or ownership tags without a code review trail.

Risk signals:

- plugin exists live but not in desired state
- desired plugin is missing live
- plugin configuration differs on protected routes
- drift affects auth, quota, or request limiting plugins

## Portfolio Value

Shows gateway-as-code validation beyond applying decK sync blindly.

## Validation

Run `python3 -m unittest discover -s tests` and confirm protected plugin drift is reported.
