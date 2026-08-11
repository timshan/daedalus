# Daedalus

Daedalus is a standalone Codex Plugin for spec-led, risk-tiered, test-first software development.
It turns an observable outcome into a proportional living Software Design Document, draws only
decision-relevant UML, delivers vertical TDD slices, reconciles implementation discoveries with
the design, and closes with fresh evidence.

The name refers to Daedalus, the architect and craftsperson of Greek mythology: design and
construction are treated as one traceable discipline.

## Workflow

Daedalus uses one feedback loop:

1. **FRAME** the outcome, scope, recovery, and risk tier.
2. **MODEL** the smallest sufficient SDD and necessary UML.
3. **BIND** each acceptance criterion to an observable oracle and vertical slice.
4. **PROVE** the missing behavior with an intended RED.
5. **BUILD** the smallest GREEN change, then REFACTOR while green.
6. **RECONCILE** evidence with requirements, decisions, UML, and traceability.
7. **SEAL** the result with fresh affected checks and realistic outcome evidence.

SDD and TDD are complementary here: the SDD defines what and why; TDD supplies executable
evidence and discoveries that may revise the living design.

All UML is written in Mermaid so diagrams remain text-reviewable and use one portable format.
Every Daedalus-managed production change also creates or updates repository-root `CHANGELOG.md`
under `[Unreleased]` in the same diff as the implementation.

## Proportional tiers

- **lite**: a one-page artifact and focused behavior test for a bounded local change.
- **standard**: contracts, selected UML or a precise omission rationale, test portfolio, and
  traceability for public or cross-module behavior.
- **high-risk**: only the applicable threat, migration, performance, rollout, monitoring,
  independent-review, and rollback evidence.

Risk tier controls the depth of evidence. It does not mandate a fixed number of diagrams.

## Install from GitHub

~~~bash
codex plugin marketplace add timshan/daedalus --ref main
codex plugin add daedalus@daedalus
~~~

Restart or open a new Codex session, then invoke the Skill explicitly:

~~~text
Use $daedalus to add this API integration with a proportional SDD and test-first slices.
~~~

Daedalus's installed runtime uses Python's standard library and does not require another custom
Skill, development repository, background service, or network call.

## Scaffold and validate an SDD

~~~bash
python3 skills/daedalus/scripts/init_sdd.py \
  --tier standard \
  --title "Add billing adapter" \
  --change-id BILLING-002 \
  --output docs/sdd/BILLING-002.md

python3 skills/daedalus/scripts/validate_sdd.py \
  docs/sdd/BILLING-002.md \
  --phase ready
~~~

The validator checks structural gates; it cannot replace engineering judgment or prove that a
requirement is correct.

## Verify a clone

~~~bash
python3 -m unittest discover -s tests -v
python3 skills/daedalus/scripts/self_test.py
~~~

The self-test scaffolds a fresh standard SDD and validates a bundled completed example using only
the installed payload.

## Repository layout

- `.agents/plugins/marketplace.json` — public Codex marketplace entry.
- `.codex-plugin/plugin.json` — Plugin identity and SemVer.
- `skills/daedalus/` — the complete installable runtime payload.
- `lifecycle.json` — package allowlist, independence probe, and repository gates.
- `docs/sdd/DAEDALUS-INDEPENDENCE-002.md` — current redesign and acceptance evidence.
- `CHANGELOG.md` — human-readable unreleased and released project changes.
- `tests/` — standard-library contract and regression tests.

## Independence boundary

The formal payload allowlist contains only `.codex-plugin`, `LICENSE`, and `skills`. Repository
tests, lifecycle configuration, development records, and public documentation are not installed as
runtime instructions. The bundled self-test and isolated installation gate verify the exact payload;
Git history preserves superseded design records without keeping them in the current working tree.

## License

[MIT](LICENSE). Third-party projects examined during prior-art research were not copied into this
repository.
