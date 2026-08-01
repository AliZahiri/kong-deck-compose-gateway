# Add consumer credential expiry gate

<!-- daily-pr-task: consumer-credential-expiry-gate -->

Gateway authentication policy is incomplete when consumer credentials can remain valid indefinitely or expire without a rotation window. This metadata-only gate validates unique credential identities, timezone-aware issuance and expiry, a bounded lifetime, and minimum remaining rotation time. It never reads or stores credential material.

## Portfolio Value

Adds auditable credential-rotation readiness without exposing secrets by enforcing bounded lifetimes, unique identities, and a usable pre-expiry rotation window.

## Validation

Run `python3 -m unittest discover -s tests` and confirm bounded unique credentials pass while duplicate identities, naive or invalid timestamps, excessive lifetimes, short rotation windows, and invalid policies fail.
