---
change_id: DAEDALUS-001
title: Daedalus spec-led TDD development Skill
risk_tier: standard
status: complete
owner: Codex
date: 2026-08-10
last_verified: 2026-08-11
target_path: public repository root
target_repository: https://github.com/timshan/daedalus
---

# Daedalus Software Design Document

## 1. Goal and non-goals

### Goal

建立名為 **Daedalus** 的 Codex Skill，使 AI Agent 在修改 production code 前：

1. 依可操作規則判定開發風險 tier。
2. 先建立或更新 Software Design Document（SDD）。
3. 只在回答具體設計問題時建立必要 UML。
4. 先觀察正確的 RED，再依 GREEN、REFACTOR、CHECK 完成垂直 slice。
5. 以可追溯的 fresh evidence 驗證預期成果，並把設計漂移回寫 SDD。

### Non-goals

- 不取代專案既有的需求、測試、CI 或架構工具。
- 不自動建立 Git branch、worktree、PR 或執行 push。
- 不綁定第三方 MCP、網路服務、遙測或自動更新。
- 不要求每個小改動都建立完整文件或固定數量的 UML。
- 不以「測試通過」取代 security、performance、migration 等必要專項驗證。

## 2. Current state and expected outcomes

上一階段已完成 GitHub MCP prior-art audit 與兩輪 Claude 對抗審查，得到
「spec-led、risk-tiered、test-first、living-artifact loop」的 PASS 版方法，
但尚未有可安裝、可驗證、可公開散布的 Skill。

| ID | Expected outcome | Observable evidence |
|---|---|---|
| OUT-001 | Codex 能依需求觸發 Daedalus | 合法 frontmatter 涵蓋 feature、bugfix、refactor、integration、migration |
| OUT-002 | lite 不承受完整 SDD／UML 成本 | lite template、validator 與 forward test 允許一頁 artifact＋no-diagram rationale |
| OUT-003 | standard／high-risk 有可追溯設計 | REQ、AC、test、implementation、evidence 可相互對照 |
| OUT-004 | Agent 不能跳過正確 RED | Skill 明定 RED reason、oracle-strength 與例外證據 |
| OUT-005 | 產物可獨立安裝與維護 | Skill quick validation、stdlib unit tests、無 runtime dependency |
| OUT-006 | 對抗審查通過 | w5:p3 最終 REPORT verdict 為 PASS，無未關閉 blocker／high／medium |
| OUT-007 | 專案只以 main 發佈 | local／remote default branch 均為 main，沒有額外 branch |
| OUT-008 | 發佈專案與已發佈 commit 一致 | release repository 的 HEAD、clean status 與 remote URL 驗證 |

## 3. Requirements

- **REQ-001 — Triggering:** frontmatter 說明何時使用，涵蓋新增功能、bugfix、refactor、integration、migration 與技術設計。
- **REQ-002 — Risk tier:** Skill 用可操作定義自行計算 lite／standard／high-risk，不能假設外部 PDCA 已提供 tier。
- **REQ-003 — SDD-first:** production code 前建立 tier-appropriate SDD；純探索且不產生 production code 時才可暫緩。
- **REQ-004 — Necessary UML:** 每張 UML 有 decision_question 並連到 REQ／AC；無必要圖時留下 no-diagram rationale。
- **REQ-005 — Test-first:** 每個 production slice 走 RED→GREEN→REFACTOR→CHECK；RED 必須因缺少目標行為而失敗。
- **REQ-006 — Test portfolio:** 依風險選擇 acceptance、contract、integration、E2E、property／mutation、security、performance 或 migration rehearsal。
- **REQ-007 — Brownfield／flaky:** characterization 只鎖住不打算改變的鄰近行為；不得固化 defect；flaky test 不得靠 silent retry 變綠。
- **REQ-008 — Living artifact:** 設計漂移時回寫 SDD／UML／decision，不把 SDD 當一次性 gate。
- **REQ-009 — Deterministic support:** 提供零第三方 runtime dependency 的 scaffold 與 validator，錯誤有穩定代碼及非零 exit status。
- **REQ-010 — Proportionality:** lite 只要求一頁 current／expected、AC、回歸測試、diff 與 recovery；未標 tier 的新 gate 不套用 lite。
- **REQ-011 — Safe defaults:** 不自動 branch／worktree／commit／push，不執行網路、遙測、自動更新或第三方安裝。
- **REQ-012 — Distribution:** repository 有 public usage、MIT license、完整 Skill、測試與 SDD；Skill folder 內不放非執行必要文件。
- **REQ-013 — Temporal gate:** ready 階段拒絕未解的設計 placeholder，但允許尚未執行的 RED／GREEN／fresh evidence 標為 pending；complete 階段才拒絕 pending。
- **REQ-014 — Markdown compatibility:** validator 必須接受常見的數字編號二級標題，且不得把 fenced code block 內的 CLI metavariable 誤判為未完成設計。
- **REQ-015 — Placeholder precision:** complete gate 只能在完成證據與結案區域拒絕未解的 `pending` marker；需求或驗收文字若是在說明 marker 語意，不得被誤判。
- **REQ-016 — High-risk enforcement:** high-risk ready gate 必須要求 threat／trust／abuse、migration／reconciliation、staged rollout／monitoring／rollback；complete gate 另要求非 placeholder 的特殊風險證據。
- **REQ-017 — Per-diagram validation:** validator 必須逐張 diagram 驗證其就近關聯的 decision_question 與同時含 REQ／AC 的 traces，不能只採文件第一組欄位。
- **REQ-018 — Evaluation provenance:** public README 必須揭露 forward fixtures 受到全域 Eureka PDCA／SessionStart context 汙染與觀測 token 成本不可單獨歸因 Daedalus。

## 4. Acceptance criteria

- **AC-001 (REQ-001, REQ-002):** Given 低風險局部 bugfix，when Agent 套用 Skill，then 選擇 lite 並解釋 tier rationale。
- **AC-002 (REQ-003, REQ-010):** Given lite 任務，when scaffold SDD，then 保持一頁式必要欄位且不強迫 UML。
- **AC-003 (REQ-003, REQ-004):** Given standard 任務，when scaffold SDD，then 包含 design question、UML／no-diagram rationale、test portfolio 與 traceability。
- **AC-004 (REQ-005):** Given 測試因 fixture 錯誤失敗，when 執行 RED gate，then 不得進入 GREEN；先修正環境並重新觀察缺少行為的失敗。
- **AC-005 (REQ-006, REQ-007):** Given brownfield integration change，when 規劃測試，then 區分 defect regression、鄰近 characterization、contract／integration 與 flaky 處置。
- **AC-006 (REQ-008):** Given implementation 合理偏離原設計，when slice CHECK，then 更新 SDD 與追溯，不隱藏 drift。
- **AC-007 (REQ-009):** Given 缺 metadata、REQ／AC、diagram rationale 或 traceability 的 standard SDD，when ready validation，then 回傳非零及穩定錯誤代碼。
- **AC-008 (REQ-009):** Given 合格 lite 與 standard SDD，when ready／complete validation，then 回傳零。
- **AC-009 (REQ-011):** Given Skill 被套用，when 未獲授權，then 不建立 branch／worktree、不發佈、不安裝 dependency、不連網。
- **AC-010 (REQ-012):** Given final repository，when 執行 quick validation、unit tests、forward tests 與 Git 檢查，then 全部通過，w5:p3 verdict 為 PASS，遠端只有 main。
- **AC-011 (REQ-013):** Given 設計內容完整但實作尚未開始的 SDD，when ready validation，then pending execution evidence 不造成失敗；when complete validation，then 同一 pending 必須失敗。
- **AC-012 (REQ-014):** Given 使用「1. Goal」式標題並在 code fence 示範 PATH metavariable 的有效 SDD，when ready validation，then 不因格式而失敗。
- **AC-013 (REQ-015):** Given status complete 且證據已填妥的 SDD，when requirement prose 合法提到 `pending`，then complete validation 仍通過；若 completion evidence 保留 `pending`，then 必須失敗。
- **AC-014 (REQ-016):** Given high-risk SDD，when 任一特殊風險 section 缺少，then ready validation 失敗；when 特殊風險證據缺少或為 placeholder，then complete validation 失敗。
- **AC-015 (REQ-004, REQ-017):** Given 兩張 UML，when 第二張缺 decision_question 或完整 REQ／AC traces，then ready validation 失敗並指出第二張圖。
- **AC-016 (REQ-018):** Given public repository README，when 使用者閱讀 forward-test evidence，then 能看見全域 context 汙染、約 64k／96k token 觀測值，以及不可把全部成本歸因 Daedalus 的限制。

## 5. Constraints, assumptions, and unknowns

### Constraints

- Skill name 與 folder 固定為小寫 daedalus。
- Python scripts 僅使用標準函式庫。
- SKILL.md 保持薄入口；詳細 schema 與矩陣只放一層 references。
- 檔案使用 UTF-8、LF；不保存秘密值。
- 沿用上一階段 GitHub MCP audit 的 adapt 結論，不複製第三方程式碼或文字。

### Assumptions

- Codex 能讀取 Skill 相對路徑中的 references、assets 與 scripts。
- 優先沿用專案既有文件慣例，否則使用 docs/sdd/CHANGE_ID.md。
- 使用者的「發佈」代表 public MIT GitHub repository。

### Resolved unknowns

- timshan/daedalus 查核時尚不存在。
- 本次不修改全域 Codex Skills；交付可安裝 repository。

## 6. Options and decision

| Option | Benefit | Cost／risk | Decision |
|---|---|---|---|
| 整包採用 Spec Kit／Superpowers／Baseline | 功能多 | 多套 gate、branch／worktree、依賴與觸發衝突 | Rejected |
| 純 SKILL.md | 最小 | template 漂移與完成自述難驗證 | Rejected |
| 薄 Skill＋references＋assets＋stdlib scripts | 比例性、可驗證、易安裝 | 需維護簡單 schema | **Selected** |

## 7. Design and contracts

### Repository layout

~~~text
daedalus/
├── README.md
├── LICENSE
├── docs/SDD.md
├── skills/daedalus/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/templates/{sdd-lite,sdd-standard,sdd-high-risk}.md
│   ├── references/{risk-and-uml,sdd-schema,tdd-and-verification}.md
│   └── scripts/{init_sdd,validate_sdd}.py
└── tests/{test_init_sdd,test_validate_sdd}.py
~~~

### Script contracts

~~~text
init_sdd.py --tier <lite|standard|high-risk> --title <text>
            --change-id <ID> --output <path> [--force]

validate_sdd.py <path> --phase <ready|complete> [--json]
~~~

- init 預設不覆寫既有檔案；只有 --force 明確覆寫。
- validate 成功回傳 0，validation failure 回傳 1，usage／I/O error 回傳 2。
- JSON 欄位固定為 valid、phase、tier、errors。
- error 以穩定代碼呈現，例如 E_META_TIER。
- ready 只把未解設計 marker 視為未完成；complete 另把 pending 視為未完成證據。fenced code metavariable 不參與 placeholder 檢查。

## 8. Necessary UML

### 8.1 Sequence diagram

- decision_question: 哪些互動必須在 production code 前完成，哪些外部寫入只能在驗證／授權後發生？
- traces: REQ-003, REQ-005, REQ-008, REQ-011, AC-004, AC-006, AC-009

~~~mermaid
sequenceDiagram
    actor User
    participant Agent as AI Agent
    participant SDD as SDD Artifact
    participant Tests as Test Runner
    participant Code as Production Code
    participant Review as Reviewer
    participant Remote as GitHub / External State

    User->>Agent: Goal and constraints
    Agent->>SDD: Classify tier and write design
    Agent->>SDD: Validate ready gate
    Agent->>Tests: Add smallest behavioral test
    Tests-->>Agent: RED for missing behavior
    Agent->>Code: Minimal GREEN implementation
    Agent->>Tests: Fresh verification
    Tests-->>Agent: GREEN
    Agent->>Code: Refactor
    Agent->>SDD: Update traceability and drift
    Agent->>Review: Request scoped review
    Review-->>Agent: Findings or PASS
    Agent->>Remote: Publish only with authorization
~~~

### 8.2 State diagram

- decision_question: 哪些 evidence gate 控制狀態轉移，失敗時回到哪個狀態？
- traces: REQ-003, REQ-005, REQ-008, REQ-009, AC-007, AC-008

~~~mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> DesignReady: SDD ready gate passes
    DesignReady --> RedObserved: intended failure observed
    RedObserved --> Green: minimal implementation passes
    Green --> Refactored: behavior remains green
    Refactored --> Verified: fresh portfolio evidence passes
    Verified --> Reviewed: findings closed
    Reviewed --> Published: authorized external write
    DesignReady --> Draft: design gap
    RedObserved --> Draft: test reveals design error
    Green --> RedObserved: regression or weak oracle
    Verified --> Draft: implementation drift
    Reviewed --> Draft: confirmed finding
    Published --> [*]
~~~

No additional class or deployment diagram is necessary: no persistent domain model,
service deployment, database, network boundary, or runtime process topology exists.

## 9. Failure, security, and observability

| Failure mode | Prevention／detection | Recovery |
|---|---|---|
| 所有任務都被升級 | tier definitions；untagged gate 不套用 lite | 降級 artifact，保留 rationale |
| 無效 RED | RED reason＋fresh command evidence | 修正測試後重新 RED |
| 弱 oracle | standard／high-risk 列 plausible wrong result；必要時 property／mutation | 強化 assertion |
| SDD／code 漂移 | complete gate、traceability、review | 回寫 SDD／decision |
| flaky retry 假綠 | 禁止 silent retry | 修正或有追蹤證據的 quarantine |
| script 覆寫文件 | 預設拒絕 existing output | 明確 --force；Git 回復 |
| public repo 洩漏資料 | publication 前 scope／secret 檢查 | 停止發佈並撤銷受影響秘密 |

Scripts 不執行網路、shell、Git 或外部程式；測試使用 temporary directories。

## 10. Test portfolio and TDD slices

### Test portfolio

- Unit／CLI contract：Python unittest 驗證 template、no-overwrite、metadata、error codes、phase 與 JSON。
- Integration：Skill Creator quick_validate.py 驗證 Skill folder。
- Forward lite：新鮮 Agent 對局部 bugfix 使用 Skill，確認沒有完整 UML 儀式。
- Forward standard：新鮮 Agent 對跨邊界功能使用 Skill，確認必要 UML、traceability 與 RED gate。
- Review：Claude w5:p3 讀完整 repository，執行核准檢查並審到 PASS。
- Publication：檢查 clean status、HEAD、remote、default branch 與 remote branch 清單。

### TDD slices

1. **Slice A — Scaffold**
   - RED: tests 找不到 init_sdd.py／templates。
   - GREEN: template selection、placeholder substitution、no-overwrite。
2. **Slice B — Ready validation**
   - RED: 缺 metadata、section、REQ／AC、diagram rationale 的文件仍被接受。
   - GREEN: stable error codes 與 exit status。
3. **Slice C — Complete validation**
   - RED: 未解 placeholder、缺 traceability 或 fresh evidence 的 complete 文件仍通過。
   - GREEN: phase-aware checks 與 JSON。
4. **Slice D — Skill behavior**
   - RED: forward task 跳過 tier／RED，或 lite 被迫畫圖。
   - GREEN: 收緊 routing、stop conditions 與 references。

## 11. Traceability

| Requirement | Acceptance | Design／UML | Test／evidence | Implementation |
|---|---|---|---|---|
| REQ-001, REQ-002 | AC-001 | metadata、tier matrix | quick validate、forward lite | SKILL.md、risk-and-uml |
| REQ-003, REQ-004, REQ-010 | AC-002, AC-003 | sequence／state、templates | scaffold tests、forward tests | templates、init_sdd.py |
| REQ-005 | AC-004 | state transitions | forward standard、review | SKILL.md、TDD reference |
| REQ-006, REQ-007 | AC-005 | test portfolio | forward standard、review | TDD reference |
| REQ-008 | AC-006 | CHECK feedback | complete validation、review | SKILL.md、schema |
| REQ-009 | AC-007, AC-008 | CLI contracts | Python unit tests | scripts |
| REQ-011 | AC-009 | external-state boundary | source review | safety rules |
| REQ-012 | AC-010 | repository layout | all checks＋GitHub readback | repository |
| REQ-013 | AC-011 | phase-aware validation contract | ready／complete regression tests | validate_sdd.py |
| REQ-014 | AC-012 | Markdown-compatible parser | numbered-heading／fence regression tests | validate_sdd.py |
| REQ-015 | AC-013 | phase-aware placeholder scope | descriptive-prose／completion-marker regression tests | validate_sdd.py |
| REQ-016 | AC-014 | high-risk tier gates | high-risk missing-section／evidence regressions | validate_sdd.py、high-risk template |
| REQ-017 | AC-015 | per-diagram association | two-diagram decision／trace regressions | validate_sdd.py |
| REQ-018 | AC-016 | publication transparency | README contract test | README.md |

## 12. Rollout, rollback, and remaining risks

### Rollout

1. 完成 unit／integration／forward tests。
2. 由 w5:p3 對完整 repository 做 scoped review，確認 contract 與 source integrity。
3. 僅在 PASS 後把 reviewed tree 放入 release repository，初始化唯一的 main。
4. 在 D 槽 checkout 重跑 final validation，建立單一 main commit。
5. 建立 public GitHub repository 並直接 push main，不建立 PR 或其他 branch。
6. 讀回 default branch、remote heads、clean status 與 HEAD 一致性。

### Rollback

- GitHub 建立前：staging 不影響既有專案；不自動刪除。
- GitHub 建立後：若 verification 失敗，停止重送，保留 commit 與錯誤證據再決定。
- D 槽目的地原本不存在；copy 失敗時保留 staging 與 GitHub commit。

### Remaining risks

- validator 只能驗證 artifact 結構，不能證明設計正確。
- Mermaid render 取決於平台；原始碼仍可版本控制。
- repository 名稱與 default branch 會在 publication 時再次讀回。

## 13. Verification evidence

本節在每個 slice 後回寫；所有驗收完成且 w5:p3 PASS 後才將 status 改為 complete。

- RED evidence: Initial implementation cycle began with 19 tests; 17 failed or errored because the Skill and scripts did not exist, while 2 incidental assertions passed. Later regressions independently produced RED for ready-phase execution evidence, numbered headings, fenced metavariables, descriptive marker prose, high-risk omissions, multi-diagram omissions, legitimate metadata wording, and public provenance before their fixes.
- GREEN evidence: On 2026-08-11, `python3 -m unittest discover -s tests -v` completed 29 tests with `OK`, including the original 24 checks and five R1 closure regressions for high-risk sections／evidence, per-diagram metadata, legitimate metadata wording, and public forward-test provenance.
- Refactor or exception: Phase-aware placeholder handling, numbered-heading normalization, and fenced-code exclusion were introduced only after focused regressions. No TDD exception was used for the executable scripts.
- Fresh verification: On 2026-08-11, the 29-test suite passed; Skill Creator `quick_validate.py skills/daedalus` returned `Skill is valid!`; the project ready gate returned `valid: true`; and both retained forward fixtures still passed their complete gates after the validator revision.
- Forward tests: A fresh lite task preserved payload-key case with 2 tests passing and a valid lite complete gate. A fresh standard Checkout／PaymentGateway task added an idempotency contract with 3 tests passing, `compileall` exit 0, necessary sequence UML, and a valid standard complete gate. The nested agents also loaded global Eureka PDCA／SessionStart context and consumed approximately 64k and 96k tokens; review must treat this as evaluation contamination and a proportionality risk rather than attributing all overhead to Daedalus.
- Adversarial review: Existing reviewer `w5:p3` R1b returned REVISE with R-01 blocker, R-02 high, R-03／R-04 medium, and optional R-05 low. After TDD fixes, R2 returned PASS and independently closed R-01～R-04 with 29 tests; no blocker／high／medium finding remains. Both rounds passed report contract and source／runtime integrity. R1's four unapproved read-only Git commands were corrected and disclosed in its report; R2 ran zero unapproved commands. R-05 remains an accepted, documented low risk for explicit `--force` only.
- GitHub publication: The reviewed tree was placed in the release repository, initialized directly as main, committed as `2398c57`, and pushed to the public `https://github.com/timshan/daedalus`. GitHub readback confirmed visibility PUBLIC, default branch main, and exactly one remote head (`refs/heads/main`). After this completion-evidence commit is pushed, controller checks must again confirm local HEAD equals remote main and the release checkout is clean; the exact final hash is recorded in the Eureka PDCA log to avoid a self-referential commit hash.
- Remaining risks: The validator proves structure rather than design truth; forward tests were contaminated by global hooks and are not a clean cost benchmark; explicit `init_sdd.py --force` follows an existing symlink; and existing reviewer mode cannot prevent previously accumulated reads or unapproved read-only commands. These are documented residual limitations, not unresolved blocker／high／medium findings.
