# Add protected plugin change approval contract

<!-- daily-pr-task: protected-plugin-change-approval -->

Updates or removals of authentication, rate-limit, request-size, and IP-restriction plugins carry more risk than ordinary gateway changes. This contract validates plugin action and scope metadata, rejects duplicate change records, and requires both a reviewer and change ticket before a protected plugin can be updated or removed. It complements decK diff safety without performing a sync.

## Portfolio Value

Introduces explicit review evidence for high-impact gateway plugin mutations while preserving deterministic pre-sync validation.

## Validation

Run `python3 -m unittest discover -s tests` and confirm approved protected changes pass while missing reviewer/ticket metadata, invalid actions/scopes, empty names, and duplicate records fail.
