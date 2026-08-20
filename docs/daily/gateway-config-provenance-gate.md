# Add gateway configuration provenance gate

<!-- daily-pr-task: gateway-config-provenance-gate -->

Gateway promotion should be tied to an immutable reviewed configuration, rather than an untraceable local file. This offline gate requires a SHA-256 digest, a named reviewer, an allowed target environment, and explicit decK diff review evidence. It validates declared promotion metadata and never connects to Kong.

## Portfolio Value

Connects decK promotion to a reviewable immutable configuration artifact and an explicit diff review.

## Validation

Run `python3 -m unittest discover -s tests` and confirm invalid digests, reviewers, environments, or missing diffs fail.
