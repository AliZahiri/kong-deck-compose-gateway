#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env}"
KONG_ADDR="${KONG_ADDR:-http://kong:8001}"

docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" --profile tools run --rm deck \
  gateway diff /deck/kong.yaml --kong-addr "$KONG_ADDR"
