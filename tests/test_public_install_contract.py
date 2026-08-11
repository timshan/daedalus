from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
SELF_TEST = ROOT / "skills" / "daedalus" / "scripts" / "self_test.py"
COMPLETE_EXAMPLE = (
    ROOT
    / "skills"
    / "daedalus"
    / "assets"
    / "examples"
    / "standalone-standard-complete.md"
)


def parse_version(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split(".")[:3])


def identity_errors(marketplace: dict[str, object], manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        return ["marketplace must contain exactly one Plugin"]

    plugin = plugins[0]
    if not isinstance(plugin, dict):
        return ["marketplace Plugin entry must be an object"]

    identities = (marketplace.get("name"), plugin.get("name"), manifest.get("name"))
    if identities != ("daedalus", "daedalus", "daedalus"):
        errors.append(f"identity mismatch: {identities!r}")
    if plugin.get("source") != {"source": "local", "path": "."}:
        errors.append(f"source mismatch: {plugin.get('source')!r}")
    return errors


class PublicInstallContractTests(unittest.TestCase):
    def test_marketplace_and_plugin_identity_are_cross_consistent(self) -> None:
        self.assertTrue(MARKETPLACE.is_file(), "public marketplace manifest is missing")
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(identity_errors(marketplace, manifest), [])
        self.assertGreaterEqual(parse_version(manifest["version"]), (1, 0, 1))

    def test_readme_exposes_the_exact_public_install_interface(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        commands = "\n".join(
            (
                "codex plugin marketplace add timshan/daedalus --ref main",
                "codex plugin add daedalus@daedalus",
            )
        )

        self.assertIn(commands, readme)
        self.assertEqual(readme.count("codex plugin marketplace add"), 1)
        self.assertEqual(readme.count("codex plugin add"), 1)

    def test_lifecycle_has_an_exact_standalone_package_boundary(self) -> None:
        lifecycle = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))

        self.assertEqual(
            lifecycle.get("package_paths"),
            [".codex-plugin", "LICENSE", "skills"],
        )
        self.assertEqual(
            lifecycle.get("independence", {}).get("standalone_checks"),
            [["python3", "skills/daedalus/scripts/self_test.py"]],
        )

    def test_bundled_self_test_exercises_v1_0_core_capabilities(self) -> None:
        self.assertTrue(SELF_TEST.is_file(), "installed-payload self-test is missing")
        self.assertTrue(COMPLETE_EXAMPLE.is_file(), "complete self-test example is missing")

        result = subprocess.run(
            [sys.executable, str(SELF_TEST)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "SELF_TEST_OK scaffold=standard complete_example=valid",
            result.stdout,
        )

    def test_changelog_records_patch_and_baseline(self) -> None:
        changelog = ROOT / "CHANGELOG.md"
        self.assertTrue(changelog.is_file(), "repository changelog is missing")
        text = changelog.read_text(encoding="utf-8")

        self.assertIn("## [1.0.1] - 2026-08-11", text)
        self.assertIn("## [1.0.0] - 2026-08-11", text)
        self.assertIn("public installation", text.lower())

    def test_public_markdown_has_no_author_local_install_dependency(self) -> None:
        paths = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
        changelog = ROOT / "CHANGELOG.md"
        if changelog.is_file():
            paths.append(changelog)
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        forbidden = (
            "/mnt/d/project/",
            "D:\\project\\",
            "skill-" + "lifecycle-control",
            "skill-" + "formal",
        )

        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)

    def test_plausible_wrong_cross_field_identity_is_rejected(self) -> None:
        marketplace = {
            "name": "daedalus",
            "plugins": [
                {
                    "name": "formal-daedalus",
                    "source": {"source": "local", "path": "."},
                }
            ],
        }
        manifest = {"name": "daedalus", "version": "1.0.1"}

        self.assertIn("identity mismatch", identity_errors(marketplace, manifest)[0])


if __name__ == "__main__":
    unittest.main()
