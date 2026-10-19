# Add gateway upstream port policy gate

<!-- daily-pr-task: gateway-upstream-port-policy-gate -->

TLS verification alone does not make an upstream endpoint intentional. This offline gate validates declared upstream names, allowed TLS service ports, and a unique endpoint assignment before promotion. The default policy permits standard HTTPS and an explicit alternate TLS port; broader ports require a reviewed policy override. It does not resolve DNS or contact upstreams.

## Portfolio Value

Makes upstream service-port exposure explicit and reviewable, complementing TLS verification with a least-privilege network endpoint policy.

## Validation

Run python3 -m unittest discover -s tests and confirm allowed unique TLS endpoints pass while plaintext ports, duplicates, and malformed policies fail.
