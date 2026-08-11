# SDD schema and gates

Software Design Document means the living artifact that connects intent, design, tests, code, and
fresh evidence. It is not a document-count target.

## Status flow

Use draft → design-ready → implementing → verifying → complete. FRAME／MODEL produce design-ready;
BIND／PROVE enter implementing; BUILD reaches verifying; RECONCILE returns to MODEL when tests,
code, or review reveal a design gap; SEAL reaches complete.

## Common metadata

Every tier records change_id, title, risk_tier, status, owner when known, affected paths,
tier_rationale, and recovery. Use stable REQ-NNN and AC-NNN identifiers.

## Tier-specific content

### lite

Keep one artifact, normally one page:

- current state and observable expected outcome;
- goal／non-goal when ambiguity exists;
- at least one REQ and linked AC;
- focused regression or behavior test;
- no-diagram rationale unless a diagram answers a real question;
- actual diff, fresh verification, remaining risk, and recovery.
- repository-root `CHANGELOG.md` plan and completed `[Unreleased]` evidence.

### standard

Include:

1. goal and non-goals;
2. current state and measurable expected outcomes;
3. requirements and acceptance criteria;
4. constraints, assumptions, and unknowns;
5. options and selected decision;
6. design, contracts, and deterministic required／optional／omit UML routing;
7. failure, security, and observability;
8. test portfolio and vertical TDD slices;
9. traceability;
10. rollout, rollback, evidence, and remaining risks.
11. repository-root `CHANGELOG.md` impact and completed `[Unreleased]` evidence.

### high-risk

Add applicable threat／abuse cases, data classification, migration and reconciliation,
performance budget, staged rollout, monitoring thresholds, rollback rehearsal, independent
review, and named approval boundary. Do not add irrelevant sections merely because the tier is
high-risk.

## Traceability

For standard and high-risk, keep one row per behavior:

~~~text
| Requirement | Acceptance | Test | Implementation | Evidence |
| REQ-001 | AC-001 | tests/... | src/... or diff | command/result |
~~~

Traceability must reflect the current implementation, not the original plan. Update it during each
CHECK. Lite may keep the same mapping inline rather than building a separate table.

## UML roles

- Every UML diagram uses a Mermaid fence. PlantUML／PUML is invalid for both roles.
- A decision diagram is `required` only when one of `risk-and-uml.md`'s observable triggers exposes
  a genuine unresolved software-system decision. It carries `decision_question` and REQ／AC
  `traces` and satisfies the Necessary UML gate.
- An `optional` explanatory diagram uses `diagram_role: reader-aid` and
  `reader_aid_purpose`. It carries no decision or traces and does not satisfy the gate.
- When no decision diagram is required, record `no_diagram_rationale` even if a reader aid exists.
- `omit` means no diagram is drawn. Risk tier alone never changes routing.

## Ready gate

- lite: metadata, current／expected, REQ／AC, test and recovery, UML rationale, no unresolved
  placeholder in required content.
- standard: all applicable design sections, REQ／AC links, required diagram question or omission rationale, test
  portfolio, complete traceability plan, recovery.
- high-risk: standard plus all applicable special-risk plans and review boundary.

The validator enforces structural minimums only. The Agent must independently test assumptions,
oracle strength, failure paths, and feasibility.

## Complete gate

- status is complete and required placeholders are removed;
- every REQ／AC maps to a test, implementation path or diff, and fresh evidence;
- RED, GREEN, refactor or exception, and final verification are recorded;
- actual behavior was checked in the nearest realistic environment;
- SDD／UML／decision matches the implementation;
- repository-root `CHANGELOG.md` exists, the same diff updates `[Unreleased]`, and the SDD records
  the entry or an inspectable evidence reference;
- remaining risks and recovery are explicit.

For lite, satisfy this in the one-page artifact; do not create a separate evidence document.

## Bundled commands

Scaffold without overwriting:

~~~text
python3 <skill-dir>/scripts/init_sdd.py --tier lite --title "Fix key" \
  --change-id CACHE-001 --output docs/sdd/CACHE-001.md
~~~

Validate:

~~~text
python3 <skill-dir>/scripts/validate_sdd.py docs/sdd/CACHE-001.md --phase ready
python3 <skill-dir>/scripts/validate_sdd.py docs/sdd/CACHE-001.md --phase complete --json
~~~
