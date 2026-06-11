from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


VALID_COLORS = {"blue", "green"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_active_color(active_file: Path) -> str:
    try:
        value = active_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "blue"
    return value if value in VALID_COLORS else "blue"


def validate_color(color: str) -> str:
    if color not in VALID_COLORS:
        raise ValueError("target color must be blue or green")
    return color


def render_deck_state(template: Path, output: Path, active_color: str) -> None:
    rendered = template.read_text(encoding="utf-8").replace("{{ACTIVE_COLOR}}", active_color)
    output.write_text(rendered, encoding="utf-8")


def compose_command(compose_file: Path, env_file: Path, *args: str) -> list[str]:
    return ["docker", "compose", "-f", str(compose_file), "--env-file", str(env_file), *args]


def run(command: list[str], *, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def get_container_id(compose_file: Path, env_file: Path, service: str) -> str:
    result = run(compose_command(compose_file, env_file, "ps", "-q", service), capture=True)
    container_id = result.stdout.strip()
    if not container_id:
        raise RuntimeError(f"Could not find {service} container")
    return container_id


def container_health(container_id: str) -> str:
    result = run(
        [
            "docker",
            "inspect",
            "--format",
            "{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}",
            container_id,
        ],
        capture=True,
    )
    return result.stdout.strip()


def wait_for_ready(container_id: str, service: str, attempts: int, interval: float) -> None:
    for _ in range(attempts):
        status = container_health(container_id)
        if status in {"healthy", "running"}:
            return
        if status == "unhealthy":
            run(["docker", "logs", container_id], check=False)
            raise RuntimeError(f"{service} is unhealthy")
        time.sleep(interval)
    raise TimeoutError(f"{service} did not become ready")


def switch(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else repo_root()
    compose_file = Path(os.environ.get("COMPOSE_FILE", root / "docker-compose.yml"))
    env_file = Path(os.environ.get("ENV_FILE", root / ".env"))
    active_file = Path(os.environ.get("ACTIVE_FILE", root / ".active-color"))
    stop_old = os.environ.get("STOP_OLD_AFTER_SWITCH", "true").lower() == "true"

    target_color = validate_color(args.color)
    current_color = read_active_color(active_file)
    service = f"sample-api-{target_color}"

    print(f"Starting {service}")
    run(compose_command(compose_file, env_file, "--profile", target_color, "up", "-d", service))

    container_id = get_container_id(compose_file, env_file, service)
    print(f"Waiting for {service} health check")
    wait_for_ready(container_id, service, args.health_attempts, args.health_interval)

    render_deck_state(root / "deck/kong.yaml.tpl", root / "deck/kong.yaml", target_color)

    print("Applying Kong state with decK")
    run([str(root / "scripts/deck-sync.sh")])

    active_file.write_text(f"{target_color}\n", encoding="utf-8")
    print(f"Kong route switched to {target_color}")

    if current_color != target_color and stop_old:
        run(compose_command(compose_file, env_file, "stop", f"sample-api-{current_color}"), check=False)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kong decK blue/green gateway helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    switch_parser = subparsers.add_parser("switch", help="Switch Kong traffic to a target color")
    switch_parser.add_argument("color", choices=sorted(VALID_COLORS))
    switch_parser.add_argument("--root", help="Repository root. Defaults to the current package root.")
    switch_parser.add_argument("--health-attempts", type=int, default=60)
    switch_parser.add_argument("--health-interval", type=float, default=2.0)
    switch_parser.set_defaults(func=switch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
