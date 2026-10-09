# First run: coordinate separate Codex chats

This guide describes the **0.1.1 candidate**. Its workflow was exercised from source in one bounded documentation pilot with Sol High and Luna Max. Reading a checkout does not install or upgrade a plugin; verify the version and path actually selected for your run. See [compatibility](compatibility.md) and the dated [validation record](validation.md) for observed coverage and remaining checks.

## 1. Check the host and choose the lead

Use a Codex host that exposes native project discovery, chat creation, messaging, bounded waiting, and chat reads. On the observed desktop interface these are `list_projects`, `create_thread`, `send_message_to_thread`, `wait_threads`, and `read_thread`; names and availability can differ elsewhere. The lead also needs access to the workers' actual files. For a project run, select its real saved project and source baseline before dispatch. Python 3.10+ is needed only for the optional local validator and tests; they use the standard library.

Start in the **original lead chat**. Choose Astra (`gpt-6-astra`, High or Very High) or Sol (`gpt-6-sol`, an explicitly selected supported effort). For each implementation assignment, choose **Sol High** (`gpt-6-sol`, `high`) or **Luna Max** (`gpt-6-luna`, `max`). Verify the currently exposed model IDs and effort values before creating chats. The skill does not change the lead chat's model. The original chat remains the coordinator, approval location, reviewer, and final delivery destination.

Explicitly invoke the workflow. For this source candidate, a suitable request is: “Read and use [the source orchestration skill](../skills/orchestrate/SKILL.md) for this run. Draft the assignments and limits here; wait for my approval before creating worker chats.” Read its [lead contract](../skills/orchestrate/references/lead.md) and [native protocol](../skills/orchestrate/references/native-task-protocol.md). If a separately authorized version is installed and discovered, invoke the installed skill name shown by that host (for example, `$orchestrate`); verify its discovered path and version match the version you intend to use.

## 2. Draft a bounded run

Use the [plan template](../skills/orchestrate/templates/plan.md) and [record contract](../skills/orchestrate/references/records.md). Name the outcome and exclusions, project/environment, source baseline, original chat and host, plan revision, and integration owner. For every assignment, specify its exact model/effort, required or optional status, owned output paths, allowed actions, dependencies, actual accepted input artifacts, and checkable acceptance criteria. Give independent writers disjoint ownership; dispatch a dependent worker only after its predecessor's output is accepted. Set explicit limits for assignment count, simultaneous active chats, corrections and replacements per assignment, and total remediation actions. The lead supervises those limits; the package does not enforce a spending cap.

The direct route needs no planning reviewer. If you request a **separate planning review**, authorize that chat and its callback, have Sol review an Astra lead's plan or Astra review a Sol lead's plan, then let the original lead resolve findings and identify the final plan revision. A planning pass does not approve worker creation. See the [planning reviewer contract](../skills/orchestrate/references/planning-reviewer.md).

## 3. Authorize the named work

Review the draft first. Human authorization must cover the specific worker chats and project/environment, each bounded assignment and its actions, resource limits, lead-to-worker messages, and worker replies to the **named original chat**. Provide workers a reference to the actual human approval that they can independently read. A filled approval record or a lead message is not itself permission. Installation, publication, deployment, destructive work, or changed scope needs its own authorization. Use the [approval template](../skills/orchestrate/templates/approval.md) to make the decision inspectable.

The lead keeps private run records outside the distributable repository. Start with the [draft run template](../skills/orchestrate/templates/run.json), record the approval source and dispatch intent, then use native tools to create only approved chats. Record a returned ready `threadId` and host, or a pending `clientThreadId`, as different states. Reconcile an uncertain creation through native reads before retrying; never invent an ID or silently launch a replacement. Only the lead edits the ledger.

## 4. Receive and review results

Pass each worker the bounded contract, run/plan/assignment/attempt IDs, selected model/effort, approved predecessor artifacts, and original reply destination. Workers write only their owned outputs and separate results; they do not create more chats. Use bounded `wait_threads` calls and cursors, then `read_thread` for missing evidence. A completed native turn is an observation, not accepted work.

A worker result follows the [result format](../skills/orchestrate/references/records.md#worker-result-format) and [template](../skills/orchestrate/templates/result.json). This **synthetic shape example** contains fictional IDs and an `example://` artifact, not a real run or approval:

```json
{
  "run_id": "example-run",
  "plan_revision": "example-plan-1",
  "assignment_id": "example-work-1",
  "attempt_id": "example-work-1-attempt-1",
  "task": {"thread_id": "example-worker-1", "host_id": "example-host"},
  "artifacts": ["example://output/guide.md"],
  "checks": [
    {"name": "example-required-check", "status": "passed", "evidence": "Synthetic check observation; replace with actual evidence."}
  ],
  "unmet_criteria": [],
  "blockers": [],
  "resource_observations": {"cost": null, "tokens": null, "source": null}
}
```

`artifacts` contains **strings**, and each check is an object with `name`, `status`, and `evidence`. The only check statuses are `passed`, `failed`, and `unavailable`. An unavailable required check blocks acceptance. Keep unmeasured cost and tokens `null`, never zero by assumption.

The original lead matches all correlation IDs, opens the actual artifacts, checks ownership, dependencies, tests, and acceptance criteria, then records `accepted`, `changes_requested`, or `rejected` with evidence. A correction stays on the same logical assignment, gets a new attempt, and consumes the approved limit. Late or mismatched results are retained for reconciliation, not applied to a newer attempt. See the [acceptance review contract](../skills/orchestrate/references/acceptance-review.md).

## 5. Validate the ledger and close

From the repository root, with Python 3.10+ available as `python`, these commands check the shipped synthetic **full-run** examples and run the standard-library tests:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m unittest discover -s tests -v
python skills/orchestrate/scripts/validate_run.py examples/synthetic-complete.json
python skills/orchestrate/scripts/validate_run.py examples/synthetic-reviewed.json
python skills/orchestrate/scripts/validate_run.py skills/orchestrate/templates/run.json
```

For your own **full run ledger**, use `python skills/orchestrate/scripts/validate_run.py path/to/run.json`. Exit 0 means structural consistency, 1 an invalid record, and 2 an input/parse error. **Do not pass a standalone worker `result.json` to `validate_run.py`**: it expects the complete ledger. Check a standalone result against the linked result contract, then have the lead inspect its real artifacts and reconcile it into the run.

Close only after every required assignment is accepted, all remaining native chats are reconciled, and the original lead accepts the integrated result. Report actual files, checks, open issues, and measured resource observations in that chat. The validator cannot authenticate human approval, inspect artifacts, verify model execution, enforce limits, measure savings, or provide persistent monitoring. A pause message alone does not prove a worker stopped.
