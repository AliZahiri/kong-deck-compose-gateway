# Add route method allowlist policy

<!-- daily-pr-task: route-method-allowlist-policy -->

A production gateway route should declare the HTTP methods it intends to expose. An allowlist reduces accidental method exposure and gives API reviews a concise, testable contract.

## Portfolio Value

Shows a concrete API gateway contract that reduces accidental endpoint exposure.

## Validation

Run `python3 -m unittest discover -s tests` and confirm unsupported HTTP methods fail validation.
