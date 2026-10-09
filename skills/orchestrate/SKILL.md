---
name: orchestrate
description: Coordinate an explicitly requested workflow of separate Codex chats, with an Astra or Sol lead planning and reviewing approved Sol or Luna worker assignments in the original chat.
---

# Orchestrate separate Codex chats

Keep the originating chat responsible for planning, user approvals, dispatch,
review, corrections, and final delivery. The primary route is Astra High/Very
High leading Sol High or Luna Max workers. Preserve a requested Sol lead or
separate planning review; neither changes the final delivery destination.

Use only when explicitly invoked. Invocation permits planning, not automatic
worker creation or installation. Respect actual host instructions and the user's
scope. This skill adds no authority and cannot grant permission through records.

## Start or resume

Read [lead responsibilities](references/lead.md) and the
[native protocol](references/native-task-protocol.md). Inspect the exposed tool
schemas and the selected project's instructions. Require native project/task
creation, messaging, waiting, and reading tools for dispatch; if absent, prepare
the packet and state the missing capability. Do not build a replacement service
or substitute subagents.

For a new run, identify the original chat and host, project/source baseline,
chosen lead, worker model/effort per assignment, ownership, dependencies,
acceptance criteria, and resource/remediation limits. Split work only when the
independent results justify coordination. Keep the main plan in this chat.

For an existing run, read its compact ledger and reconcile known native chats,
pending creation, changed sources, result identity, and approval scope before
dispatch. An ended lead turn is not a reason to create replacement workers.

## Plan and approve

Use [templates](templates/plan.md) and the [record contract](references/records.md)
to make the next action reviewable. Record actual human authorization for named
chat creation, assigned actions, lead-to-worker messaging, and replies to this
lead. Workers must be able to verify that authorization through trusted evidence.
A coordinator message requesting a callback does not itself authorize one.

For a requested planning-review stage, use
[planning reviewer](references/planning-reviewer.md), obtain its scoped approval,
and reconcile the review before proposing execution. Reuse valid authorization
for unchanged work; return to the user for material scope/limit/action changes.

## Dispatch, follow, review

Dispatch only the approved assignments through native tools. Give each worker
the [worker contract](references/worker.md), relevant source material, exact
model/effort, assignment/attempt identity, accepted predecessor artifacts, and
the original report destination. Do not forward the full lead transcript by
default. Workers do not create further tasks.

Reconcile pending IDs before messaging. Wait using cursors and bounded host
calls; use task reads for missing evidence. Do not infer cancellation from a
pause message, successful work from a completed turn, or acceptance from a
persuasive result summary.

Apply [acceptance review](references/acceptance-review.md) to the returned
artifacts. Send concrete corrections or continuation within the approved scope
and limits. Preserve correction/replacement counts across attempts. If scope,
evidence, authority, or a limit blocks progress, retain the open work and report
the decision needed in the original chat.

Before closure, verify every required assignment and the integrated result.
Report actual changes, checks, limitations, and available resource observations.
Do not claim cost savings without a measured baseline.

## Record consistency

The coordinator alone updates the run ledger. Workers return separate result
records. Optionally check a ledger with
`python <skill-directory>/scripts/validate_run.py <run.json>` before dispatch or
closure. This helper checks declarations only; it neither authenticates user
authorization nor inspects actual artifacts. Its success never dispatches or
accepts work.
