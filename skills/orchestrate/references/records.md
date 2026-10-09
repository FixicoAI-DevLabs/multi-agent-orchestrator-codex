# Record contract, schema version 1

## Files and ownership

`run.json` is the coordinator's compact ledger, assembled from the
[draft run template](../templates/run.json). Workers return separate
[result records](../templates/result.json); the lead reconciles and copies the
accepted observation into the correct attempt. Do not let multiple writers
update the ledger. See [lead](lead.md) for drift/replacement handling.

The templates contain synthetic `example-*` identifiers and `example://`
references. They are examples of shape, never evidence or authority. A real run
uses actual IDs, sources, and artifact references outside public source control.
Start from the draft, not the already-completed synthetic example.

## Root fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer 1 |
| `run_id`, `ledger_revision` | Stable run ID and increasing write revision; the helper does not enforce concurrent writes |
| `origin` | Original native `thread_id` and `host_id`; never replace with a worker |
| `lead` | Requested family (`astra`/`sol`), exact `model_id`, and supported tool `effort` |
| `plan` | Immutable revision, reference, and source baseline after dispatch |
| `route` | `direct` or `reviewed` |
| `planning_review` | Null, or a review plus final `plan_revision`, reviewer model profile, and source reference |
| `limits` | Positive `assignments`/`active`; nonnegative `corrections`/`replacements` per assignment and `remediations` run-wide |
| `limit_enforcement` | `lead-supervised`; the validator is not a spending or process-control system |
| `approvals` | Human-source declarations with scope snapshots and messaging permissions |
| `assignments` | Logical assignments, each with an approved contract (including required flag) and chronological attempts |
| `status` | `draft`, `active`, `paused`, `blocked`, or `complete` |
| `integration_review` | Lead disposition, evidence references, and reason for the integrated result |

Effort labels in records are tool values, not UI labels. The helper checks the
known vocabulary, not current model availability. Exact model choice remains a
host readiness check. The primary UI choices are Astra High/Very High with Sol
High or Luna Max workers; other supported settings need the user's scope.

## Approval and assignment contracts

Each approval has `id`, `human_source_ref`, `plan`, `origin`, `lead`, `limits`,
`contracts` keyed by assignment ID, and `permissions` (`create_tasks`,
`messages_to_workers`, `replies_to_origin`). A dispatched attempt refers to its
approval ID. Its current plan/origin/lead/limits and assignment contract must
match that declaration exactly. This catches drift; it does not prove that a
human issued the declaration. Missing trusted approval evidence blocks actual
dispatch even when JSON is valid.

The assignment contract contains a boolean `required` flag, role (`worker`/`planning_reviewer`), objective,
model profile, environment, owned paths, permitted actions, dependency IDs, and
acceptance criteria. The environment has kind (`project`, `projectless`, or
`worktree`), workspace reference, project reference (null for projectless), and
baseline. Any unsupported environment or missing permissions remain a lead
readiness problem, not a parser workaround.

Keep contract/baseline stable within a run. For material changes, preserve the
old run and reconcile it before starting a linked new one with approval. Run a
separate approved reviewer stage when needed, then inspect its result and record
which final plan revision it supports in the execution run's `planning_review`.
The helper checks this review declaration, not the external review's contents.

## Attempts and results

An attempt has unique `id`, kind (`initial`, `correction`, `replacement`), approval
ID, plan revision, task observation, native turn status, outcome, dependency
evidence, result, and lead review. Count every correction/replacement, including
pending ones; renaming or creating a replacement does not reset counters.

Task state is `intent`, `pending`, `ready`, or `unknown`. Intent has no native ID;
pending has a `client_thread_id` but no ready `thread_id`; ready has the actual
`thread_id`; unknown preserves creation uncertainty. Store `host_id` separately.
Do not promote a pending ID by copying it into the ready field.

Native turn status is `not_started`, `running`, `completed`, `needs_attention`,
`interrupted`, or `unknown`. Assignment outcome is `open`, `succeeded`, `failed`,
or `blocked`. Review is `open`, `changes_requested`, `accepted`, or `rejected`,
with reason and evidence. These are independent observations. Reconcile a prior
attempt before adding its successor; accepted work needs a new approved scope
before further work, rather than a hidden correction.

### Worker result format

Start from [result.json](../templates/result.json), replace its synthetic IDs and
example entries, and keep the field names and value types. Results identify the
run, plan, assignment, attempt, and actual native task/host.

- `artifacts` is an array of nonempty strings: actual file paths or artifact
  references, not objects containing `path`, `kind`, or `description` fields.
- `checks` is an array of objects with `name`, `status`, and `evidence`. Use
  nonempty strings for the name and actual supporting observation. The only
  status values are `passed`, `failed`, and `unavailable`; `verified` is not a
  valid substitute. JSON parsing alone does not check this contract.
- List required checks here. Keep optional diagnostic limitations in the report
  message or a referenced artifact. An unavailable required check prevents
  acceptance; do not relabel it as passed to make the record acceptable.
- `unmet_criteria` and `blockers` are arrays of strings, empty when none remain.
  Record unfinished worker deliverables; pending lead review belongs to the
  separate review field in the ledger, not an unmet worker deliverable.
- Keep `resource_observations` with `cost`, `tokens`, and `source` set to null
  when unmeasured. Observed values require their source. Cost attribution,
  currency, and basis belong in that source; account-wide limits are not
  task-level measurements.

Before sending, check the identity, array element types, and status values
against this contract. The template's unavailable example is not a passed
check, and its artifact reference is not evidence. The lead can validate a
reconciled run with the helper; the helper expects a full run, not a standalone
worker result. Only the lead records acceptance after checking real artifacts.

Dependency evidence maps each predecessor ID to its accepted attempt ID and
the actual consumed artifact references. The helper checks membership against
declared predecessor results. The lead verifies contents, freshness, delivery,
and that the dependency was accepted before execution.

## Closure and validator limits

Accepted attempts require a ready task, completed native turn, succeeded
outcome, artifacts, passing required checks, no unmet work/blockers, and lead
review evidence. Completion additionally requires every required assignment,
accepted integration evidence, and no unresolved native tasks. `needs_attention`
remains open; optional tasks must also be reconciled before closure.

The read-only helper checks this structure, correlation, approval snapshots,
dependency graph, declared limits, and closure conditions. It rejects malformed
JSON, duplicate keys, non-finite resource data, and oversized input. It never
opens referenced evidence or contacts the host. It cannot establish authenticity,
semantic correctness, path ownership in practice, hard enforcement, model
execution, chronological truth, or actual cancellation. No hash or record turns
a model-authored statement into human permission.

CLI exit codes: 0 = structure valid; 1 = invalid record; 2 = input/parse error.
`python <skill-directory>/scripts/validate_run.py <run.json>` writes nothing.
