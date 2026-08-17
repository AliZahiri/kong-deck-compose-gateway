# Add gateway route change window gate

<!-- daily-pr-task: gateway-route-change-window-gate -->

Gateway route changes that alter public traffic should be tied to an explicit approved window. This offline policy validates timezone-aware start and end times, a bounded window duration, and an approval reference. It does not perform a live Kong sync or bypass existing promotion checks.

## Portfolio Value

Adds a reviewable operational guardrail for externally visible route changes while preserving decK diff and promotion safety controls.

## Validation

Run `python3 -m unittest discover -s tests` and confirm approved, bounded timezone-aware windows pass while invalid timestamps and missing approvals fail.
