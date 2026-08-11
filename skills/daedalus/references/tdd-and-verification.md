# TDD and outcome verification

Use an outer observable oracle and an inner implementation loop. Unit TDD alone does not prove
contracts, external integrations, security, performance, or migration behavior.

## Outer oracle

Translate each AC into the nearest executable evidence:

- acceptance／BDD for user-visible behavior;
- contract tests for APIs, events, schemas, files, or CLIs;
- integration tests for database, filesystem, SDK, queue, or real dependency seams;
- E2E／smoke for the critical cross-component journey.

Do not substitute mock call sequences for an observable outcome unless the call itself is the
public contract.

## Inner RED→GREEN→REFACTOR→CHECK

### RED

1. Add one smallest behavioral test for one AC.
2. Run it before production code.
3. Confirm the failure is the intended missing behavior—not syntax, import, fixture, permission,
   stale build, or unavailable environment.
4. Record command, key failure, and reason.
5. For standard／high-risk, state one plausible wrong implementation result and confirm the oracle
   rejects it. Add negative, boundary, property, or mutation testing when it does not.

### GREEN

Write only enough production change to satisfy the behavior. Run the focused test and affected
existing tests. Avoid speculative abstractions and unrelated cleanup.

### REFACTOR

While green, improve names, duplication, seams, and boundaries. Rerun fresh checks after the
refactor; earlier green output is stale evidence.

### CHECK

Update REQ／AC traceability, implementation path or diff, and evidence. If the slice invalidates a
design assumption, update SDD／UML／decision and pass ready again.

## Portfolio escalation

| Risk signal | Add |
|---|---|
| Parser, calculation, many branches | property, fuzz, boundary, or mutation checks |
| Public API／event／schema | consumer／provider contract tests |
| Database／filesystem／SDK／queue | integration tests with the real seam |
| Critical user journey | focused E2E or smoke |
| Auth／trust／secrets | abuse cases and security checks |
| Numerical SLO／cost budget | reproducible benchmark with threshold |
| Data migration／irreversible state | rehearsal, reconciliation, backup, and rollback evidence |

## Brownfield rules

- Characterize only adjacent behavior the change must preserve.
- Define the defect with a new regression RED; never encode the defect as desired behavior.
- A lite bugfix may skip a separate characterization ritual when one focused regression isolates
  the risk.
- Do not broaden a refactor until affected existing behavior is observable.

## Flaky and exceptional work

- Never silently retry until green. Fix nondeterminism or quarantine with owner／tracking reason,
  expiry or exit condition, and proof that the target oracle remains valid.
- A time-boxed spike answers one technical unknown; discard it or place it behind a failing
  contract before production use.
- Generated code, pure documentation, or declarative config may use schema, snapshot, dry-run,
  smoke, or integration evidence instead of unit RED. Record why and challenge the alternate
  oracle at standard／high-risk CHECK.

## Fresh completion evidence

Run the applicable test, lint, typecheck, build, security, benchmark, or rehearsal command after
the final change. Inspect the actual diff and the nearest realistic outcome. Record command,
result, timestamp when useful, remaining risk, and recovery. Do not claim complete from memory,
old output, or Agent confidence.
