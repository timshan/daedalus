from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "daedalus"


class IndependenceContractTests(unittest.TestCase):
    def test_public_marketplace_points_to_the_root_plugin(self) -> None:
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(marketplace["name"], "daedalus")
        self.assertEqual(len(marketplace["plugins"]), 1)
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], "daedalus")
        self.assertEqual(plugin["source"], {"source": "local", "path": "."})

    def test_package_is_an_explicit_runtime_allowlist(self) -> None:
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))

        self.assertEqual(
            config["package_paths"],
            [".codex-plugin", "LICENSE", "skills"],
        )

    def test_installed_payload_declares_a_behavioral_self_test(self) -> None:
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        checks = config["independence"]["standalone_checks"]

        self.assertEqual(
            checks,
            [["python3", "skills/daedalus/scripts/self_test.py"]],
        )
        self.assertTrue((SKILL / "scripts" / "self_test.py").is_file())
        self.assertTrue(
            (SKILL / "assets" / "examples" / "standalone-standard-complete.md").is_file()
        )

    def test_packaged_skill_contains_no_explicit_external_skill_provenance(self) -> None:
        forbidden = (
            "skill-" + "lifecycle-control",
            "global " + "Eureka",
            "w5:" + "p3",
            "Claude " + "Code",
            "Spec " + "Kit",
            "Super" + "powers",
        )
        text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in SKILL.rglob("*")
            if path.is_file()
        )

        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, text)

    def test_skill_defines_the_complete_living_workflow(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        for stage in (
            "FRAME",
            "MODEL",
            "BIND",
            "PROVE",
            "BUILD",
            "RECONCILE",
            "SEAL",
        ):
            with self.subTest(stage=stage):
                self.assertIn(stage, text)
        self.assertIn("return to MODEL", text)
        self.assertNotIn("Do not create a branch or worktree", text)

    def test_public_documentation_has_no_external_local_install_or_dirty_benchmark(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        current_docs = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in (ROOT / "docs").rglob("*.md")
        )
        combined = readme + "\n" + current_docs

        forbidden = (
            "/mnt/d/project/" + "skill-lifecycle-control",
            "D:\\project\\" + "skill-lifecycle-control",
            "/path/to/" + "skill-creator",
            "global " + "Eureka",
            "64" + "k",
            "96" + "k",
        )
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)


if __name__ == "__main__":
    unittest.main()
