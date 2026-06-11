# Kong decK Docker Compose Gateway

Kong Gateway platform kit using Docker Compose and decK for declarative configuration.

The deployment pattern supports zero-downtime traffic switching for HTTP services by starting the inactive app color, waiting for health checks, applying the new Kong state with decK, and switching traffic without restarting Kong.

## What This Shows

- Kong Gateway with PostgreSQL in Docker Compose
- decK-based gateway configuration
- Blue/green upstream switching
- Health-check-gated route promotion
- Local development and production-oriented notes
- Gateway configuration as code

## Architecture

```text
Client
  |
  v
Kong Proxy
  |
  v
Kong Service -> active upstream color
  |
  +--> sample-api-blue
  +--> sample-api-green

decK syncs desired gateway state through the Kong Admin API.
```

## Quick Start

```bash
cp .env.example .env
docker compose --env-file .env up -d kong-database
docker compose --env-file .env run --rm kong-migrations
docker compose --env-file .env --profile blue up -d kong sample-api-blue
./scripts/deck-sync.sh
curl http://localhost:8000/api
```

Switch traffic to green:

```bash
./scripts/switch-upstream.sh green
```

Switch back to blue:

```bash
./scripts/switch-upstream.sh blue
```

## Repository Structure

```text
.
├── deck/
│   ├── kong.yaml
│   └── kong.yaml.tpl
├── docs/
│   └── zero-downtime-kong-deck.md
├── scripts/
│   ├── deck-diff.sh
│   ├── deck-sync.sh
│   └── switch-upstream.sh
└── docker-compose.yml
```

## Production Notes

- Protect Kong Admin API. Do not expose it publicly.
- Use decK diff before sync in controlled environments.
- Use health checks before route promotion.
- Keep gateway state in Git and apply through CI/CD.
- Use backward-compatible backend changes when switching traffic.
- Separate local bootstrap secrets from production secrets.

See [docs/zero-downtime-kong-deck.md](docs/zero-downtime-kong-deck.md).
