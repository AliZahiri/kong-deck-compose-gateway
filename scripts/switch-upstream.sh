#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env}"
ACTIVE_FILE="${ACTIVE_FILE:-$ROOT_DIR/.active-color}"
STOP_OLD_AFTER_SWITCH="${STOP_OLD_AFTER_SWITCH:-true}"

target_color="${1:-}"
if [[ "$target_color" != "blue" && "$target_color" != "green" ]]; then
  echo "usage: $0 blue|green"
  exit 1
fi

current_color="$(cat "$ACTIVE_FILE" 2>/dev/null || echo blue)"

echo "Starting sample-api-$target_color"
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" --profile "$target_color" up -d "sample-api-$target_color"

container_id="$(docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps -q "sample-api-$target_color")"
if [[ -z "$container_id" ]]; then
  echo "Could not find sample-api-$target_color container"
  exit 1
fi

echo "Waiting for sample-api-$target_color health check"
for _ in $(seq 1 60); do
  status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}' "$container_id")"
  if [[ "$status" == "healthy" || "$status" == "running" ]]; then
    break
  fi
  if [[ "$status" == "unhealthy" ]]; then
    docker logs "$container_id" || true
    echo "sample-api-$target_color is unhealthy"
    exit 1
  fi
  sleep 2
done

sed "s/{{ACTIVE_COLOR}}/$target_color/g" "$ROOT_DIR/deck/kong.yaml.tpl" > "$ROOT_DIR/deck/kong.yaml"

echo "Applying Kong state with decK"
"$ROOT_DIR/scripts/deck-sync.sh"

echo "$target_color" > "$ACTIVE_FILE"
echo "Kong route switched to $target_color"

if [[ "$current_color" != "$target_color" && "$STOP_OLD_AFTER_SWITCH" == "true" ]]; then
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" stop "sample-api-$current_color" || true
fi
