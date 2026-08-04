# Add Kong Admin API exposure gate

<!-- daily-pr-task: admin-api-exposure-gate -->

Documenting Admin API security is not enough to prevent an unsafe listener from reaching a data-plane network. This offline gate validates unique listeners and permits remote exposure only when TLS, client authentication, RBAC, and control-plane isolation are all explicitly evidenced. It evaluates configuration metadata and never contacts Kong.

## Portfolio Value

Turns Admin API isolation into a testable gateway policy by distinguishing safe loopback listeners from remote listeners that require layered transport, identity, authorization, and network controls.

## Validation

Run `python3 -m unittest discover -s tests` and confirm loopback and fully hardened control-plane listeners pass while empty input, invalid or duplicate addresses, and unprotected remote exposure fail.
