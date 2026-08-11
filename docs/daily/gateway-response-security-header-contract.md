# Add gateway response security-header contract

<!-- daily-pr-task: gateway-response-security-header-contract -->

A gateway should make browser-facing response protections explicit instead of relying on each upstream service to remember them. This offline gate validates a route header contract: HTTPS public routes require HSTS, all routes require content-type sniffing protection and a frame policy, and header names are unique case-insensitively. It does not call Kong.

## Portfolio Value

Shows that gateway-as-code covers client-facing hardening and not only upstream routing, rate limits, and authentication.

## Validation

Run `python3 -m unittest discover -s tests` and confirm protected public HTTPS routes pass while non-mapping headers, case-insensitive duplicates, missing frame or nosniff headers, and missing HSTS fail.
