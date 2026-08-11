# Risk tier and necessary UML

Read this reference before selecting an artifact or diagram.

## Risk tiers

| Tier | Use when | Minimum artifact |
|---|---|---|
| lite | One localized bug, refactor, or low-risk setting; no public contract, boundary, schema, trust, migration, irreversible, or numerical SLO impact | One page: current／expected, REQ／AC, focused test, diff, recovery, evidence |
| standard | Public contract or cross-module consumer changes; an external integration, data model, three or more decision branches, persistent state, or meaningful performance budget may change | Full SDD, applicable traceability, selected UML or rationale, contract／integration evidence |
| high-risk | Authentication, authorization, secrets, payment, safety, trust boundary, irreversible data change, cross-service migration, availability, or numerical performance SLO is materially at risk | Full SDD plus independent review and applicable security, migration, rollout, monitoring, rollback, and rehearsal evidence |

Record tier_rationale with concrete triggers. Default to standard when classification is unclear.
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

## UML selection matrix

Use Mermaid or PlantUML diagram-as-code. Every diagram must declare decision_question and traces
containing the relevant REQ and AC IDs. A diagram without a decision question is decoration.

| Diagram | Select when the decision concerns |
|---|---|
| Context／component | actors, deployables, external APIs, ownership, or trust boundaries |
| Sequence | interaction order, timeout, retry, failure, compensation, or contract handoff |
| Class／domain | entity relationships, invariants, schema, serialization, or migration mapping |
| State machine | lifecycle, legal transitions, concurrency, retry, cancellation, or recovery |
| Activity | three or more branches, parallel work, or compensation |
| Deployment | runtime process, network zone, scaling, availability, or release topology |

Choose the smallest set that resolves the design questions. Verify names, contracts, states, and
cardinality against the written SDD. If no diagram changes a decision, write:

~~~text
no_diagram_rationale: <why this change has no boundary, interaction, lifecycle, schema, or deployment decision>
~~~

Do not require a fixed number of diagrams. New diagram gates must name their applicable tier;
otherwise they do not apply to lite.
