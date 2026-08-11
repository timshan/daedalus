# Risk tier and deterministic UML routing

Read this reference before selecting an artifact or diagram.

All UML in a Daedalus SDD must use Mermaid fenced code. PlantUML and PUML are not accepted for
decision diagrams or reader aids.

## Risk tiers

| Tier | Use when | Minimum artifact |
|---|---|---|
| lite | One localized bug, refactor, or low-risk setting; no public contract, boundary, schema, trust, migration, irreversible, or numerical SLO impact | One page: current／expected, REQ／AC, focused test, diff, recovery, evidence |
| standard | Public contract or cross-module consumer changes; an external integration, data model, three or more decision branches, persistent state, or meaningful performance budget may change | Full SDD, applicable traceability, required UML or omission rationale, contract／integration evidence |
| high-risk | Authentication, authorization, secrets, payment, safety, trust boundary, irreversible data change, cross-service migration, availability, or numerical performance SLO is materially at risk | Full SDD plus independent review and applicable security, migration, rollout, monitoring, rollback, and rehearsal evidence |

Record `tier_rationale` with concrete triggers. Default to standard when classification is unclear.
Do not self-downgrade a clear security, trust-boundary, irreversible, or migration risk.

## Operational definitions

- **Public contract:** an API, event, file format, CLI, schema, or behavior consumed outside the
  implementation unit.
- **Cross-module:** a public contract is consumed by a separately owned or independently tested
  module; changing multiple files alone is not cross-module.
- **Cross-boundary:** a deployable process, external API, data-ownership boundary, or trust
  boundary is crossed.
- **Complex workflow:** three or more decision branches, or parallel, compensation, retry state,
  or persistent lifecycle exists.
- **Major performance requirement:** a stated numerical SLO, latency, throughput, memory, or cost
  budget may be affected.
- **Irreversible:** ordinary rollback cannot restore the prior data or external state.

## Three-outcome routing

The six diagram types below describe the software system being designed or built. They do not
describe the authoring workflow or the SDD document's own status lifecycle.

For each diagram type, choose exactly one outcome:

1. **required** — the row's trigger is true, at least two materially different designs or runtime
   outcomes are defensible from prose／code alone, and the diagram resolves that ambiguity. Draw or
   update the smallest decision diagram; add `decision_question` and REQ／AC `traces`.
2. **optional** — no unresolved design ambiguity exists, but a visual materially shortens
   explanation for a reader. Keep it outside the Necessary UML gate and mark it with
   `diagram_role: reader-aid` plus `reader_aid_purpose`. It does not satisfy a required diagram.
3. **omit** — neither condition is true. Draw nothing and record one concrete
   `no_diagram_rationale` covering all six types.

If an authoritative existing diagram already answers the unchanged question, link or update it;
do not create a duplicate. Risk tier alone never changes `optional` or `omit` into `required`.

## Per-type decision table

| Type | Required trigger | Explicit non-trigger／omit example | Decision question | Minimum content | Stale or removable when |
|---|---|---|---|---|---|
| Context／component | A new actor, deployable, external API, ownership boundary, or trust boundary is introduced, or responsibility moves across one, and the diff alone cannot show who owns the behavior | A private helper is added inside an existing module; ownership and boundaries do not change | Which system owns this behavior, and which ownership or trust boundary is crossed? | Only changed actors／components, owners, boundaries, and relevant edges | A depicted owner／boundary no longer matches code or deployment; remove if the boundary disappears |
| Sequence | Three or more messages across two or more participants are introduced or reordered, and retry, timeout, failure, or compensation has more than one defensible behavior | One synchronous call propagates failure and has no retry or compensation | In what order do failure-prone steps occur, and what happens to completed work after a later failure? | Only participants, messages, timeout／retry, and compensation relevant to the decision | Runtime call order diverges, or the flow becomes an unambiguous single-call path |
| Class／domain | A persistent or serialized entity, relationship, cardinality, or invariant changes and a wrong choice would require data or compatibility repair | An optional field is added without changing relationships, cardinality, or invariants | What cardinalities and invariants are legal, and what compatibility or migration follows? | Only new or changed entities, relationships, cardinalities, and invariants | Schema／migration changes invalidate it, or no modeled relationship remains |
| State machine | A runtime entity gains a state, or the same source state has multiple plausible legal／illegal transitions | A boolean flag has exactly one transition each way and no concurrent or recovery state | Which runtime transitions are legal, including plausible transitions that must be rejected? | Only affected states, transitions, guards, terminal／recovery paths | Code adds／removes a state or transition, or the lifecycle collapses to an unambiguous flag |
| Activity | Three or more decision branches, genuine parallel work, reconvergence, or compensation interact in a way not obvious from reading top to bottom | Three sequential guard clauses only stop with errors; one `if/else` has fewer than three branches | Which paths reconverge, and what must occur exactly once across all paths? | Only branches, parallel joins, reconvergence, and compensation relevant to the question | A branch／join changes, or the flow becomes linear and obvious |
| Deployment | A runtime process, container, service, network zone, scaling rule, or availability topology is introduced or changed, and reachability cannot be inferred from application code | A high-risk permission check changes inside one existing process with no new process or network exposure | Where does the changed runtime execute, what can reach it, and across which network boundary? | Only changed processes／zones, relevant network edges, scaling／availability decision | Infrastructure is split／merged or reachability changes; remove when no topology decision remains |

## Boundary examples

- A high-risk in-process authorization change with no new actor, call-order ambiguity, persistent
  entity, runtime state, three-branch flow, process, or network edge requires no UML. High risk
  changes evidence depth, not diagram count.
- Three function calls in a fixed sequence do not require a sequence diagram unless ordering or
  failure behavior has more than one defensible answer.
- Three guard clauses are not an activity-diagram trigger when every path simply stops.
- A document's `draft → complete` metadata is not a software state-machine trigger.
- The FRAME／MODEL／BIND／PROVE／BUILD／RECONCILE／SEAL method is not a software activity trigger;
  a visual of it is only a reader aid.
- A new database table may require class／domain UML but not deployment UML when no runtime process
  or network topology changes.

## Gate and maintenance rules

- Choose the smallest diagram set that resolves all required decision questions. Never require a
  fixed number of diagrams.
- Every decision diagram uses Mermaid and declares `decision_question` and `traces` containing relevant REQ and AC
  IDs. Verify names, contracts, states, and cardinality against the written SDD and implementation.
- A reader-aid diagram uses Mermaid and declares `diagram_role: reader-aid` and `reader_aid_purpose`; it carries no
  `decision_question` or REQ／AC `traces` and never replaces `no_diagram_rationale`.
- At every RECONCILE, update or remove a stale diagram. A diagram retained after its question or
  trigger disappears is documentation debt.
- A new diagram gate must name its applicable tier; otherwise it does not apply to lite work.

If no decision diagram is required, write:

~~~text
no_diagram_rationale: <why none of the six required triggers has a genuine unresolved decision>
~~~
