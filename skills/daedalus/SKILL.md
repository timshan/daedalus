---
name: daedalus
description: Guide risk-tiered software development from a Software Design Document through necessary UML, test-driven vertical slices, fresh verification, and living-design updates. Use whenever Codex is asked to implement or modify production code—including features, bug fixes, refactors, integrations, migrations, performance or security changes—or to create a technical design that will lead to code. Do not use for read-only explanation, pure research, or documentation-only work that cannot change production behavior.
---

# Daedalus

Build from explicit intent and evidence. Keep the process proportional: a localized fix gets a
one-page artifact; a risky boundary or migration gets deeper design and verification.

## Non-negotiable invariants

- Write or update a tier-appropriate Software Design Document before production code.
- Link observable outcomes through requirement and acceptance IDs to tests, implementation, and evidence.
- Create UML only to answer a named design question. Record a rationale when no diagram is needed.
- Observe RED for the intended missing behavior before GREEN. Do not count syntax, fixture, import, or environment failures.
- Treat the SDD as living: write back verified design drift during every slice CHECK.
- Do not create a branch or worktree, install dependencies, use network access, or mutate external state unless the user separately authorizes it.
- Treat any untagged gate as a workflow defect; it does not apply to lite work.

## Workflow

### 1. Inspect and classify

Read project instructions, existing design documents, affected code, tests, public contracts, and
the smallest relevant history. State goal, non-goals, expected outcomes, affected paths, recovery,
and uncertainty.

Read [references/risk-and-uml.md](references/risk-and-uml.md) completely. Select lite, standard,
or high-risk and record tier_rationale. When uncertain, use standard. Never self-downgrade a
security, trust-boundary, irreversible, or migration risk.

### 2. Create the SDD

Reuse the repository's current design location and format when it supports the required fields.
Otherwise create docs/sdd/<change-id>.md. To scaffold the bundled format, run:

~~~text
python3 <skill-dir>/scripts/init_sdd.py \
  --tier <lite|standard|high-risk> \
  --title "<change title>" \
  --change-id <ID> \
  --output <project>/docs/sdd/<change-id>.md
~~~

Read [references/sdd-schema.md](references/sdd-schema.md) completely before filling the artifact.
Separate WHAT—goal, requirement, acceptance, expected outcome—from HOW—options, decision,
contract, diagram, rollout. Use stable REQ-NNN and AC-NNN IDs.

Do not write production code until the ready gate passes:

~~~text
python3 <skill-dir>/scripts/validate_sdd.py <sdd-path> --phase ready
~~~

The bundled validator checks structure, not correctness. Independently challenge assumptions,
contracts, failure paths, test oracle, recovery, and whether each diagram answers its question.

### 3. Select the test portfolio

Read [references/tdd-and-verification.md](references/tdd-and-verification.md) completely. Define an
outer acceptance or contract test for the observable outcome, then select inner unit, integration,
E2E, property, mutation, security, performance, or migration checks by risk.

For brownfield work, characterize only adjacent behavior that must remain unchanged. Define the
defect itself with a new regression RED. Never preserve a bug as characterization.

### 4. Deliver vertical TDD slices

For one observable behavior at a time:

1. **RED:** Add the smallest behavioral test. Run it and record the command, failure, and why the
   failure proves missing behavior. For standard and high-risk, name one plausible wrong result
   and confirm the assertion rejects it; strengthen with negative, property, or mutation checks
   when needed.
2. **GREEN:** Make the smallest production change that passes the target behavior. Run focused
   and affected existing tests.
3. **REFACTOR:** Improve names, duplication, and boundaries only while green; rerun fresh checks.
4. **CHECK:** Update traceability and evidence. If implementation or tests reveal a design error,
   return to the SDD, update the decision or UML, and revalidate ready before continuing.

Do not silently retry a flaky test until green. Fix nondeterminism or quarantine it only with a
tracked reason and evidence that it does not invalidate this slice's oracle.

### 5. Verify the expected result

Apply the tier-specific completion gate:

- **lite:** one-page artifact, one focused regression or behavior test, actual diff, fresh affected
  checks, and recovery.
- **standard:** all applicable traceability, contract or integration evidence, SDD consistency,
  fresh build／lint／type／test results, realistic outcome verification, and remaining risks.
- **high-risk:** all standard evidence plus the applicable independent review, security,
  performance, migration rehearsal, rollout, monitoring, and rollback proof.

Set SDD status to complete, replace placeholders with evidence, and run:

~~~text
python3 <skill-dir>/scripts/validate_sdd.py <sdd-path> --phase complete
~~~

Inspect the actual diff and external state. Passing tests alone is not proof that the requested
outcome exists.

## Exceptions and stop conditions

- A time-boxed spike may precede production TDD only to resolve a named technical unknown. Discard
  it or place its behavior behind a failing contract test before production use.
- Generated code, pure documentation, and declarative configuration may use schema, snapshot,
  dry-run, smoke, or integration evidence instead of a unit RED. Record the exception and
  alternate oracle; standard and high-risk CHECK must challenge the justification.
- Stop and ask for direction when requirements conflict, a required outcome has no safe oracle,
  a high-risk irreversible action lacks rollback, or authority is needed for an external write.
- Preserve unrelated user changes. Never use completion language without fresh evidence.

## Bundled resources

- [references/risk-and-uml.md](references/risk-and-uml.md): tier definitions, operational terms,
  escalation triggers, and UML selection.
- [references/sdd-schema.md](references/sdd-schema.md): artifact schema, ready／complete gates, and
  traceability rules.
- [references/tdd-and-verification.md](references/tdd-and-verification.md): RED quality, portfolio
  selection, exceptions, and outcome evidence.
- [scripts/init_sdd.py](scripts/init_sdd.py): scaffold a tier-specific SDD without overwriting by
  default.
- [scripts/validate_sdd.py](scripts/validate_sdd.py): deterministic structural ready／complete gate.
- assets/templates/: source templates consumed by the scaffold script.
