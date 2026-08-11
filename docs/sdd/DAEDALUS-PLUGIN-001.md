---
change_id: DAEDALUS-PLUGIN-001
title: Package Daedalus as a formal Codex Plugin
risk_tier: standard
status: complete
date: 2026-08-11
tier_rationale: Changes runtime packaging, version identity, installation instructions, and formal promotion gates without changing the Daedalus Skill's behavior.
affected_paths: .codex-plugin/plugin.json, lifecycle.json, README.md, tests/test_skill_contract.py, docs/sdd/DAEDALUS-PLUGIN-001.md
---

# Package Daedalus as a formal Codex Plugin

## Goal and non-goals

Goal: package the existing validated Daedalus Skill as versioned Codex Plugin `daedalus` 1.0.0 and connect it to the formal lifecycle without exposing mutable development source to Codex discovery.

Non-goals: change Daedalus workflow semantics, delete legacy installations, edit Codex cache files, or publish bytes that differ from the local formal artifact.

## Current state and expected outcomes

Current: the repository is a valid standalone Skill repository on `main`; it has no Plugin manifest, formal version, immutable artifact, or Plugin installation path.

| Outcome ID | Observable expected result | Evidence |
|---|---|---|
| OUT-001 | Codex Plugin tooling accepts the repository payload | Plugin validator and Skill validator pass. |
| OUT-002 | Development and formal installation are separated | README uses an immutable formal marketplace and contains no direct copy instruction. |
| OUT-003 | Formal promotion audits legacy discovery roots | `lifecycle.json` includes both standalone Skill roots and controller regression proves the wiring. |

## Requirements

- REQ-001: Add a strict-SemVer Plugin manifest whose name is `daedalus` and whose Skill source is `./skills/`.
- REQ-002: Configure repository tests, completed SDD gates, and real standalone discovery roots for lifecycle promotion.
- REQ-003: Replace direct Skill-folder installation guidance with the immutable formal Plugin marketplace workflow.
- REQ-004: Preserve the existing Skill payload and legacy commit through an explicit recovery tag.

## Acceptance criteria

- AC-001 (REQ-001): Given the repository root, when the official Plugin validator runs, then it accepts the manifest and packaged Skill.
- AC-002 (REQ-002): Given a same-named Skill under a configured discovery root, when promotion preflight runs, then it fails with `E_DISCOVERY` before mutation.
- AC-003 (REQ-003): Given the README, when its installation section is inspected, then it uses `codex plugin` and contains no copy into `~/.codex/skills`.
- AC-004 (REQ-004): Given the pre-migration commit, when recovery refs are inspected, then `legacy-standalone-20260811` points to that exact commit.

## Constraints, assumptions, and unknowns

- Constraint: Keep exactly the two permanent branches selected by the lifecycle policy: `develop` and `main`.
- Assumption: A non-default immutable formal marketplace is generated and activated by the lifecycle controller.
- Unknown: Universal public Plugin-directory submission remains outside this migration; GitHub Release is the publication boundary.

## Options and decision

| Option | Benefit | Cost or risk | Decision |
|---|---|---|---|
| Keep manual standalone copy | No packaging change | Duplicate discovery and unversioned runtime drift remain | Reject |
| Package repository root as Plugin | Preserves existing layout and tests | Artifact contains repository support files | Select |
| Move Skill under a nested Plugin directory | Repo-local marketplace layout is conventional | Large path migration adds no runtime value | Reject |

## Design and contracts

The Plugin manifest discovers `skills/daedalus`. `lifecycle.json` declares the repository root as the payload, executes all existing tests plus both completed SDD gates, and audits `~/.codex/skills` and `~/.agents/skills`. The lifecycle controller promotes the clean `develop` commit to `main`, produces `formal/v1.0.0`, and activates the exact artifact through an immutable formal marketplace.

## Necessary UML

no_diagram_rationale: The component relationship is a single repository payload consumed by an already documented lifecycle controller; the lifecycle state and ownership UML live in that controller's high-risk SDD, and duplicating it here would not change this packaging decision.

## Failure, security, and observability

| Failure or risk | Detection | Handling or recovery |
|---|---|---|
| Invalid Plugin schema | Official Plugin validator exits nonzero | Stop promotion and retain standalone recovery tag. |
| Legacy duplicate Skill | Configured discovery audit finds duplicate name or symlink | Stop promotion; archive or reconcile only after comparison. |
| Artifact or release drift | Formal lock checksum differs | Stop activation/publication and retain prior runtime. |

## Test portfolio and TDD slices

Outer acceptance or contract oracle: repository unit tests, official Plugin and Skill validators, Daedalus SDD validators, lifecycle dry-run, and independent w5:p3 review.

1. RED: Plugin contract tests failed because the manifest and lifecycle file were absent and README instructed direct copy.
2. GREEN: Added manifest, lifecycle configuration, formal install guidance, and discovery-root assertions.
3. REFACTOR: Kept the existing repository layout and added no dependency or runtime code.
4. CHECK: 31 repository tests, Plugin validator, Skill validator, old SDD complete gate, and this SDD complete gate pass in the staging tree.

## Traceability

| Requirement | Acceptance | Test | Implementation | Evidence |
|---|---|---|---|---|
| REQ-001 | AC-001 | tests/test_skill_contract.py | .codex-plugin/plugin.json | Plugin validator passed in staging. |
| REQ-002 | AC-002 | lifecycle controller discovery regression | lifecycle.json | Discovery-root regression passed. |
| REQ-003 | AC-003 | tests/test_skill_contract.py | README.md | README contract passed. |
| REQ-004 | AC-004 | Git tag inspection | legacy-standalone-20260811 | Tag recorded at pre-migration commit 0afd87e. |

## Rollout, rollback, and remaining risks

Rollout: commit to `develop`, run lifecycle dry-run, obtain w5:p3 PASS, promote the exact commit to local formal, validate the extracted payload, then separately publish that artifact.

Rollback: reinstall a previous immutable formal package when available; for this first Plugin migration, archive rather than delete any legacy standalone runtime and use `legacy-standalone-20260811` to reconstruct source.

Remaining risks: a legacy standalone Daedalus copy, if discovered, must be reconciled before formal activation; public directory submission is not included.

## Verification evidence

- RED evidence: the two new Plugin contract tests failed on missing manifest and direct-copy README.
- GREEN evidence: the same tests passed after the packaging files and README changed.
- Refactor or exception: packaging preserves the existing Skill path and adds no behavioral implementation.
- Fresh verification: staging run completed 31 unit tests and both official validators successfully on 2026-08-11.
- Realistic outcome check: lifecycle promotion remains gated on the clean committed source, discovery audit, and second adversarial review.
