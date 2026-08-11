---
change_id: EXAMPLE-001
title: Preserve tenant cache isolation
risk_tier: standard
status: complete
date: 2026-08-11
tier_rationale: The cache key is a public contract shared by separately tested modules.
affected_paths: src/cache_key.py, tests/test_cache_contract.py
---

# Preserve tenant cache isolation

## Goal and non-goals

Goal: include the tenant identifier in the shared cache key contract.

Non-goals: replace the cache backend or change eviction policy.

## Current state and expected outcomes

Current: two tenants can produce the same key for the same object identifier.

| Outcome ID | Observable expected result | Evidence |
|---|---|---|
| OUT-001 | Equal object identifiers from different tenants produce different keys | Contract test passes |

## Requirements

- REQ-001: Isolate cache keys by tenant.

## Acceptance criteria

- AC-001 (REQ-001): Given two tenants and one object identifier, when keys are generated, then the keys differ and preserve each tenant identifier.

## Constraints, assumptions, and unknowns

- Constraint: Existing single-tenant callers remain valid.
- Assumption: Tenant identifiers are already normalized strings.
- Unknown: None affecting this bounded example.

## Options and decision

| Option | Benefit | Cost or risk | Decision |
|---|---|---|---|
| Prefix the existing key with tenant ID | Small compatible contract change | Consumers must use the shared helper | Selected |
| Allocate a cache per tenant | Strong isolation | Operational complexity exceeds the requirement | Rejected |

## Design and contracts

FRAME identified a shared key contract. MODEL selected an explicit tenant prefix. BIND mapped AC-001 to a contract test. PROVE observed the collision. BUILD changed the helper and refactored duplicate formatting. RECONCILE confirmed no UML or requirement drift. SEAL reran the affected suite and inspected representative keys.

## Necessary UML

decision_question: Where is tenant identity introduced into the shared cache-key contract?
traces: REQ-001, AC-001

~~~mermaid
sequenceDiagram
    Caller->>CacheKey: build(tenant, object_id)
    CacheKey-->>Caller: tenant:object_id
~~~

## Failure, security, and observability

| Failure or risk | Detection | Handling or recovery |
|---|---|---|
| Caller bypasses helper | Contract search and affected tests | Revert the helper diff and migrate the missed caller |

## Test portfolio and TDD slices

Outer acceptance or contract oracle: `tests/test_cache_contract.py` compares keys produced through the public helper.

1. RED: the two-tenant contract test failed because both keys were `object-7`.
2. GREEN: prefixing the normalized tenant made the contract test pass.
3. REFACTOR: key formatting moved to one helper while all cache tests stayed green.
4. CHECK: traceability and the sequence diagram match the final helper contract.

## Traceability

| Requirement | Acceptance | Test | Implementation | Evidence |
|---|---|---|---|---|
| REQ-001 | AC-001 | tests/test_cache_contract.py | src/cache_key.py | focused and affected tests passed |

## Rollout, rollback, and remaining risks

Rollout: deploy the helper and its consumers together.

Rollback: revert the localized helper and caller changes.

Remaining risks: cache entries written with the old format expire naturally rather than being reused.

## Changelog

CHANGELOG.md impact: `[Unreleased]` records tenant-aware cache keys.

Changelog evidence: the same diff adds the tenant-isolation entry to repository-root `CHANGELOG.md`.

## Verification evidence

- RED evidence: focused contract test failed with two equal keys before implementation.
- GREEN evidence: focused contract test passed after tenant prefixing.
- Refactor or exception: formatting was centralized and the affected suite remained green.
- Fresh verification: focused and affected tests passed after the final refactor.
- Remaining risks: old-format cache entries are abandoned until expiry.
