# Zero-Downtime Gateway Changes With Kong and decK

Kong can apply route, service, upstream, plugin, and other gateway configuration changes through the Admin API. decK makes that configuration declarative and Git-friendly.

For HTTP services, this allows a Docker Compose based blue/green deployment pattern:

1. Start the inactive app color.
2. Wait for a real health check.
3. Render the decK state to point Kong to the new color.
4. Run `deck gateway diff`.
5. Run `deck gateway sync`.
6. Confirm traffic through Kong.
7. Stop the old color after the switch.

## Why This Avoids Downtime

Kong stays running while the upstream target changes. The proxy process is not restarted for every application release. Existing client traffic continues to hit Kong while the desired gateway state is applied.

## Requirements

- Kong Admin API must be reachable only from trusted automation.
- decK state must be reviewed before production sync.
- The new backend must pass a readiness check before route promotion.
- The old and new backend versions must be compatible during the switch.
- Database migrations must be backward compatible.

## Rollback

Rollback is another decK sync pointing the route back to the previous color:

```bash
./scripts/switch-upstream.sh blue
```

or

```bash
./scripts/switch-upstream.sh green
```

## Production Hardening

- Add authentication and authorization plugins where required.
- Add request and response size limits.
- Add rate limiting for public APIs.
- Centralize Kong access logs.
- Keep declarative config in Git and apply it through CI/CD.
- Use separate workspaces or environments for staging and production.
