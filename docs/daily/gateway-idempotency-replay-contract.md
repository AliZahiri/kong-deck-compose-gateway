# Add gateway idempotency replay contract

<!-- daily-pr-task: gateway-idempotency-replay-contract -->

Retries for mutating API requests can duplicate payments, writes, or provisioning work unless the gateway and upstream share a durable idempotency contract. This offline gate validates the configuration evidence for unsafe-method routes: a standard key header, bounded key retention, route-and-consumer scoping, a request-body fingerprint, explicit replay behavior, and a conflict response for key reuse with different payloads. It does not configure Kong or process traffic.

## Portfolio Value

Extends gateway retry safety into a concrete replay contract, reducing duplicate side effects for real write endpoints without making unsupported runtime claims.

## Validation

Run `python3 -m unittest discover -s tests` and confirm a complete POST replay contract passes while empty routes, duplicate names, invalid methods, non-standard headers, unbounded retention, weak scope, missing fingerprints or replay behavior, invalid conflict status, and invalid limits fail.
