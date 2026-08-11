---
change_id: DAEDALUS-INSTALL-HOTFIX-003
title: Daedalus v1.0.1 public installation hotfix
risk_tier: standard
status: complete
date: 2026-08-11
tier_rationale: Changes the public Codex CLI installation contract, GitHub marketplace package boundary, Plugin identity version, and release behavior across an external consumer boundary.
affected_paths: .agents/plugins/marketplace.json, .codex-plugin/plugin.json, README.md, CHANGELOG.md, lifecycle.json, skills/daedalus/scripts/self_test.py, skills/daedalus/assets/examples/standalone-standard-complete.md, tests/test_public_install_contract.py, docs/SDD.md, docs/sdd/DAEDALUS-PLUGIN-001.md, docs/sdd/DAEDALUS-INSTALL-HOTFIX-003.md
---

# Daedalus v1.0.1 public installation hotfix

## Goal and non-goals

Goal: make public `main` installable from `timshan/daedalus` with the documented Codex CLI selector, while preserving the v1.0.0 Daedalus workflow and producing a standalone formal Plugin version 1.0.1.

Non-goals: import the 1.1.0 seven-stage workflow, Mermaid-only validator changes, changelog enforcement gate, or other develop behavior; rewrite v1.0.0 tags, Release, or artifact; create a third branch, worktree, or pull request.

## Current state and expected outcomes

Current: public `main` at `4bc7b593ec6312acb58a2215b3506a97148982f0` documents an author-local installation source and has no repository marketplace manifest. The Plugin manifest is 1.0.0, the lifecycle config has no package allowlist or standalone check, and there is no repository-root changelog.

| Outcome ID | Observable expected result | Evidence |
|---|---|---|
| OUT-001 | The two README commands register GitHub `main` and install `daedalus@daedalus`. | Contract test and post-release fresh-profile transcript. |
| OUT-002 | Marketplace name, Plugin entry, manifest identity, and source root agree on `daedalus` and `.`. | Cross-field regression and Plugin validation. |
| OUT-003 | The formal payload contains only `.codex-plugin`, `LICENSE`, and `skills`, then passes an installed-cache core capability probe. | `lifecycle.json` contract and Ariadne independence JSON. |
| OUT-004 | v1.0.1 documents the installation repair without importing 1.1.0 runtime behavior. | Changelog, version diff, unit suite, and Skill validation. |
| OUT-005 | Existing public documentation has no author-machine installation dependency. | Repository documentation scan. |

## Requirements

- REQ-001: Publish a root marketplace named `daedalus` with exactly one Plugin named `daedalus` whose local source path is `.`.
- REQ-002: Document exactly `codex plugin marketplace add timshan/daedalus --ref main` followed by `codex plugin add daedalus@daedalus` as the public installation interface.
- REQ-003: Set the root Plugin manifest to strict SemVer `1.0.1` without changing the v1.0.x Skill workflow contract.
- REQ-004: Allowlist only `.codex-plugin`, `LICENSE`, and `skills` in the formal payload and declare a non-empty installed-payload standalone check.
- REQ-005: Bundle a Python-standard-library self-test that scaffolds a standard SDD and validates a completed v1.0.x-compatible example from the installed Plugin.
- REQ-006: Create a repository-root changelog with a v1.0.1 installation fix and v1.0.0 baseline, and remove author-local installation dependencies from current public Markdown.

## Acceptance criteria

- AC-001 (REQ-001, REQ-003): Given the repository manifests, when the public-install contract test runs, then marketplace name, only Plugin name, manifest name, source path, and version equal `daedalus`, `daedalus`, `daedalus`, `.`, and `1.0.1` respectively.
- AC-002 (REQ-002): Given README, when its installation code block is inspected, then it contains the two approved commands in order and no alternate local marketplace command.
- AC-003 (REQ-004): Given `lifecycle.json`, when lifecycle validation runs, then its exact package allowlist and standalone check are accepted.
- AC-004 (REQ-005): Given only the installed payload and Python 3, when `self_test.py` runs, then it creates a standard scaffold and validates the bundled complete example.
- AC-005 (REQ-006): Given repository Markdown, when the documentation regression runs, then no forbidden author-local path or local formal marketplace identifier is present and the changelog contains both 1.0.1 and 1.0.0.
- AC-006 (REQ-001, REQ-002, REQ-003): Given a plausible wrong result where README appears correct but marketplace or Plugin identity differs, when the cross-field oracle evaluates it, then it reports an identity mismatch.
- AC-007 (REQ-001, REQ-002, REQ-003, REQ-004, REQ-005): Given the exact candidate artifact in a fresh isolated profile, when the independence gate runs, then `daedalus@ariadne-standalone` 1.0.1 is the only enabled Plugin and its installed self-test passes.

## Constraints, assumptions, and unknowns

- Constraint: Keep only local `develop` and `main`; use no feature branch, worktree, pull request, external dependency, or mutation before exact authorization.
- Constraint: Preserve v1.0.0 refs, Release, and artifact; a publication failure must be fixed forward as v1.0.2 rather than by rewriting v1.0.1.
- Constraint: The hotfix includes only package and installation compatibility needed by v1.0.x.
- Assumption: Codex resolves a GitHub marketplace repository through `.agents/plugins/marketplace.json`, then resolves the selector as Plugin name at marketplace name.
- Assumption: Ariadne 1.1.2 can validate and promote a root Plugin with an explicit package allowlist and standalone check.
- Unknown: Public installation and Git marketplace source can only be proven after exact v1.0.1 release authorization and remote publication.

## Options and decision

| Option | Benefit | Cost or risk | Decision |
|---|---|---|---|
| Publish current 1.1.0 develop | Already has a public marketplace and standalone probe | Expands the emergency fix into workflow, UML, validator, and changelog-gate changes | Reject |
| Edit README only on v1.0.0 | Smallest text diff | Selector still cannot resolve because the marketplace manifest is absent | Reject |
| Backport the minimal package boundary to v1.0.1 | Repairs the public contract while preserving v1.0.x behavior | Requires a separate patch release and later merge reconciliation | Select |

## Design and contracts

GitHub `main` is the public marketplace source. Its root marketplace manifest owns the public marketplace identity `daedalus` and points its sole `daedalus` Plugin to repository root `.`. The root Plugin manifest owns Plugin identity and version 1.0.1 and points Skill discovery to `./skills/`. README composes those identities into `daedalus@daedalus`; the regression reads all three surfaces together rather than validating each file in isolation.

The formal package boundary is separate from the Git marketplace metadata. `lifecycle.json` allowlists `.codex-plugin`, `LICENSE`, and `skills`; Ariadne builds and installs those exact bytes through an isolated temporary marketplace. The bundled self-test imports sibling v1.0.x scripts from the installed payload, scaffolds a new standard SDD in a temporary directory, and validates a bundled complete fixture. Repository tests, public docs, marketplace metadata, and lifecycle configuration remain outside the installed formal runtime.

## Necessary UML

decision_question: How does the GitHub marketplace resolve and install Daedalus without an author-local formal channel?
traces: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, AC-001, AC-002, AC-003, AC-004, AC-006, AC-007

~~~mermaid
flowchart LR
    User[Codex user] -->|marketplace add repository at main| GitHub[GitHub repository main]
    GitHub --> Registry[Marketplace manifest: daedalus]
    Registry -->|Plugin daedalus, local source dot| Root[Repository root Plugin]
    Root --> Manifest[Plugin manifest: daedalus 1.0.1]
    Manifest -->|skills path| Skill[skills/daedalus]
    User -->|plugin add daedalus at daedalus| Installed[Codex installed Plugin]
    Skill --> Installed
    Lifecycle[Formal allowlist] -->|manifest, license, skills| Artifact[Exact standalone artifact]
    Artifact --> InstalledProbe[Isolated installed self-test]
~~~

## Failure, security, and observability

| Failure or risk | Detection | Handling or recovery |
|---|---|---|
| README command and manifest identities drift | Cross-field contract regression and plausible-wrong-result test | Stop before commit or release; repair the inconsistent surface. |
| Marketplace source points outside repository root | Exact JSON assertion and fresh public install | Stop publication; retain v1.0.0 and correct the v1.0.1 candidate. |
| Formal payload includes repository-only data | Exact package allowlist assertion and Ariadne artifact inspection | Stop promotion; narrow `package_paths`. |
| Self-test accidentally depends on 1.1.0 workflow | Run self-test on the v1.0.0-based candidate and inspect its fixture markers | Replace with a v1.0.x-compatible fixture; do not copy 1.1.0 assets. |
| Remote state changes partially | Ariadne dry-run, pre-write ref checks, atomic release path, and post-write readback | Stop on any gate failure; do not retry blindly or rewrite tags. |
| Public install fails after release | Fresh profile install from README plus marketplace-source inspection | Do not claim completion; preserve v1.0.1 and prepare v1.0.2. |

## Test portfolio and TDD slices

Outer acceptance or contract oracle: run the README commands verbatim in an empty Codex profile after publication, then assert the installed Plugin identity, version, enabled state, Git source URL, installed bytes, and bundled self-test.

1. RED: `python3 -B -m unittest tests.test_public_install_contract -v` on the unmodified v1.0.0 baseline ran seven tests; six target tests failed with nine assertions for the absent marketplace, old README commands, missing package boundary and probe, missing changelog, and forbidden public references. The plausible wrong cross-field identity test passed by rejecting the mismatch.
2. GREEN: the same focused command passed all seven tests after adding only the v1.0.1 marketplace, README, manifest version, allowlist, self-test, fixture, changelog, and public-document sanitization required by the contract.
3. REFACTOR: the cross-field helper remains test-only and the runtime probe remains inside the packaged Skill; no production abstraction, external dependency, or 1.1.0 workflow behavior was added.
4. CHECK: the focused regression passed 7 tests and the full suite passed 38 tests; Plugin／Skill validators, both completed legacy SDD gates, the bundled self-test, Codex CLI contract help, and `git diff --check` passed on the final working diff.

## Traceability

| Requirement | Acceptance | Test | Implementation | Evidence |
|---|---|---|---|---|
| REQ-001, REQ-003 | AC-001, AC-006 | tests/test_public_install_contract.py | .agents/plugins/marketplace.json; .codex-plugin/plugin.json | Focused contract 7 tests passed; wrong identity fixture was rejected. |
| REQ-002 | AC-002, AC-006 | tests/test_public_install_contract.py | README.md | Exact ordered commands and single-command counts passed; Codex 0.147.0 help confirms both argument forms. |
| REQ-004 | AC-003, AC-007 | tests/test_public_install_contract.py; Ariadne independence | lifecycle.json | Exact allowlist regression passed; isolated artifact payload SHA-256 is `e0187339b69b8c93600e4f740dbc81c6ec7000f1f9d0bac937f6f29549357351`. |
| REQ-005 | AC-004, AC-007 | tests/test_public_install_contract.py; installed self-test | skills/daedalus/scripts/self_test.py; skills/daedalus/assets/examples/standalone-standard-complete.md | `daedalus@ariadne-standalone` 1.0.1 was the sole enabled Plugin, installed-cache self-test passed 1/1, and artifact SHA-256 is `260f1973d16c91ae83091c5b3705173575e6c28e4b53bdf74a7ebb460dadea48`. |
| REQ-006 | AC-005 | tests/test_public_install_contract.py | CHANGELOG.md; README.md; docs/SDD.md; docs/sdd/DAEDALUS-PLUGIN-001.md | Documentation scan and changelog assertions passed. |

## Rollout, rollback, and remaining risks

Rollout: implement and commit the candidate on the isolated clone's `develop`; run Ariadne independence and promotion／release dry-runs; after exact authorization, promote 1.0.1, release the locked artifact, verify public installation, fast-forward canonical `main`, merge `main` once into canonical `develop`, verify ancestry, and push `develop`.

Rollback: before external writes, discard the isolated clone or revert its commit. After release, keep v1.0.0 immutable and recover by reinstalling it; do not remove or rewrite v1.0.1. Canonical develop conflict resolution remains recoverable through the single merge commit and its first parent.

Remaining risks: public Git installation and GitHub Release byte identity require the post-authorization lifecycle gates; external publication still requires exact authorization. Historical evidence was wording-sanitized without changing its recorded outcomes.

## Verification evidence

- RED evidence: `python3 -B -m unittest tests.test_public_install_contract -v` on v1.0.0 produced six failing tests and nine failed assertions for the intended missing installation behavior; the wrong-identity control was rejected.
- GREEN evidence: the focused command passed 7 tests after the minimal package and documentation changes.
- Refactor or exception: no production refactor was needed; the v1.0.x validator and workflow remain unchanged, while the new self-test reuses their public modules.
- Fresh verification: `python3 -B -m unittest discover -s tests -v` passed 38 tests; Plugin validation, Skill quick validation, two legacy complete SDD gates, bundled self-test, Codex CLI help, and `git diff --check` all returned zero. Ariadne independence and 1.0.1 promotion dry-run also passed.
- Realistic outcome check: Ariadne built the allowlisted artifact, installed it into a fresh isolated profile as the sole enabled `daedalus@ariadne-standalone` 1.0.1 Plugin, verified installed bytes, and passed its installed-cache self-test. Public Git installation remains the post-release outer oracle rather than an inferred result.
