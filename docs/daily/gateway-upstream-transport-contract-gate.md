# Add gateway upstream transport contract gate

<!-- daily-pr-task: gateway-upstream-transport-contract-gate -->

An upstream route can be syntactically valid while forwarding customer traffic with weak transport settings. This offline policy validates declared upstream protocol, TLS verification, and finite connection/read/write timeouts before a decK promotion. It does not probe upstreams or alter Kong state. Exceptions should be modelled as an explicit reviewed policy rather than silently allowing insecure transport.

## Portfolio Value

Prevents a gateway promotion from silently accepting plaintext, unverifiable TLS, or unbounded upstream timeout settings that can harm availability and traceability.

## Validation

Run python3 -m unittest discover -s tests and confirm HTTPS plus verified TLS and bounded timeouts pass while insecure transport, duplicate names, and malformed timeouts fail.
