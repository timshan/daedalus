from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "daedalus" / "scripts" / "validate_sdd.py"


def lite_document(*, tier: str = "lite", status: str = "design-ready") -> str:
    return textwrap.dedent(
        f"""\
        ---
        change_id: CACHE-001
        title: Fix cache key
        risk_tier: {tier}
        status: {status}
        ---

        # Fix cache key

        ## Current state and expected outcome

        Current: stale cache keys collide.
        Expected: keys are isolated by tenant.

        ## Requirements

        - REQ-001: Isolate cache keys by tenant.

        ## Acceptance criteria

        - AC-001 (REQ-001): Given two tenants, their keys do not collide.

        ## Test and recovery

        Regression test: tests/test_cache.py::test_tenant_key_isolation
        Recovery: revert the localized cache-key diff.

        ## Necessary UML

        no_diagram_rationale: Local pure-function change with no boundary, lifecycle, schema, or deployment decision.

        ## Verification evidence

        RED evidence: test fails on the old key format.
        GREEN evidence: focused regression test passes.
        Fresh verification: focused test and existing cache suite pass.
        Remaining risks: none beyond the localized key format.
        """
    )


def standard_document(*, status: str = "design-ready", pending: bool = False) -> str:
    evidence = "pending" if pending else "verified by command output"
    return textwrap.dedent(
        f"""\
        ---
        change_id: BILLING-002
        title: Add billing adapter
        risk_tier: standard
        status: {status}
        ---

        # Add billing adapter

        ## Goal and non-goals

        Goal: add one billing boundary. Non-goal: replace the provider.

        ## Current state and expected outcomes

        Current: no billing adapter. Expected: accepted charges cross one contract.

        ## Requirements

        - REQ-001: Submit a charge through the adapter.

        ## Acceptance criteria

        - AC-001 (REQ-001): Given an accepted charge, return the provider receipt.

        ## Constraints, assumptions, and unknowns

        Keep the provider SDK behind one boundary.

        ## Options and decision

        Select an adapter because it isolates the external contract.

        ## Design and contracts

        BillingPort accepts Charge and returns Receipt.

        ## Necessary UML

        decision_question: Where does the external billing boundary live?
        traces: REQ-001, AC-001

        ~~~mermaid
        sequenceDiagram
            App->>BillingPort: charge
            BillingPort-->>App: receipt
        ~~~

        ## Failure, security, and observability

        Timeouts fail closed and emit a redacted metric.

        ## Test portfolio and TDD slices

        Contract test first, then adapter integration.

        ## Traceability

        | Requirement | Acceptance | Test | Implementation | Evidence |
        |---|---|---|---|---|
        | REQ-001 | AC-001 | tests/test_billing_contract.py | src/billing_adapter.py | {evidence} |

        ## Rollout, rollback, and remaining risks

        Roll out behind configuration. Roll back by disabling the adapter.

        ## Verification evidence

        RED evidence: {evidence}
        GREEN evidence: {evidence}
        Refactor or exception: {evidence}
        Fresh verification: {evidence}
        Remaining risks: provider sandbox differs from production.
        """
    )


def high_risk_document(*, status: str = "design-ready") -> str:
    return standard_document(status=status).replace(
        "risk_tier: standard",
        "risk_tier: high-risk",
    ).replace(
        "## Failure, security, and observability",
        "## Threat, trust, data, and abuse cases\n\n"
        "Trust boundary: payment provider.\n"
        "Sensitive data or secret handling: redact provider credentials.\n"
        "Abuse case and control: reject replayed requests.\n\n"
        "## Failure, security, and observability",
    ).replace(
        "## Test portfolio and TDD slices",
        "## Migration and reconciliation\n\n"
        "Backup or restore point: reversible sandbox fixture.\n"
        "Rehearsal: sandbox migration dry run passed.\n"
        "Reconciliation: compare accepted receipts.\n"
        "Irreversible boundary: none.\n\n"
        "## Test portfolio and TDD slices",
    ).replace(
        "## Rollout, rollback, and remaining risks",
        "## Staged rollout, monitoring, and rollback\n\n"
        "Stage and stop condition: one sandbox consumer.\n"
        "Monitoring and threshold: zero duplicate receipts.\n"
        "Rollback trigger and procedure: disable the adapter.\n"
        "Independent review or approval boundary: reviewer PASS.\n\n"
        "## Rollout, rollback, and remaining risks",
    ).replace(
        "Remaining risks: provider sandbox differs from production.",
        "Security／performance／migration evidence: sandbox abuse and migration checks passed.\n"
        "Remaining risks: provider sandbox differs from production.",
    )


class ValidateSddCliTests(unittest.TestCase):
    def run_cli(
        self, content: str, *, phase: str = "ready", json_mode: bool = False
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "change.md"
            path.write_text(content, encoding="utf-8")
            command = [sys.executable, str(SCRIPT), str(path), "--phase", phase]
            if json_mode:
                command.append("--json")
            return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_valid_lite_ready_document_passes(self) -> None:
        result = self.run_cli(lite_document())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_valid_standard_ready_document_passes(self) -> None:
        result = self.run_cli(standard_document())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ready_allows_future_execution_evidence_to_be_pending(self) -> None:
        result = self.run_cli(standard_document(pending=True), phase="ready")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_numbered_second_level_headings_are_supported(self) -> None:
        numbered: list[str] = []
        counter = 0
        for line in standard_document().splitlines():
            if line.startswith("## "):
                counter += 1
                line = f"## {counter}. {line[3:]}"
            numbered.append(line)
        result = self.run_cli("\n".join(numbered) + "\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ready_ignores_cli_metavariables_inside_fenced_code(self) -> None:
        content = standard_document().replace(
            "BillingPort accepts Charge and returns Receipt.",
            "BillingPort accepts Charge and returns Receipt.\n\n"
            "~~~text\nvalidate <path> --phase <ready|complete>\n~~~",
        )
        result = self.run_cli(content)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ready_rejects_unresolved_design_marker_outside_fence(self) -> None:
        content = standard_document().replace(
            "Keep the provider SDK behind one boundary.",
            "TBD",
        )
        result = self.run_cli(content)
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_READY_PLACEHOLDER", result.stdout)

    def test_invalid_tier_has_stable_error_code(self) -> None:
        result = self.run_cli(lite_document(tier="enterprise"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_META_TIER", result.stdout)

    def test_missing_acceptance_id_is_rejected(self) -> None:
        content = lite_document().replace("AC-001", "criterion-one")
        result = self.run_cli(content)
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_ID_AC", result.stdout)

    def test_standard_requires_diagram_decision_question_or_rationale(self) -> None:
        content = standard_document().replace(
            "decision_question: Where does the external billing boundary live?",
            "diagram note removed",
        )
        result = self.run_cli(content)
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_DIAGRAM_DECISION", result.stdout)

    def test_standard_traceability_must_cover_every_requirement(self) -> None:
        content = standard_document().replace(
            "| REQ-001 | AC-001 | tests/test_billing_contract.py |",
            "| REQ-999 | AC-001 | tests/test_billing_contract.py |",
        )
        result = self.run_cli(content)
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_TRACE_REQ", result.stdout)

    def test_high_risk_ready_requires_special_sections(self) -> None:
        content = high_risk_document()
        for heading in (
            "Threat, trust, data, and abuse cases",
            "Migration and reconciliation",
            "Staged rollout, monitoring, and rollback",
        ):
            with self.subTest(heading=heading):
                missing = content.replace(f"## {heading}", f"## Removed {heading}")
                result = self.run_cli(missing, phase="ready")
                self.assertEqual(result.returncode, 1)
                self.assertIn("E_SECTION", result.stdout)

    def test_high_risk_complete_requires_special_evidence(self) -> None:
        content = high_risk_document(status="complete")
        result = self.run_cli(content, phase="complete")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        missing = content.replace(
            "Security／performance／migration evidence: sandbox abuse and migration checks passed.",
            "Security evidence intentionally omitted.",
        )
        result = self.run_cli(missing, phase="complete")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_COMPLETE_EVIDENCE", result.stdout)

    def test_each_diagram_requires_its_own_decision_and_traces(self) -> None:
        second_diagram = textwrap.dedent(
            """\

            ### Retry lifecycle

            ~~~mermaid
            stateDiagram-v2
                [*] --> Charged
            ~~~
            """
        )
        content = standard_document().replace(
            "## Failure, security, and observability",
            second_diagram + "\n## Failure, security, and observability",
        )
        result = self.run_cli(content, phase="ready")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_DIAGRAM_DECISION", result.stdout)

        missing_trace = second_diagram.replace(
            "~~~mermaid",
            "decision_question: Which retry state is legal?\ntraces: REQ-001\n\n~~~mermaid",
        )
        content = standard_document().replace(
            "## Failure, security, and observability",
            missing_trace + "\n## Failure, security, and observability",
        )
        result = self.run_cli(content, phase="ready")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_DIAGRAM_TRACE", result.stdout)

    def test_complete_phase_rejects_placeholders(self) -> None:
        result = self.run_cli(
            standard_document(status="complete", pending=True), phase="complete"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_COMPLETE_PLACEHOLDER", result.stdout)

    def test_complete_phase_requires_complete_status(self) -> None:
        result = self.run_cli(standard_document(), phase="complete")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E_COMPLETE_STATUS", result.stdout)

    def test_complete_standard_document_passes(self) -> None:
        result = self.run_cli(standard_document(status="complete"), phase="complete")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_complete_allows_pending_term_in_descriptive_prose(self) -> None:
        content = standard_document(status="complete").replace(
            "Goal: add one billing boundary.",
            "Goal: document why pending is reserved for unresolved completion evidence, then add one billing boundary.",
        )
        result = self.run_cli(content, phase="complete")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_pending_term_is_valid_in_metadata_and_diagram_fields(self) -> None:
        content = standard_document().replace(
            "title: Add billing adapter",
            "title: Resolve pending order state",
        ).replace(
            "decision_question: Where does the external billing boundary live?",
            "decision_question: Where does the pending order state cross the boundary?",
        )
        result = self.run_cli(content, phase="ready")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        lite = lite_document().replace(
            "no_diagram_rationale: Local pure-function change with no boundary, lifecycle, schema, or deployment decision.",
            "no_diagram_rationale: No external write is pending authorization, so no diagram is needed.",
        )
        result = self.run_cli(lite, phase="ready")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_json_contract_is_machine_readable(self) -> None:
        result = self.run_cli(lite_document(tier="bad"), json_mode=True)
        payload = json.loads(result.stdout)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(set(payload), {"valid", "phase", "tier", "errors"})
        self.assertFalse(payload["valid"])
        self.assertEqual(payload["phase"], "ready")
        self.assertEqual(payload["tier"], "bad")
        self.assertTrue(
            any(error["code"] == "E_META_TIER" for error in payload["errors"])
        )


if __name__ == "__main__":
    unittest.main()
