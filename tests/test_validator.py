from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/orchestrate/scripts/validate_run.py"
spec = importlib.util.spec_from_file_location("validate_run", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def fixture(name="examples/synthetic-complete.json"):
    return validator.load_record(ROOT / name)


def current(run, assignment=0):
    return run["assignments"][assignment]["attempts"][-1]


def add_correction(run, kind="correction"):
    old = current(run)
    old["review"]["disposition"] = "changes_requested"
    old["outcome"] = "failed"
    old["result"]["checks"][0]["status"] = "failed"
    new = deepcopy(old)
    new.update(id="work-1-attempt-2", kind=kind, outcome="succeeded")
    new["result"]["attempt_id"] = new["id"]
    new["result"]["checks"][0]["status"] = "passed"
    new["review"]["disposition"] = "accepted"
    if kind == "replacement":
        new["task"]["thread_id"] = "example-replacement"
        new["result"]["task"]["thread_id"] = "example-replacement"
    run["assignments"][0]["attempts"].append(new)


class RunChecks(unittest.TestCase):
    def assertInvalid(self, run, fragment):
        errors = validator.validate(run)
        self.assertTrue(errors, "expected invalid declaration")
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_primary_astra_sol_luna_complete(self):
        self.assertEqual(validator.validate(fixture()), [])

    def test_draft_requires_no_fake_approval(self):
        self.assertEqual(validator.validate(fixture("skills/orchestrate/templates/run.json")), [])

    def test_intent_template_remains_undispatched(self):
        run = fixture("skills/orchestrate/templates/run.json")
        run["assignments"][0]["attempts"] = [fixture("skills/orchestrate/templates/attempt.json")]
        self.assertEqual(validator.validate(run), [])

    def test_optional_sol_lead(self):
        run = fixture()
        run["lead"] = {"family": "sol", "model_id": "gpt-6-sol", "effort": "high"}
        run["approvals"][0]["lead"] = deepcopy(run["lead"])
        self.assertEqual(validator.validate(run), [])

    def test_astra_with_sol_review(self):
        self.assertEqual(validator.validate(fixture("examples/synthetic-reviewed.json")), [])

    def test_sol_with_astra_review(self):
        run = fixture("examples/synthetic-reviewed.json")
        run["lead"] = {"family": "sol", "model_id": "gpt-6-sol", "effort": "high"}
        run["approvals"][0]["lead"] = deepcopy(run["lead"])
        run["planning_review"]["reviewer"] = {"family": "astra", "model_id": "gpt-6-astra", "effort": "xhigh"}
        self.assertEqual(validator.validate(run), [])

    def test_review_stage_cannot_be_skipped(self):
        run = fixture()
        run["route"] = "reviewed"
        self.assertInvalid(run, "required planning review missing")

    def test_stale_planning_review_cannot_pass(self):
        run = fixture("examples/synthetic-reviewed.json")
        run["planning_review"]["plan_revision"] = "old-plan"
        self.assertInvalid(run, "not accepted for current plan")

    def test_planning_review_with_open_findings_blocks_dispatch(self):
        run = fixture("examples/synthetic-reviewed.json")
        run["planning_review"]["disposition"] = "changes_requested"
        self.assertInvalid(run, "not accepted for current plan")

    def test_missing_approval_blocks_dispatched_record(self):
        run = fixture()
        run["approvals"] = []
        self.assertInvalid(run, "missing approval declaration")

    def test_each_messaging_and_creation_permission_matters(self):
        for permission in ("create_tasks", "messages_to_workers", "replies_to_origin"):
            with self.subTest(permission=permission):
                run = fixture()
                run["approvals"][0]["permissions"][permission] = False
                self.assertInvalid(run, "messaging not approved")

    def test_missing_human_source_is_invalid(self):
        run = fixture()
        run["approvals"][0]["human_source_ref"] = ""
        self.assertInvalid(run, "human_source_ref")

    def test_changed_plan_or_baseline_invalidates_snapshot(self):
        for key in ("revision", "baseline"):
            with self.subTest(key=key):
                run = fixture()
                run["plan"][key] = "changed"
                self.assertInvalid(run, "approval scope mismatch: plan")

    def test_changed_model_actions_or_target_invalidates_snapshot(self):
        for key, value in (("model", {"family": "sol", "model_id": "gpt-6.1-sol", "effort": "high"}),
                           ("actions", ["publish"]), ("owned_paths", ["another-component/"]),
                           ("required", False)):
            with self.subTest(key=key):
                run = fixture()
                run["assignments"][0]["contract"][key] = value
                self.assertInvalid(run, "approval contract mismatch")

    def test_required_assignment_cannot_be_silently_removed(self):
        run = fixture()
        run["assignments"].pop()
        self.assertInvalid(run, "approved assignment removed")

    def test_changed_limits_need_new_approval(self):
        run = fixture()
        run["limits"]["active"] = 10
        self.assertInvalid(run, "approval scope mismatch: limits")

    def test_unchanged_approval_reused_for_correction(self):
        run = fixture()
        add_correction(run)
        self.assertEqual(validator.validate(run), [])

    def test_replacement_preserves_logical_assignment(self):
        run = fixture()
        add_correction(run, "replacement")
        self.assertEqual(validator.validate(run), [])

    def test_correction_limit_is_per_logical_assignment(self):
        run = fixture()
        add_correction(run)
        run["limits"]["corrections"] = 0
        run["approvals"][0]["limits"] = deepcopy(run["limits"])
        self.assertInvalid(run, "correction limit exceeded")

    def test_replacement_limit_is_not_reset_by_task_id(self):
        run = fixture()
        add_correction(run, "replacement")
        run["limits"]["replacements"] = 0
        run["approvals"][0]["limits"] = deepcopy(run["limits"])
        self.assertInvalid(run, "replacement limit exceeded")

    def test_run_wide_remediation_cap(self):
        run = fixture()
        add_correction(run)
        run["limits"]["remediations"] = 0
        run["approvals"][0]["limits"] = deepcopy(run["limits"])
        self.assertInvalid(run, "remediation limit exceeded")

    def test_wrong_or_delayed_result_is_not_accepted(self):
        for key in ("run_id", "plan_revision", "assignment_id", "attempt_id"):
            with self.subTest(key=key):
                run = fixture()
                current(run)["result"][key] = "old-or-other"
                self.assertInvalid(run, "result identity mismatch")

    def test_wrong_task_or_host_is_not_accepted(self):
        for key in ("thread_id", "host_id"):
            with self.subTest(key=key):
                run = fixture()
                current(run)["result"]["task"][key] = "other"
                self.assertInvalid(run, "result task mismatch")

    def test_duplicate_attempt_id_cannot_accept_twice(self):
        run = fixture()
        current(run, 1)["id"] = current(run)["id"]
        self.assertInvalid(run, "duplicate attempt id")

    def test_duplicate_approval_id_not_silently_overwritten(self):
        run = fixture()
        run["approvals"].append(deepcopy(run["approvals"][0]))
        self.assertInvalid(run, "duplicate approval id")

    def test_native_task_cannot_belong_to_two_assignments(self):
        run = fixture()
        current(run, 1)["task"] = deepcopy(current(run)["task"])
        self.assertInvalid(run, "task assigned to two")

    def test_origin_is_not_worker(self):
        run = fixture()
        current(run)["task"]["thread_id"] = run["origin"]["thread_id"]
        self.assertInvalid(run, "worker task is origin")

    def test_pending_creation_is_valid_open_state(self):
        run = fixture()
        run["status"] = "active"
        attempt = current(run)
        attempt["task"].update(state="pending", thread_id=None, client_thread_id="example-pending")
        attempt.update(turn_status="not_started", outcome="open", result=None,
                       review={"disposition": "open", "evidence": [], "reason": "Creation pending."})
        self.assertEqual(validator.validate(run), [])
        run["status"] = "complete"
        self.assertInvalid(run, "completion with unresolved")

    def test_pending_id_is_not_ready_id(self):
        run = fixture()
        current(run)["task"]["client_thread_id"] = current(run)["task"]["thread_id"]
        self.assertInvalid(run, "pending ID reused as ready")

    def test_unknown_creation_requires_reconciliation(self):
        run = fixture()
        attempt = current(run)
        attempt["task"].update(state="unknown", thread_id=None)
        attempt.update(turn_status="unknown", outcome="open", result=None,
                       review={"disposition": "open", "evidence": [], "reason": "Creation uncertain."})
        self.assertInvalid(run, "completion with unresolved")

    def test_attention_or_interruption_does_not_equal_acceptance(self):
        for status in ("needs_attention", "interrupted", "unknown", "running"):
            with self.subTest(status=status):
                run = fixture()
                current(run)["turn_status"] = status
                self.assertInvalid(run, "accepted work is not completed success")

    def test_finished_turn_alone_does_not_close_required_work(self):
        run = fixture()
        current(run)["review"]["disposition"] = "open"
        self.assertInvalid(run, "required assignment not accepted")

    def test_failed_or_missing_evidence_prevents_acceptance(self):
        for mutation, fragment in (
            (lambda a: a.update(result=None), "acceptance missing result"),
            (lambda a: a["result"].update(artifacts=[]), "acceptance missing artifact"),
            (lambda a: a["result"]["checks"][0].update(status="failed"), "failed/unavailable check"),
            (lambda a: a["result"].update(unmet_criteria=["unfinished"]), "acceptance has unmet work"),
            (lambda a: a["result"].update(blockers=["blocked"]), "acceptance has unmet work"),
            (lambda a: a["review"].update(evidence=[]), "acceptance missing evidence"),
        ):
            with self.subTest(fragment=fragment):
                run = fixture()
                mutation(current(run))
                self.assertInvalid(run, fragment)

    def test_integration_review_is_required(self):
        run = fixture()
        run["integration_review"]["disposition"] = "open"
        self.assertInvalid(run, "integrated result not accepted")

    def test_real_predecessor_references_required(self):
        run = fixture("tests/fixtures/dependent-complete.json")
        self.assertEqual(validator.validate(run), [])
        current(run, 1)["dependency_evidence"]["work-1"]["artifacts"] = ["example://invented-artifact"]
        self.assertInvalid(run, "predecessor artifacts mismatch")

    def test_unaccepted_predecessor_blocks_dependent(self):
        run = fixture("tests/fixtures/dependent-complete.json")
        current(run)["review"]["disposition"] = "changes_requested"
        self.assertInvalid(run, "predecessor not accepted")

    def test_dependency_cycles_and_missing_predecessors(self):
        for dependency in ("work-2", "missing-work"):
            with self.subTest(dependency=dependency):
                run = fixture("tests/fixtures/dependent-complete.json")
                run["assignments"][0]["contract"]["dependencies"] = [dependency]
                self.assertInvalid(run, "cyclic or unresolved dependencies")

    def test_concurrency_limit_counts_unresolved_work(self):
        run = fixture()
        run["status"] = "active"
        run["limits"]["active"] = 1
        run["approvals"][0]["limits"] = deepcopy(run["limits"])
        for assignment in run["assignments"]:
            attempt = assignment["attempts"][0]
            attempt.update(turn_status="running", outcome="open", result=None,
                           review={"disposition": "open", "evidence": [], "reason": "Running."})
        self.assertInvalid(run, "active concurrency limit exceeded")

    def test_replacement_cannot_hide_still_running_predecessor(self):
        run = fixture()
        add_correction(run, "replacement")
        run["assignments"][0]["attempts"][0]["turn_status"] = "running"
        self.assertInvalid(run, "predecessor attempt still unresolved")

    def test_no_architectural_three_task_ceiling(self):
        run = fixture("skills/orchestrate/templates/run.json")
        run["limits"].update(assignments=12, active=10)
        original = deepcopy(run["assignments"][0])
        run["assignments"] = []
        for n in range(12):
            item = deepcopy(original)
            item["id"] = f"work-{n}"
            run["assignments"].append(item)
        self.assertEqual(validator.validate(run), [])

    def test_unavailable_resources_remain_null(self):
        run = fixture()
        self.assertIsNone(current(run)["result"]["resource_observations"]["cost"])
        self.assertEqual(validator.validate(run), [])
        current(run)["result"]["resource_observations"]["cost"] = 1
        self.assertInvalid(run, "resource_observations.source")

    def test_nonfinite_or_boolean_resource_values_are_invalid(self):
        for amount in (True, float("inf"), float("nan"), -1):
            with self.subTest(amount=amount):
                run = fixture()
                current(run)["result"]["resource_observations"].update(cost=amount, source="example://usage")
                self.assertInvalid(run, "invalid resource observation")

    def test_malformed_types_do_not_crash(self):
        for key in ("origin", "lead", "plan", "route", "limits", "assignments", "approvals", "integration_review"):
            with self.subTest(key=key):
                run = fixture()
                run[key] = None
                self.assertTrue(validator.validate(run))
        self.assertTrue(validator.validate([]))

    def test_missing_root_fields_report_errors(self):
        for key in fixture():
            run = fixture()
            del run[key]
            self.assertTrue(validator.validate(run), key)

    def test_validation_never_mutates_records(self):
        run = fixture()
        before = deepcopy(run)
        validator.validate(run)
        self.assertEqual(run, before)


class CommandChecks(unittest.TestCase):
    def invoke(self, content):
        parent = os.environ.get("ORCHESTRATOR_TEST_TMP")
        with tempfile.TemporaryDirectory(prefix="orchestrator-tests-", dir=parent) as directory:
            path = Path(directory) / "input.json"
            path.write_text(content, encoding="utf-8")
            before = path.read_bytes()
            process = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(sorted(p.name for p in Path(directory).iterdir()), ["input.json"])
            return process

    def test_cli_valid_record_and_explicit_limit_message(self):
        process = self.invoke(json.dumps(fixture()))
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("independently verify human authority", process.stdout)

    def test_cli_invalid_record_exit_one(self):
        process = self.invoke("{}")
        self.assertEqual(process.returncode, 1)

    def test_cli_parse_errors_exit_two(self):
        for content in ('{"x": 1, "x": 2}', '{"x": NaN}', '{"x": Infinity}', '{bad'):
            with self.subTest(content=content):
                process = self.invoke(content)
                self.assertEqual(process.returncode, 2)
                self.assertNotIn("Traceback", process.stderr)

    def test_cli_oversized_input(self):
        process = self.invoke(" " * (validator.MAX_BYTES + 1))
        self.assertEqual(process.returncode, 2)

    def test_cli_missing_file(self):
        process = subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "nonexistent-record.json")],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)


if __name__ == "__main__":
    unittest.main()
