---
change_id: SELF-TEST-COMPLETE-001
title: Installed Daedalus capability probe
risk_tier: standard
status: complete
---

# Installed Daedalus capability probe

## Goal and non-goals

Goal: prove the installed payload can validate a completed standard SDD. Non-goal: modify a production system.

## Current state and expected outcomes

Current: the fixture is bundled with Daedalus. Expected: the v1.0.x validator accepts it at the complete gate.

## Requirements

- REQ-001: Validate one complete standard SDD from the installed payload.

## Acceptance criteria

- AC-001 (REQ-001): Given the bundled fixture, when complete validation runs, then it returns no structural errors.

## Constraints, assumptions, and unknowns

Use only the installed Plugin payload and Python standard library. The fixture does not claim semantic design correctness.

## Options and decision

Select a bundled static fixture because it supplies a deterministic complete-gate oracle without external services.

## Design and contracts

The self-test reads this UTF-8 Markdown file and calls the sibling validator's public `validate` function with phase `complete`.

## Necessary UML

no_diagram_rationale: The local deterministic function call has no boundary, lifecycle, schema, interaction-order, or deployment decision.

## Failure, security, and observability

Validation errors are printed without secrets and return a nonzero process status.

## Test portfolio and TDD slices

The outer probe combines a fresh standard scaffold with complete validation of this fixture.

## Traceability

| Requirement | Acceptance | Test | Implementation | Evidence |
|---|---|---|---|---|
| REQ-001 | AC-001 | self_test.py | validate_sdd.py | Installed-payload probe returns zero. |

## Rollout, rollback, and remaining risks

Rollout is inclusion in the immutable Plugin payload. Rollback reinstalls a prior immutable version.

Remaining risks: structural validation does not prove the quality of a real project's requirements or implementation.

## Verification evidence

RED evidence: the v1.0.0 installed payload had no bundled standalone probe.
GREEN evidence: the v1.0.1 self-test validates this fixture successfully.
Refactor or exception: the probe reuses the public scaffold and validator modules without a new dependency.
Fresh verification: repository tests and isolated installed-payload execution run after the final diff.
Realistic outcome check: the isolated profile invokes this file from the Codex-installed Plugin cache.
