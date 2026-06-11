import tempfile
import unittest
from pathlib import Path

from kong_deck_gateway.cli import read_active_color, render_deck_state, validate_color


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
            template.write_text("url: http://sample-api-{{ACTIVE_COLOR}}:80", encoding="utf-8")

            render_deck_state(template, output, "green")

            self.assertEqual(output.read_text(encoding="utf-8"), "url: http://sample-api-green:80")


if __name__ == "__main__":
    unittest.main()
