# Add gateway route preflight gate

<!-- daily-pr-task: gateway-route-preflight-gate -->

Route promotion should evaluate authentication coverage and request-body limits together rather than as disconnected checks. This aggregate preflight reports route-specific violations before decK sync and keeps public exceptions explicit.

## Portfolio Value

Converts route security policies into a single pre-sync decision suitable for promotion automation.

## Validation

Run `python3 -m unittest discover -s tests` and confirm authentication and payload-size failures are aggregated per route.
