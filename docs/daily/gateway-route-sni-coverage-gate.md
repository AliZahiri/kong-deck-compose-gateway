# Add gateway route SNI coverage gate

<!-- daily-pr-task: gateway-route-sni-coverage-gate -->

HTTPS gateway promotion should prove that every routed hostname is covered by an active certificate SNI. This offline gate validates unique route names, explicit hosts, and exact or single-label wildcard SNI coverage without loading certificates or contacting Kong.

## Portfolio Value

Adds a deterministic TLS promotion check that connects declarative route hosts to the certificate names actually available to the gateway.

## Validation

Run python3 -m unittest discover -s tests and confirm exact and single-label wildcard coverage passes while duplicate routes, malformed hosts, and uncovered names fail.
