from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "daedalus" / "scripts" / "init_sdd.py"


class InitSddCliTests(unittest.TestCase):
    def run_cli(
        self,
        output: Path,
        *,
        tier: str = "lite",
        title: str = "Fix cache key",
        change_id: str = "CACHE-001",
        force: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "--tier",
            tier,
            "--title",
            title,
            "--change-id",
            change_id,
            "--output",
            str(output),
        ]
        if force:
            command.append("--force")
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_lite_scaffold_is_proportional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cache-fix.md"
            result = self.run_cli(output)

            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("change_id: CACHE-001", text)
            self.assertIn("title: Fix cache key", text)
            self.assertIn("risk_tier: lite", text)
            self.assertIn("## Current state and expected outcome", text)
            self.assertIn("## Acceptance criteria", text)
            self.assertIn("## Test and recovery", text)
            self.assertIn("no_diagram_rationale:", text)
            self.assertNotIn("## Deployment architecture", text)

    def test_standard_scaffold_contains_design_and_traceability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "integration.md"
            result = self.run_cli(
                output,
                tier="standard",
                title="Add billing adapter",
                change_id="BILLING-002",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("risk_tier: standard", text)
            self.assertIn("## Design and contracts", text)
            self.assertIn("## Necessary UML", text)
            self.assertIn("required, optional, or omit", text)
            self.assertIn("no_diagram_rationale:", text)
            self.assertNotIn("sequenceDiagram", text)
            self.assertIn("## Test portfolio and TDD slices", text)
            self.assertIn("## Traceability", text)
            self.assertIn("## Changelog", text)

    def test_existing_output_is_not_overwritten_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "existing.md"
            output.write_text("KEEP ME\n", encoding="utf-8")

            result = self.run_cli(output)

            self.assertEqual(result.returncode, 2)
            self.assertIn("E_OUTPUT_EXISTS", result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "KEEP ME\n")

    def test_force_explicitly_overwrites_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "existing.md"
            output.write_text("old\n", encoding="utf-8")

            result = self.run_cli(output, force=True)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("change_id: CACHE-001", output.read_text(encoding="utf-8"))

    def test_invalid_tier_is_rejected_by_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "invalid.md"
            result = self.run_cli(output, tier="enterprise")

            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
