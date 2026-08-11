#!/usr/bin/env python3
"""Exercise Daedalus's installed v1.0.x scaffold and validation capability."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import init_sdd
import validate_sdd


def fail(message: str) -> int:
    print(f"SELF_TEST_FAILED: {message}", file=sys.stderr)
    return 1


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    example = skill_root / "assets" / "examples" / "standalone-standard-complete.md"

    with tempfile.TemporaryDirectory(prefix="daedalus-self-test-") as raw:
        output = Path(raw) / "SELF-TEST-001.md"
        scaffold_result = init_sdd.main(
            [
                "--tier",
                "standard",
                "--title",
                "Standalone capability probe",
                "--change-id",
                "SELF-TEST-001",
                "--output",
                str(output),
            ]
        )
        if scaffold_result != 0 or not output.is_file():
            return fail("standard scaffold was not created")
        scaffold = output.read_text(encoding="utf-8")
        for marker in (
            "risk_tier: standard",
            "## Necessary UML",
            "## Traceability",
        ):
            if marker not in scaffold:
                return fail(f"scaffold is missing {marker!r}")

    if not example.is_file():
        return fail("bundled complete example is missing")
    tier, errors = validate_sdd.validate(example.read_text(encoding="utf-8"), "complete")
    if errors:
        detail = "; ".join(f"{error.code}: {error.message}" for error in errors)
        return fail(detail)
    if tier != "standard":
        return fail(f"unexpected example tier: {tier!r}")

    print("SELF_TEST_OK scaffold=standard complete_example=valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
