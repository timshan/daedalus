---
name: daedalus
description: Guide risk-tiered software development from a living Software Design Document through deterministic necessary-UML routing, test-driven vertical slices, design reconciliation, and fresh outcome evidence. Use whenever Codex is asked to implement or modify production code—including features, bug fixes, refactors, integrations, migrations, performance or security changes—or to create a technical design that will lead to code. Do not use for read-only explanation, pure research, or documentation-only work that cannot change production behavior.
---

# Daedalus

Build from explicit intent and executable evidence. SDD defines what and why; TDD proves each
behavior and returns implementation discoveries to the living design.

## Invariants

- Write or update a tier-appropriate SDD before production code.
- Link observable outcomes through REQ and AC IDs to tests, implementation, and fresh evidence.
- Use the `required／optional／omit` UML routing rule; risk tier alone never mandates a diagram.
- Write every decision or reader-aid UML diagram in Mermaid; do not use PlantUML or PUML.
- Observe the intended missing behavior in RED before GREEN. Syntax, import, fixture, permission,
  or unavailable-environment failures are not behavioral RED.
- Reconcile design after every vertical slice; update or remove stale SDD／UML content.
- Create or update the repository-root `CHANGELOG.md` in the same diff as every production change,
  and keep the pending entry under `[Unreleased]` until release.
- Respect project instructions and user authority. This Skill grants no permission to create Git
  topology, install dependencies, access networks, or mutate external systems.
- Preserve unrelated user changes and never claim completion from stale evidence.

## Workflow

### 1. FRAME — outcome and risk

Read project instructions, current design, affected code, tests, contracts, and the smallest
relevant history. State goal, non-goals, observable outcomes, affected paths, recovery, and
uncertainty.

Inspect the repository-root `CHANGELOG.md`. If it is absent, plan to create it. Record the intended
`[Unreleased]` entry in the SDD without reconstructing unsupported historical release details.

Read [references/risk-and-uml.md](references/risk-and-uml.md) completely. Select lite, standard, or
high-risk and record `tier_rationale`. When uncertain, use standard. Never self-downgrade a clear
security, trust-boundary, irreversible, or migration risk.

### 2. MODEL — living SDD and necessary UML

Reuse the repository's current design format when it supports the required fields. Otherwise run:

~~~text
python3 <skill-dir>/scripts/init_sdd.py \
  --tier <lite|standard|high-risk> \
  --title "<change title>" \
  --change-id <ID> \
  --output <project>/docs/sdd/<change-id>.md
~~~

Read [references/sdd-schema.md](references/sdd-schema.md) completely. Separate WHAT—goal,
requirement, acceptance, expected outcome—from HOW—options, decision, contract, diagram, rollout.
Use stable REQ-NNN and AC-NNN IDs.

For every UML type, select `required`, `optional`, or `omit` using the observable triggers in
[references/risk-and-uml.md](references/risk-and-uml.md). Decision UML must describe the software
being built, not this workflow or the SDD document lifecycle. Draw the smallest set that resolves
genuine ambiguities; otherwise record one concrete `no_diagram_rationale`.
All selected UML, including optional reader aids, must be Mermaid.

Do not write production code until the structural ready gate passes:

~~~text
python3 <skill-dir>/scripts/validate_sdd.py <sdd-path> --phase ready
~~~

The validator checks structure, not correctness. Independently challenge assumptions, contracts,
failure paths, recovery, oracle strength, and each diagram's routing trigger.

### 3. BIND — acceptance to executable oracle

Read [references/tdd-and-verification.md](references/tdd-and-verification.md) completely. Map each AC
to the nearest observable outer oracle, then choose the smallest next vertical slice and its inner
test portfolio.

For brownfield work, characterize only adjacent behavior that must remain unchanged. Define the
defect itself with a new regression RED; never preserve a bug as desired behavior.

### 4. PROVE — intended RED

Add the smallest behavioral test for one AC. Run it before production code and record the command,
failure, and why it proves the requested behavior is missing. For standard and high-risk, name one
plausible wrong result and confirm the assertion rejects it. Strengthen with negative, boundary,
property, or mutation checks when risk warrants them.

### 5. BUILD — GREEN and REFACTOR

Make the smallest production change that satisfies the target behavior. Run the focused test and
affected existing tests. Improve names, duplication, seams, and boundaries only while green, then
rerun fresh checks after the refactor.

Do not silently retry flaky tests until green. Fix nondeterminism or quarantine it only with a
tracked reason, exit condition, and evidence that the target oracle remains valid.

### 6. RECONCILE — return evidence to design

Update REQ／AC traceability, implementation paths, evidence, remaining risks, and recovery. Compare
the actual implementation with every affected decision and diagram. Update or remove stale UML.
Update the repository-root `CHANGELOG.md` with the externally observable or maintainer-relevant
change; keep implementation noise out of the entry.

If evidence invalidates a requirement, contract, option, risk classification, or UML decision,
return to MODEL, revise the SDD, pass the ready gate again, then create the next RED. If the design
still holds and accepted behavior remains, return to BIND for the next slice.

### 7. SEAL — fresh outcome proof

Apply the proportional completion gate:

- **lite:** one-page artifact, one focused behavior or regression test, actual diff, fresh affected
  checks, realistic outcome inspection, and recovery.
- **standard:** applicable traceability, contract／integration evidence, SDD consistency, fresh
  build／lint／type／test results, realistic outcome inspection, and remaining risks.
- **high-risk:** standard evidence plus only the applicable independent review, security,
  performance, migration rehearsal, rollout, monitoring, and rollback proof.

Set status to complete, replace unresolved completion markers with evidence, and run:

~~~text
python3 <skill-dir>/scripts/validate_sdd.py <sdd-path> --phase complete
~~~

Inspect the actual diff and nearest realistic outcome. Passing tests alone is not proof that the
requested result exists. Confirm the same diff contains the SDD's `CHANGELOG.md` entry under
`[Unreleased]`; do not mark the SDD complete when changelog evidence is missing.

## Exceptions and stop conditions

- A time-boxed spike may precede production TDD only to resolve a named technical unknown. Discard
  it or place its behavior behind a failing contract test before production use.
- Generated code, pure documentation, and declarative configuration may use schema, snapshot,
  dry-run, smoke, or integration evidence instead of a unit RED. Record the exception and
  alternate oracle; standard and high-risk RECONCILE must challenge the justification.
- Stop for direction when requirements conflict, a required outcome has no safe oracle, a
  high-risk irreversible action lacks rollback, or new authority is needed for an external write.

## Bundled resources

- [references/risk-and-uml.md](references/risk-and-uml.md): tier definitions and deterministic UML
  routing.
- [references/sdd-schema.md](references/sdd-schema.md): artifact schema, gates, and traceability.
- [references/tdd-and-verification.md](references/tdd-and-verification.md): oracle selection, TDD,
  exceptions, and outcome evidence.
- [scripts/init_sdd.py](scripts/init_sdd.py): scaffold a tier-specific SDD without overwriting by
  default.
- [scripts/validate_sdd.py](scripts/validate_sdd.py): deterministic structural ready／complete gate.
- [scripts/self_test.py](scripts/self_test.py): exercise scaffold and validation from the installed
  payload.
- `assets/templates/` and `assets/examples/`: bundled scaffolds and standalone evidence fixture.
