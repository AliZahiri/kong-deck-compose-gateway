# Add rate limiting plugin notes

<!-- daily-pr-task: rate-limiting-plugin -->

Rate limiting belongs at the gateway boundary for public or shared internal APIs. Kong can enforce request limits before traffic reaches backend services.

Plugin planning inputs:

- consumer or service-level scope
- limit period and burst tolerance
- storage policy
- response behavior when limits are exceeded
- dashboard and alerting signals

The decK template includes a service-level `rate-limiting` plugin. Operators can preview changes with `deck diff` after setting:

- `KONG_RATE_LIMIT_MINUTE`
- `KONG_RATE_LIMIT_POLICY`
- `KONG_RATE_LIMIT_FAULT_TOLERANT`

## Portfolio Value

Connects Kong gateway configuration with production traffic protection.

## Validation

Review the markdown file and confirm it describes planning inputs instead of hard-coded policy.
