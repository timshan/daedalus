# Daedalus

Daedalus is a Codex Skill for **spec-led, risk-tiered, test-first software development**.
It requires a proportional Software Design Document before production code, selects only necessary
UML, runs vertical RED→GREEN→REFACTOR→CHECK slices, and closes work with fresh evidence.

The name refers to Daedalus, the architect and craftsperson of Greek mythology: design and
construction are treated as one traceable discipline.

## What it changes

- **lite** keeps a local fix to a one-page design and focused regression.
- **standard** adds contracts, selected UML, test portfolio, and traceability.
- **high-risk** adds only the applicable security, migration, rollout, monitoring, and independent
  review evidence.
- SDD, tests, implementation, and observed results stay synchronized.

Daedalus does not create branches or worktrees, install dependencies, use telemetry, update
itself, or write external state without separate authorization.

## Repository layout

- `.agents/plugins/marketplace.json` — public marketplace identity and root Plugin source.
- `.codex-plugin/plugin.json` — formal Plugin identity and SemVer.
- `skills/daedalus/` — Skill payload packaged by the Plugin.
- `lifecycle.json` — immutable package boundary and repository checks.
- `docs/` — design and acceptance evidence.
- `CHANGELOG.md` — released project changes.
- `tests/` — standard-library contract tests for scripts and Skill packaging.

## Install from GitHub

Register the public repository at `main`, then install Daedalus from its marketplace:

~~~bash
codex plugin marketplace add timshan/daedalus --ref main
codex plugin add daedalus@daedalus
~~~

Restart or open a new Codex session after installation. Invoke it explicitly with a request such
as:

~~~text
Use $daedalus to add this API integration with a risk-tiered SDD and test-first slices.
~~~

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

The validator checks structural gates; it does not prove that requirements, design, tests, or
engineering judgment are correct.

## Verify this repository

~~~bash
python3 -m unittest discover -s tests -v
python3 skills/daedalus/scripts/self_test.py
~~~

The bundled self-test scaffolds a fresh standard SDD and validates a completed example using only
the installed Daedalus payload and Python's standard library.

### Forward-test provenance

The recorded lite and standard forward tests ran inside an environment that also loaded global
Eureka PDCA and SessionStart context. The observed runs consumed approximately 64k and 96k tokens,
respectively. Those totals are **not attributable to Daedalus alone** and are evidence of evaluation
contamination, not a clean cost benchmark. The behavioral results remain useful—the fixtures,
tests, diffs, and completed SDDs are retained—but adopters should not infer Daedalus's standalone
token cost from those two runs.

## License

MIT. Third-party projects examined during prior-art research were not copied into this repository.
