# Add forwarded header trust gate

<!-- daily-pr-task: forwarded-header-trust-gate -->

Client-supplied forwarding headers can spoof source identity and scheme unless Kong trusts only explicit proxy networks and replaces untrusted values at the edge. This offline gate validates canonical proxy CIDRs, unique service policies, incoming header sanitization, forwarded-header replacement, and request-ID generation before gateway promotion.

## Portfolio Value

Protects gateway auditability and IP-based controls from spoofed forwarding metadata by requiring explicit proxy trust and deterministic edge sanitization.

## Validation

Run `python3 -m unittest discover -s tests` and confirm canonical trusted networks with sanitized headers pass while empty or duplicate CIDRs, noncanonical networks, empty evidence, duplicate services, and disabled replacement controls fail.
