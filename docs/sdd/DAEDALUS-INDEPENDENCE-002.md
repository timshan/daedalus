---
change_id: DAEDALUS-INDEPENDENCE-002
title: Make Daedalus independently installable and evidence-driven
risk_tier: standard
status: complete
date: 2026-08-11
tier_rationale: Changes the public Plugin payload, Skill workflow, templates, validation contract, and installation guidance across repository boundaries; it does not introduce a trust, secret, migration, or irreversible-data boundary.
affected_paths: .agents/plugins/marketplace.json, .codex-plugin/plugin.json, lifecycle.json, README.md, CHANGELOG.md, docs/SDD.md, docs/sdd/, skills/daedalus/, tests/
---

# Make Daedalus independently installable and evidence-driven

## Goal and non-goals

Goal: remove repository and workflow content inherited from unrelated Skills or controllers, package only Daedalus-owned runtime files, and make one installed Daedalus Plugin sufficient to guide a coding agent from a proportional SDD through UML, TDD slices, design reconciliation, changelog maintenance, and fresh outcome evidence.

Non-goals: embed a lifecycle or release controller into Daedalus, require a specific Git branching model, require subagents or external review for ordinary work, or replace project-specific test tools.

## Current state and expected outcomes

Current: all 31 repository tests pass, but Ariadne independence exits with `E_INDEPENDENCE_CONFIG`; the root is packaged without an allowlist, README installation depends on an unrelated local controller path, the baseline SDD and tests preserve contaminated global-session evidence, and the packaged Skill carries lifecycle policy unrelated to SDD／TDD.

| Outcome ID | Observable expected result | Evidence |
|---|---|---|
| OUT-001 | The formal payload contains only the Plugin manifest, license, and Daedalus Skill | Artifact member and package allowlist tests |
| OUT-002 | The exact payload installs as the sole enabled Plugin in a fresh profile and executes a bundled core probe | Ariadne independence JSON reports independent and one standalone check passed |
| OUT-003 | Packaged instructions contain no explicit dependency on another custom Skill or controller | Ariadne dependency scan reports zero references and local provenance tests pass |
| OUT-004 | A coding agent can follow one coherent SDD→TDD→design-feedback workflow | Skill contract tests, bundled self-test, and isolated forward acceptance |
| OUT-005 | Repository documentation contains no stale local installation path or contaminated benchmark claim | Documentation contract tests and scoped content scan |
| OUT-006 | Every Daedalus-managed production change has a human-readable pending changelog entry | Skill contract, SDD structural gate, templates, and repository `CHANGELOG.md` |

## Requirements

- REQ-001: Define an allowlisted Plugin payload containing `.codex-plugin`, `LICENSE`, and `skills` only.
- REQ-002: Declare a non-empty standalone check that runs from the installed payload without network, third-party packages, or another custom Skill.
- REQ-003: Make the standalone check exercise both SDD scaffolding and structural validation, not merely `--help`.
- REQ-004: Replace unrelated lifecycle, branching, worktree, controller, and global-session policy with Daedalus-scoped authority and safety wording.
- REQ-005: Define one living workflow: FRAME, MODEL, BIND, PROVE, BUILD, RECONCILE, and SEAL.
- REQ-006: Keep SDD and TDD complementary: SDD defines intent／design／acceptance while TDD supplies executable evidence and feeds discoveries back into the SDD.
- REQ-007: Provide public installation and verification instructions that rely only on the Daedalus repository／Plugin payload.
- REQ-008: Preserve proportional lite／standard／high-risk routing and require only UML that answers a named design question.
- REQ-009: Enforce the independent packaging and pollution boundaries with local RED tests before implementation.
- REQ-010: Define deterministic `required／optional／omit` routing for six software-system UML types, including per-type non-triggers, minimum content, and removal conditions; explanatory process diagrams must not satisfy the Necessary UML gate.
- REQ-011: Require Mermaid for every decision and reader-aid UML diagram; reject PlantUML and PUML fences with a stable validation error.
- REQ-012: Require every Daedalus-managed production change to create or update repository-root `CHANGELOG.md` under `[Unreleased]` in the same diff, and record inspectable evidence in the SDD.

## Acceptance criteria

- AC-001 (REQ-001): Given the repository, when its configured artifact is built, then no `README.md`, `docs/`, `tests/`, or `lifecycle.json` member is included.
- AC-002 (REQ-002, REQ-003): Given a fresh isolated Codex profile with only Daedalus enabled, when the standalone check runs from the installed cache, then it scaffolds an SDD, validates a bundled complete example, and exits zero.
- AC-003 (REQ-004): Given all packaged text, when provenance terms are scanned, then no unrelated custom Skill, controller path, global session, branch, worktree, or subagent workflow is required.
- AC-004 (REQ-005, REQ-006): Given the Skill instructions, when workflow stages are inspected, then all seven stages exist and RECONCILE explicitly returns changed assumptions to SDD／UML before the next RED.
- AC-005 (REQ-007): Given the repository marketplace manifest and README instructions, when followed from the public repository, then `daedalus@daedalus` installs without an external local project path or validator.
- AC-006 (REQ-008): Given lite and standard templates, when scaffolded, then both retain proportional gates and standard records the workflow stages without forcing unrelated high-risk evidence.
- AC-007 (REQ-009): Given the pre-change tree, when new boundary tests run, then they fail for the missing independence contract, oversized package, stale documentation, and polluted workflow wording; after implementation the same tests pass.
- AC-008 (REQ-010): Given the UML reference and templates, when two agents inspect the same change, then each can apply observable per-type triggers and counterexamples; optional reader aids are explicitly marked and do not replace a required diagram or omission rationale.
- AC-009 (REQ-011): Given an otherwise valid SDD containing a `plantuml` or `puml` UML fence, when validation runs, then it fails with `E_UML_FORMAT`; the equivalent Mermaid fence remains valid.
- AC-010 (REQ-012): Given a Daedalus-managed production change, when the complete gate runs, then the SDD contains a Changelog section naming repository-root `CHANGELOG.md`, targeting `[Unreleased]`, and recording non-placeholder evidence; the Daedalus repository itself contains that file in the same change set.

## Constraints, assumptions, and unknowns

- Constraint: Runtime scripts use only the Python standard library and perform no network, Git, shell, or external-state mutation.
- Constraint: Existing public behavior of `init_sdd.py` and `validate_sdd.py` remains compatible.
- Assumption: Codex Plugin installation can discover `skills/daedalus` from the existing manifest.
- Assumption: Ariadne remains an external development gate and is never packaged as a Daedalus dependency.
- Constraint: Commit, push, promotion, tag, and release remain separately authorized lifecycle actions; the changelog requirement grants none of those permissions.

## Options and decision

| Option | Benefit | Cost or risk | Decision |
|---|---|---|---|
| Keep the repository root as the unrestricted payload | No layout changes | Ships tests, historical docs, lifecycle metadata, and stale evidence | Reject |
| Move runtime into a nested Plugin and migrate all paths | Strong physical separation | Large path churn without improving the existing manifest contract | Reject |
| Keep root Plugin and add an explicit package allowlist plus installed-payload self-test | Minimal compatible change; exact runtime boundary becomes machine-verifiable | Repository docs remain outside the formal artifact and need separate tests | Select |
| Split SDD and TDD into multiple cooperating Skills | Narrower individual prompts | Recreates cross-Skill dependency and installation failure modes | Reject |

The changelog extension references the human-readable repository-root convention from `olivierlacan/keep-a-changelog`. `changesets/changesets` and `googleapis/release-please` were rejected because dependency, monorepo, GitHub, and release-automation scope exceeds this structural workflow gate. Audit evidence: `/home/timshan/workspace/reuse-audits/PDCA-20260811-daedalus-changelog-gate-github-reuse-audit.md`.

## Design and contracts

The root remains the Plugin root. `.agents/plugins/marketplace.json` exposes that root through the public repository, while `package_paths` is the formal artifact allowlist. Repository-only tests, lifecycle metadata, public documentation, and historical design records remain outside the installed payload. The Skill payload consists of instructions, references, templates, standard-library scripts, and a complete example used by `self_test.py`.

The workflow contract is:

1. FRAME the observable outcome, boundaries, recovery, and risk tier.
2. MODEL the smallest sufficient living SDD and necessary UML.
3. BIND each acceptance criterion to an outer oracle and the next vertical slice.
4. PROVE the behavior is absent with an intended RED.
5. BUILD the smallest GREEN change and REFACTOR while green.
6. RECONCILE evidence with requirements, decisions, UML, traceability, and the repository-root `[Unreleased]` entry; return to MODEL if assumptions changed.
7. SEAL with fresh affected checks, realistic outcome inspection, changelog evidence, remaining risk, recovery, and complete validation.

## Necessary UML

### Component boundary

decision_question: Which files and components may an independently installed Daedalus use at runtime?
traces: REQ-001, REQ-002, REQ-003, REQ-007; AC-001, AC-002, AC-005

~~~mermaid
flowchart LR
    U[User and project] --> S[Daedalus SKILL.md]
    S --> R[Bundled references]
    S --> T[Bundled SDD templates]
    S --> C[Bundled stdlib CLIs]
    C --> P[Project SDD and tests]
    T --> P
    X[Repository docs tests lifecycle] -. excluded from Plugin artifact .-> S
    O[Other custom Skills] -. no runtime edge .-> S
~~~

## Reference diagrams

The following diagrams explain Daedalus's own method and document state. They are reader aids, not
software-system decisions, and do not satisfy the Necessary UML gate above.

### Authoring workflow reader aid

diagram_role: reader-aid
reader_aid_purpose: Explain how specification and test feedback cooperate without becoming a frozen waterfall.

~~~mermaid
flowchart TD
    F[FRAME outcome and risk] --> M[MODEL SDD and necessary UML]
    M --> B[BIND AC to outer oracle and slice]
    B --> R[PROVE intended RED]
    R --> G[BUILD GREEN]
    G --> Q[REFACTOR while green]
    Q --> C[RECONCILE evidence and design]
    C -->|assumption changed| M
    C -->|more behavior| B
    C -->|all AC satisfied| S[SEAL fresh evidence]
~~~

### SDD document-state reader aid

diagram_role: reader-aid
reader_aid_purpose: Explain the lifecycle of the SDD artifact itself; these are not runtime product states.

~~~mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> DesignReady: ready gate passes
    DesignReady --> Implementing: intended RED observed
    Implementing --> Verifying: target is green and refactored
    Verifying --> DesignReady: CHECK exposes design drift
    Verifying --> Implementing: next accepted slice
    Verifying --> Complete: SEAL and complete gate pass
    Complete --> Draft: later change reopens contract
~~~

## Failure, security, and observability

| Failure or risk | Detection | Handling or recovery |
|---|---|---|
| Repository files leak into Plugin | Artifact membership test and Ariadne payload report | Stop; correct `package_paths` and rebuild |
| Hidden custom-Skill dependency | Ariadne reference scan plus local forbidden-provenance scan | Remove the dependency; do not install it to satisfy the gate |
| Weak standalone probe | Review confirms both scaffold and validation run from installed payload | Strengthen bundled self-test before claiming independence |
| Frozen SDD blocks TDD learning | Workflow contract test requires RECONCILE feedback edge | Return to MODEL, update SDD／UML, rerun ready gate |
| Tests prove implementation detail only | AC-to-outer-oracle review and realistic outcome check | Replace or add a boundary-level oracle |
| Existing CLI behavior regresses | Existing 31 tests plus new compatibility tests | Revert focused change or restore prior version from Git |
| Production behavior changes without release-facing context | SDD Changelog section, validator errors, and Skill contract tests | Add or correct the repository-root `[Unreleased]` entry before SEAL |

## Test portfolio and TDD slices

Outer acceptance or contract oracle: Ariadne must install the exact allowlisted payload as the sole enabled Plugin and run Daedalus's bundled behavioral self-test from the installed cache.

1. RED: add boundary tests for package allowlist, independence command, bundled self-test, public documentation, clean provenance, seven-stage workflow, and mandatory changelog evidence; observe failures on the existing behavior.
2. GREEN: add package contract and self-test, clean packaged and repository text, update templates／references／README／CHANGELOG, enforce the SDD Changelog section, and bump the development manifest to 1.1.0.
3. REFACTOR: centralize standalone example use, keep scripts standard-library-only, and remove tests that institutionalize contaminated evidence.
4. CHECK: run repository tests, Skill validation, SDD ready／complete gates, scoped provenance scan, artifact inspection, Ariadne independence, and an isolated forward task.

## Traceability

| Requirement | Acceptance | Test | Implementation | Evidence |
|---|---|---|---|---|
| REQ-001 | AC-001 | tests/test_independence_contract.py | lifecycle.json | Artifact contains exactly 14 allowlisted files |
| REQ-002, REQ-003 | AC-002 | installed self-test and Ariadne independence | self_test.py, bundled example | Isolated exact-payload check passed |
| REQ-004 | AC-003 | tests/test_independence_contract.py | SKILL.md, README.md, current docs | Scoped provenance regressions and dependency scan passed |
| REQ-005, REQ-006 | AC-004 | tests/test_skill_contract.py | SKILL.md, references, templates | Seven-stage workflow regressions passed |
| REQ-007 | AC-005 | marketplace and README contract tests | marketplace.json, README.md | Public-selector contract passed |
| REQ-008 | AC-006 | tests/test_init_sdd.py | templates and risk reference | Lite／standard scaffold regressions passed |
| REQ-009 | AC-007 | recorded RED and GREEN commands | tests/ | Initial RED failed 14 assertions＋2 errors; final GREEN passes 43 tests |
| REQ-010 | AC-008 | reader-aid, routing, and no-sequence-bias regressions | risk-and-uml.md, templates, validate_sdd.py | UML regressions passed; Claude R2 findings implemented |
| REQ-011 | AC-009 | Mermaid-only format regression | risk-and-uml.md, SKILL.md, validate_sdd.py | PlantUML／PUML RED failed twice; Mermaid-only GREEN passed |
| REQ-012 | AC-010 | tests/test_skill_contract.py, tests/test_validate_sdd.py, tests/test_init_sdd.py | SKILL.md, sdd-schema.md, templates, validator, CHANGELOG.md | Changelog contract RED failed three focused assertions; GREEN passes with structural evidence |

## Rollout, rollback, and remaining risks

Rollout: implement and verify in a workspace copy, then synchronize only verified changed files through the separately authorized project lifecycle. Promotion, tagging, and release remain independent actions.

Rollback: before commit, Git diff can restore each changed file; after commit or push, revert the focused commit or restore from the current `v1.0.0` tag without rewriting history.

Remaining risks: static scans cannot detect unattributed conceptual copying; structural SDD validation cannot judge engineering correctness; an isolated forward run still evaluates agent behavior probabilistically and must be interpreted with artifact evidence.

## Changelog

CHANGELOG.md impact: `[Unreleased]` records independent packaging, the living seven-stage workflow, Mermaid-only deterministic UML, and mandatory changelog evidence.

Changelog evidence: repository-root `CHANGELOG.md` is present in the same diff and is excluded from the installable payload by `package_paths`.

## Verification evidence

- RED evidence: `python3 -m unittest tests.test_independence_contract -v` failed with 14 assertion failures and 2 errors on the v1.0.0 baseline; the Mermaid-only regression failed for PlantUML and PUML; the changelog slice then failed three focused assertions because the Skill, validator, template, and repository file lacked the new contract.
- GREEN evidence: the full suite passes after independent packaging, seven-stage workflow, deterministic UML routing, Mermaid enforcement, templates, changelog contract, and documentation were implemented.
- Refactor or exception: Historical polluted SDDs were removed from the current tree but remain recoverable from Git; runtime instructions now separate project authority from Daedalus workflow, and no TDD exception was used for executable behavior.
- Fresh verification: all 43 tests passed; Skill validation returned `Skill is valid!`; bundled `self_test.py` returned `SELF_TEST_OK`; complete structural gate and `git diff --check` passed; the final Ariadne rerun is recorded with the isolated result below.
- Realistic outcome check: Ariadne installed Daedalus 1.1.0 as the sole enabled Plugin in a fresh profile, found zero explicit references to 11 external discovered Skills, executed one bundled behavioral check from the installed cache, and bound the exact 14-file payload to SHA-256 `82aa4e39ac7095d23318c0f22b2cbf2ec5aea05a3e099f0afa134e39f4ada2a8` and artifact SHA-256 `117fd8b1f56d0f6dd45d1491c48d9e692322586b47f2615fb3e170bc6c201336`.
