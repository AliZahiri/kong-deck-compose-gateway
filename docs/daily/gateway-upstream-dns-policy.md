# Add gateway upstream DNS policy gate

<!-- daily-pr-task: gateway-upstream-dns-policy -->

Declarative gateway state should make upstream name resolution predictable. This offline policy gate validates DNS resolver intent for each upstream: an HTTPS-safe hostname, positive resolver timeout, bounded cache TTL, and an explicit resolver address. It prevents accidental use of loopback, wildcard, or unbounded stale name-resolution settings before route promotion.

## Portfolio Value

Broadens gateway-as-code safety to upstream resolution, a frequent source of brownouts and stale routing during service promotion.

## Validation

Run `python3 -m unittest discover -s tests` and confirm a bounded non-loopback DNS policy passes while invalid names, loopback or malformed resolvers, invalid timeout or TTL values, and invalid policy limits fail.
