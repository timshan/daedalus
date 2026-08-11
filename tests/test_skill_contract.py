from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "daedalus"


class SkillContractTests(unittest.TestCase):
    def test_plugin_manifest_and_lifecycle_contract(self) -> None:
        manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        lifecycle = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["name"], "daedalus")
        self.assertRegex(manifest["version"], r"^[0-9]+\.[0-9]+\.[0-9]+$")
        self.assertEqual(lifecycle["plugin_path"], ".")
        self.assertTrue(lifecycle["checks"])
        self.assertEqual(
            lifecycle["discovery_roots"], ["~/.codex/skills", "~/.agents/skills"]
        )

    def test_readme_uses_plugin_installation_not_direct_skill_copy(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("codex plugin", text)
        self.assertNotIn('cp -R skills/daedalus "$HOME/.codex/skills/daedalus"', text)

    def test_skill_metadata_and_core_guards_exist(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: daedalus", text)
        self.assertIn("description:", text)
        self.assertIn("lite", text)
        self.assertIn("standard", text)
        self.assertIn("high-risk", text)
        self.assertIn("RED", text)
        self.assertIn("GREEN", text)
        self.assertIn("REFACTOR", text)
        self.assertIn("Do not create a branch or worktree", text)
        self.assertIn("untagged gate", text)

    def test_required_resources_exist_and_are_linked(self) -> None:
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        relative_paths = [
            "references/risk-and-uml.md",
            "references/sdd-schema.md",
            "references/tdd-and-verification.md",
            "scripts/init_sdd.py",
            "scripts/validate_sdd.py",
        ]
        for relative in relative_paths:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL / relative).is_file())
                self.assertIn(relative, skill_text)

    def test_openai_yaml_default_prompt_mentions_skill(self) -> None:
        text = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('$daedalus', text)

    def test_readme_discloses_forward_test_provenance(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        normalized = " ".join(text.split())

        self.assertIn("global Eureka", normalized)
        self.assertIn("64k", normalized)
        self.assertIn("96k", normalized)
        self.assertIn("not attributable to Daedalus alone", normalized)

    def test_scripts_do_not_import_network_shell_or_git_process_modules(self) -> None:
        forbidden = {"subprocess", "socket", "urllib", "http", "requests"}
        for script in (SKILL / "scripts").glob("*.py"):
            tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
            self.assertFalse(forbidden & imported, f"{script}: {forbidden & imported}")


if __name__ == "__main__":
    unittest.main()
