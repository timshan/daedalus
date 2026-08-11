#!/usr/bin/env python3
"""Create a tier-specific Daedalus SDD without overwriting by default."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


TIERS = ("lite", "standard", "high-risk")
CHANGE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a risk-tiered Daedalus Software Design Document."
    )
    parser.add_argument("--tier", required=True, choices=TIERS)
    parser.add_argument("--title", required=True)
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Explicitly overwrite an existing output file.",
    )
    return parser


def fail(code: str, message: str) -> int:
    print(f"{code}: {message}", file=sys.stderr)
    return 2


def render(template: str, *, tier: str, title: str, change_id: str) -> str:
    replacements = {
        "{{CHANGE_ID}}": change_id,
        "{{TITLE}}": title,
        "{{TIER}}": tier,
        "{{DATE}}": date.today().isoformat(),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    title = args.title.strip()
    change_id = args.change_id.strip()
    output = args.output.expanduser()

    if not title or "\n" in title or "\r" in title:
        return fail("E_TITLE_INVALID", "title must be one non-empty line")
    if not CHANGE_ID.fullmatch(change_id):
        return fail(
            "E_CHANGE_ID_INVALID",
            "change-id must be 2-64 letters, digits, dots, underscores, or hyphens",
        )
    if output.exists() and not args.force:
        return fail("E_OUTPUT_EXISTS", f"refusing to overwrite {output}")

    skill_root = Path(__file__).resolve().parents[1]
    template_path = skill_root / "assets" / "templates" / f"sdd-{args.tier}.md"
    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        return fail("E_TEMPLATE_READ", f"{template_path}: {exc}")

    content = render(
        template,
        tier=args.tier,
        title=title,
        change_id=change_id,
    )

    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        mode = "w" if args.force else "x"
        with output.open(mode, encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError:
        return fail("E_OUTPUT_EXISTS", f"refusing to overwrite {output}")
    except OSError as exc:
        return fail("E_OUTPUT_WRITE", f"{output}: {exc}")

    print(f"CREATED={output}")
    print(f"TIER={args.tier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
