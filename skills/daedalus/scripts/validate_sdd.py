#!/usr/bin/env python3
"""Validate the structural ready or complete gate for a Daedalus SDD."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TIERS = {"lite", "standard", "high-risk"}
STATUSES = {"draft", "design-ready", "implementing", "verifying", "complete"}
PLACEHOLDER = re.compile(
    r"\b(?:TBD|TODO|pending)\b|\{\{[^}\n]+\}\}|<[^>\n]+>",
    re.IGNORECASE,
)
DESIGN_PLACEHOLDER = re.compile(
    r"\b(?:TBD|TODO)\b|\{\{[^}\n]+\}\}|<[^>\n]+>",
    re.IGNORECASE,
)
PENDING_MARKER = re.compile(r"\bpending\b", re.IGNORECASE)
REQ_DEFINITION = re.compile(
    r"^\s*-\s*(?:\*\*)?(REQ-\d{3,})(?:\*\*)?\s*(?:—|-|:)",
    re.MULTILINE,
)
AC_DEFINITION = re.compile(
    r"^\s*-\s*(?:\*\*)?(AC-\d{3,})(?:\*\*)?\s*(?:—|-|:|\()",
    re.MULTILINE,
)


@dataclass(frozen=True)
class ValidationError:
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Daedalus SDD ready or complete gate."
    )
    parser.add_argument("path", type=Path)
    parser.add_argument("--phase", choices=("ready", "complete"), default="ready")
    parser.add_argument("--json", action="store_true", dest="json_mode")
    return parser


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[ValidationError]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [
            ValidationError("E_FRONTMATTER", "document must start with YAML frontmatter")
        ]

    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        return {}, [ValidationError("E_FRONTMATTER", "frontmatter is not closed")]

    metadata: dict[str, str] = {}
    errors: list[ValidationError] = []
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(
                ValidationError("E_FRONTMATTER_LINE", f"invalid metadata line: {line}")
            )
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, errors


def normalize_heading(title: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", title.strip()).lower()


def headings(text: str) -> set[str]:
    return {
        normalize_heading(match.group(1))
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    }


def section_body(text: str, title: str) -> str:
    pattern = re.compile(
        rf"^##\s+(?:\d+(?:\.\d+)*[.)]?\s+)?{re.escape(title)}\s*$\n"
        rf"(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def without_fenced_code(text: str) -> str:
    fence = re.compile(r"^\s*(~~~|\x60{3})")
    result: list[str] = []
    active: str | None = None
    for line in text.splitlines():
        match = fence.match(line)
        if match:
            marker = match.group(1)
            active = None if active == marker else marker
            result.append("")
            continue
        result.append("" if active else line)
    return "\n".join(result)


def field_value(text: str, field: str) -> str | None:
    match = re.search(
        rf"^\s*(?:[-*]\s*)?{re.escape(field)}\s*:\s*(.*?)\s*$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def usable(value: str | None, *, pending_is_placeholder: bool = False) -> bool:
    pattern = PLACEHOLDER if pending_is_placeholder else DESIGN_PLACEHOLDER
    return bool(value and not pattern.search(value))


def add_once(errors: list[ValidationError], code: str, message: str) -> None:
    if not any(error.code == code and error.message == message for error in errors):
        errors.append(ValidationError(code, message))


def required_sections(tier: str) -> tuple[str, ...]:
    if tier == "lite":
        return (
            "current state and expected outcome",
            "requirements",
            "acceptance criteria",
            "test and recovery",
            "necessary uml",
            "changelog",
            "verification evidence",
        )
    standard = (
        "goal and non-goals",
        "current state and expected outcomes",
        "requirements",
        "acceptance criteria",
        "constraints, assumptions, and unknowns",
        "options and decision",
        "design and contracts",
        "necessary uml",
        "failure, security, and observability",
        "test portfolio and tdd slices",
        "traceability",
        "changelog",
        "verification evidence",
    )
    if tier == "high-risk":
        return standard + (
            "threat, trust, data, and abuse cases",
            "migration and reconciliation",
            "staged rollout, monitoring, and rollback",
        )
    return standard


def diagram_contexts(text: str) -> list[str]:
    """Return the local metadata text immediately associated with each diagram."""
    lines = text.splitlines(keepends=True)
    opening = re.compile(
        r"^\s*(?P<fence>`{3,}|~{3,})(?P<language>mermaid|plantuml|puml)\b",
        re.IGNORECASE,
    )
    heading = re.compile(r"^#{2,6}\s+")
    contexts: list[str] = []
    previous_end = 0
    index = 0

    while index < len(lines):
        match = opening.match(lines[index])
        if not match:
            index += 1
            continue

        context_start = previous_end
        for candidate in range(previous_end, index):
            if heading.match(lines[candidate]):
                context_start = candidate + 1
        contexts.append("".join(lines[context_start:index]))

        marker = match.group("fence")
        closing = re.compile(
            rf"^\s*{re.escape(marker[0])}{{{len(marker)},}}\s*$"
        )
        index += 1
        while index < len(lines):
            if closing.match(lines[index]):
                index += 1
                break
            index += 1
        previous_end = index

    return contexts


def validate(text: str, phase: str) -> tuple[str | None, list[ValidationError]]:
    metadata, errors = parse_frontmatter(text)
    tier = metadata.get("risk_tier")
    status = metadata.get("status")
    placeholder_text = without_fenced_code(text)

    if re.search(
        r"^\s*(?:~{3,}|`{3,})(?:plantuml|puml)\b",
        text,
        re.MULTILINE | re.IGNORECASE,
    ):
        add_once(
            errors,
            "E_UML_FORMAT",
            "all UML diagrams must use a Mermaid fence",
        )

    for key in ("change_id", "title", "risk_tier", "status"):
        if not usable(metadata.get(key)):
            add_once(errors, "E_META_REQUIRED", f"missing or placeholder metadata: {key}")
    if tier not in TIERS:
        add_once(errors, "E_META_TIER", f"risk_tier must be one of {sorted(TIERS)}")
    if status not in STATUSES:
        add_once(errors, "E_META_STATUS", f"status must be one of {sorted(STATUSES)}")

    present_headings = headings(text)
    if tier in TIERS:
        for title in required_sections(tier):
            if title not in present_headings:
                add_once(errors, "E_SECTION", f"missing section: {title}")

    changelog = section_body(text, "Changelog")
    if changelog:
        if "CHANGELOG.md" not in changelog:
            add_once(
                errors,
                "E_CHANGELOG_PATH",
                "changelog section must name repository-root CHANGELOG.md",
            )
        if "[Unreleased]" not in changelog:
            add_once(
                errors,
                "E_CHANGELOG_UNRELEASED",
                "changelog section must target [Unreleased]",
            )

    requirement_ids = REQ_DEFINITION.findall(text)
    acceptance_ids = AC_DEFINITION.findall(text)
    if not requirement_ids:
        add_once(errors, "E_ID_REQ", "at least one REQ-NNN definition is required")
    if not acceptance_ids:
        add_once(errors, "E_ID_AC", "at least one AC-NNN definition is required")
    if len(requirement_ids) != len(set(requirement_ids)):
        add_once(errors, "E_ID_REQ_DUP", "requirement IDs must be unique")
    if len(acceptance_ids) != len(set(acceptance_ids)):
        add_once(errors, "E_ID_AC_DUP", "acceptance IDs must be unique")

    for line in text.splitlines():
        if AC_DEFINITION.match(line) and not re.search(r"\bREQ-\d{3,}\b", line):
            add_once(
                errors,
                "E_AC_LINK",
                "every AC definition must link at least one REQ ID",
            )

    diagrams = diagram_contexts(text)
    decision_diagrams: list[tuple[int, str]] = []
    for index, context in enumerate(diagrams, start=1):
        role = field_value(context, "diagram_role") or "decision"
        if role == "reader-aid":
            purpose = field_value(context, "reader_aid_purpose")
            if not usable(purpose):
                add_once(
                    errors,
                    "E_READER_AID_PURPOSE",
                    f"reader-aid diagram {index} needs reader_aid_purpose",
                )
            if field_value(context, "decision_question") or field_value(context, "traces"):
                add_once(
                    errors,
                    "E_READER_AID_TRACE",
                    f"reader-aid diagram {index} must not declare decision_question or traces",
                )
            continue
        if role != "decision":
            add_once(
                errors,
                "E_DIAGRAM_ROLE",
                f"diagram {index} role must be decision or reader-aid",
            )
            continue
        decision_diagrams.append((index, context))

    if decision_diagrams:
        for index, context in decision_diagrams:
            decision = field_value(context, "decision_question")
            traces = field_value(context, "traces")
            if not usable(decision):
                add_once(
                    errors,
                    "E_DIAGRAM_DECISION",
                    f"diagram {index} needs a non-placeholder decision_question",
                )
            if not (
                usable(traces)
                and re.search(r"\bREQ-\d{3,}\b", traces or "")
                and re.search(r"\bAC-\d{3,}\b", traces or "")
            ):
                add_once(
                    errors,
                    "E_DIAGRAM_TRACE",
                    f"diagram {index} traces must include REQ and AC IDs",
                )
    else:
        rationale = field_value(text, "no_diagram_rationale")
        if not usable(rationale):
            add_once(
                errors,
                "E_DIAGRAM_RATIONALE",
                "provide a diagram or a non-placeholder no_diagram_rationale",
            )

    if tier in {"standard", "high-risk"}:
        trace = section_body(text, "Traceability")
        for requirement_id in sorted(set(requirement_ids)):
            if requirement_id not in trace:
                add_once(
                    errors,
                    "E_TRACE_REQ",
                    f"traceability does not cover {requirement_id}",
                )
        for acceptance_id in sorted(set(acceptance_ids)):
            if acceptance_id not in trace:
                add_once(
                    errors,
                    "E_TRACE_AC",
                    f"traceability does not cover {acceptance_id}",
                )

    if phase == "ready" and DESIGN_PLACEHOLDER.search(placeholder_text):
        add_once(
            errors,
            "E_READY_PLACEHOLDER",
            "ready document still contains TBD, TODO, or template markers",
        )

    if phase == "complete":
        if status != "complete":
            add_once(
                errors,
                "E_COMPLETE_STATUS",
                "complete validation requires status: complete",
            )
        completion_titles = (
            "test and recovery",
            "test portfolio and tdd slices",
            "traceability",
            "rollout, rollback, and remaining risks",
            "staged rollout, monitoring, and rollback",
            "changelog",
            "verification evidence",
        )
        completion_text = without_fenced_code(
            "\n".join(section_body(text, title) for title in completion_titles)
        )
        if DESIGN_PLACEHOLDER.search(placeholder_text) or PENDING_MARKER.search(
            completion_text
        ):
            add_once(
                errors,
                "E_COMPLETE_PLACEHOLDER",
                "complete document still contains a design placeholder or pending completion marker",
            )
        evidence_fields = [
            "RED evidence",
            "GREEN evidence",
            "Refactor or exception",
            "Fresh verification",
            "Changelog evidence",
            "Remaining risks",
        ]
        if tier == "high-risk":
            evidence_fields.append("Security／performance／migration evidence")
        for field in evidence_fields:
            if not usable(field_value(text, field), pending_is_placeholder=True):
                add_once(
                    errors,
                    "E_COMPLETE_EVIDENCE",
                    f"missing non-placeholder completion field: {field}",
                )

    return tier, errors


def emit(
    *, tier: str | None, phase: str, errors: list[ValidationError], json_mode: bool
) -> None:
    valid = not errors
    if json_mode:
        print(
            json.dumps(
                {
                    "valid": valid,
                    "phase": phase,
                    "tier": tier,
                    "errors": [error.as_dict() for error in errors],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return

    if valid:
        print(f"VALID tier={tier} phase={phase}")
        return
    print(f"INVALID tier={tier} phase={phase}")
    for error in errors:
        print(f"{error.code}: {error.message}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        if args.json_mode:
            print(
                json.dumps(
                    {
                        "valid": False,
                        "phase": args.phase,
                        "tier": None,
                        "errors": [
                            {"code": "E_INPUT_READ", "message": f"{args.path}: {exc}"}
                        ],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(f"E_INPUT_READ: {args.path}: {exc}", file=sys.stderr)
        return 2

    tier, errors = validate(text, args.phase)
    emit(tier=tier, phase=args.phase, errors=errors, json_mode=args.json_mode)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
