# Add regex route priority gate

<!-- daily-pr-task: regex-route-priority-gate -->

Kong regex paths must be explicitly marked and are evaluated before prefix paths according to regex_priority. This offline gate caps regex-route count, requires each regex path to use the Kong ~ prefix and match request-path form, and rejects missing or duplicate priorities that would leave routing precedence ambiguous. It evaluates declarative route metadata only and does not contact the Admin API.

## Portfolio Value

Makes regex routing reviewable before decK sync by preventing unbounded regex growth and ambiguous precedence that can shadow intended gateway routes.

## Validation

Run `python3 -m unittest discover -s tests` and confirm explicitly prefixed regex paths with distinct priorities pass while empty or non-path regexes, duplicate or invalid priorities, excessive regex count, and invalid policy values fail.
