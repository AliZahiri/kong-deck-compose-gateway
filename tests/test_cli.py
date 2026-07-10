import tempfile
import unittest
import json
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from kong_deck_gateway.cli import (
    deck_template_values,
    deck_script,
    read_active_color,
    promotion_plan,
    render_deck_state,
    switch,
    validate_color,
)


class KongDeckGatewayTests(unittest.TestCase):
    def test_validate_color_accepts_known_colors(self):
        self.assertEqual(validate_color("blue"), "blue")
        self.assertEqual(validate_color("green"), "green")

    def test_validate_color_rejects_unknown_color(self):
        with self.assertRaises(ValueError):
            validate_color("red")

    def test_read_active_color_defaults_to_blue(self):
        missing = Path(tempfile.gettempdir()) / "missing-kong-active-color"
        self.assertEqual(read_active_color(missing), "blue")

    def test_render_deck_state_replaces_active_color(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            template = tmp / "kong.yaml.tpl"
            output = tmp / "kong.yaml"
            template.write_text(
                (
                    "url: http://sample-api-{{ACTIVE_COLOR}}:80\n"
                    "minute: {{RATE_LIMIT_MINUTE}}\n"
                    "policy: {{RATE_LIMIT_POLICY}}\n"
                    "fault_tolerant: {{RATE_LIMIT_FAULT_TOLERANT}}\n"
                ),
                encoding="utf-8",
            )

            render_deck_state(template, output, "green")

            rendered = output.read_text(encoding="utf-8")
            self.assertIn("url: http://sample-api-green:80", rendered)
            self.assertIn("minute: 60", rendered)
            self.assertIn("policy: local", rendered)
            self.assertIn("fault_tolerant: true", rendered)

    def test_deck_template_values_validate_rate_limit_environment(self):
        values = deck_template_values(
            "green",
            {
                "KONG_RATE_LIMIT_MINUTE": "120",
                "KONG_RATE_LIMIT_POLICY": "redis",
                "KONG_RATE_LIMIT_FAULT_TOLERANT": "false",
            },
        )

        self.assertEqual(values["RATE_LIMIT_MINUTE"], "120")
        self.assertEqual(values["RATE_LIMIT_POLICY"], "redis")
        self.assertEqual(values["RATE_LIMIT_FAULT_TOLERANT"], "false")

    def test_deck_template_values_reject_invalid_rate_limit_minute(self):
        with self.assertRaises(ValueError):
            deck_template_values("green", {"KONG_RATE_LIMIT_MINUTE": "0"})

    def test_deck_script_resolves_supported_actions(self):
        root = Path("/repo")
        self.assertEqual(deck_script(root, "diff"), root / "scripts/deck-diff.sh")
        self.assertEqual(deck_script(root, "sync"), root / "scripts/deck-sync.sh")

    def test_deck_script_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            deck_script(Path("/repo"), "delete")

    def test_promotion_plan_reports_sync_and_stop_decisions(self):
        plan = promotion_plan(
            current_color="blue",
            target_color="green",
            service="sample-api-green",
            deck_state=Path("/repo/deck/kong.yaml"),
            run_diff=True,
            stop_old=True,
        )

        self.assertEqual(plan["target_color"], "green")
        self.assertEqual(plan["previous_color"], "blue")
        self.assertTrue(plan["will_run_diff"])
        self.assertFalse(plan["will_apply_sync"])
        self.assertTrue(plan["will_stop_previous_color"])

    def test_switch_dry_run_renders_diff_and_skips_sync(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "deck").mkdir()
            (root / "scripts").mkdir()
            (root / "deck/kong.yaml.tpl").write_text(
                "url: http://sample-api-{{ACTIVE_COLOR}}:80",
                encoding="utf-8",
            )
            active_file = root / ".active-color"
            active_file.write_text("blue\n", encoding="utf-8")
            args = SimpleNamespace(
                root=str(root),
                color="green",
                health_attempts=2,
                health_interval=0.1,
                skip_diff=False,
                dry_run=True,
                plan_json=False,
            )

            with (
                mock.patch("kong_deck_gateway.cli.run") as run_mock,
                mock.patch("kong_deck_gateway.cli.get_container_id", return_value="container-id"),
                mock.patch("kong_deck_gateway.cli.wait_for_ready"),
            ):
                self.assertEqual(switch(args), 0)

            commands = [call.args[0] for call in run_mock.call_args_list]
            self.assertIn([str(root / "scripts/deck-diff.sh")], commands)
            self.assertNotIn([str(root / "scripts/deck-sync.sh")], commands)
            self.assertEqual(active_file.read_text(encoding="utf-8"), "blue\n")
            self.assertIn("sample-api-green", (root / "deck/kong.yaml").read_text(encoding="utf-8"))

    def test_switch_dry_run_can_print_json_plan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "deck").mkdir()
            (root / "scripts").mkdir()
            (root / "deck/kong.yaml.tpl").write_text(
                "url: http://sample-api-{{ACTIVE_COLOR}}:80",
                encoding="utf-8",
            )
            (root / ".active-color").write_text("blue\n", encoding="utf-8")
            args = SimpleNamespace(
                root=str(root),
                color="green",
                health_attempts=2,
                health_interval=0.1,
                skip_diff=True,
                dry_run=True,
                plan_json=True,
            )

            with (
                mock.patch("kong_deck_gateway.cli.run") as run_mock,
                mock.patch("kong_deck_gateway.cli.get_container_id", return_value="container-id"),
                mock.patch("kong_deck_gateway.cli.wait_for_ready"),
            ):
                with mock.patch("sys.stdout", new_callable=__import__("io").StringIO) as stdout:
                    self.assertEqual(switch(args), 0)

            commands = [call.args[0] for call in run_mock.call_args_list]
            self.assertNotIn([str(root / "scripts/deck-sync.sh")], commands)
            output = stdout.getvalue()
            plan = json.loads(output[output.index("{") :])
            self.assertEqual(plan["target_color"], "green")


if __name__ == "__main__":
    unittest.main()
