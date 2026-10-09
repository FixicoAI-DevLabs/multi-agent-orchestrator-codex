# Native task protocol

## Intake and readiness

Inspect actual tool schemas. On the desktop host used for this candidate the
interface is `list_projects`, `create_thread`, `send_message_to_thread`,
`wait_threads`, and `read_thread`. Namespaces can vary. Those tools are supplied
by the host; this skill cannot call them from a standalone Python process.

Record the original chat/host, existing project and baseline, actual requested
model IDs/efforts, route, assignments, acceptance, and approved limits. Resolve
human-facing labels such as Very High against the exposed schema before
dispatch. If the original lead model cannot be verified, ask the user to confirm
it; do not claim to have changed it. Never silently substitute a different Sol
release or a default model for an explicitly selected one.

## Authorization and dispatch

Use the [approval template](../templates/approval.md). Chat creation must be
explicitly requested by the human, including target/environment and resource
scope. Approval must also cover lead messages and worker replies to the named
origin. Provide a pointer to the actual human source so the worker can verify
it. A record is a declaration, not an authentication mechanism.

Call `list_projects` before creating a project-targeted task. Use a projectless
target only for work without a repository. Use the worktree environment only
when explicitly requested and supported. Do not assume a worktree copies
uncommitted changes; provide the actual approved baseline/artifacts.

Persist dispatch intent before calling `create_thread`. Include run, plan,
assignment and attempt IDs in the creation prompt. Request the model/effort
explicitly when the user has chosen them. Record the returned host and ready
`threadId`, or pending `clientThreadId`, without conflating them. Follow required
host creation UI directives where applicable.

An unknown response is `unknown`, not failure to create. Reconcile through native
inventories/reads and exact identity before retrying. If reconciliation is
ambiguous, stop dispatch for that assignment and ask for the missing evidence.
There is no generic assumed “resolve pending task” endpoint.

## Wait, report, and continue

Give each worker its [contract](worker.md), scoped packet, and report target. Use
returned wait cursors to avoid replaying consumed output. The current desktop
wait interface accepts at most eight targets in one call; batch larger approved
waves fairly. This does not limit the whole run to eight or three workers.
Prefer waits of 30–60 seconds, interleaved with useful lead work and updates;
back off when nothing changes. Read task histories only for missing evidence.

Native messages can continue an idle original chat while the host supports that
behavior. After a lead final response, a returned result still needs identity
reconciliation and review. Do not promise that the skill remains continuously
running across app shutdown or unavailable hosts.

Preserve native turn status separately from assignment outcome and acceptance.
Check the actual artifact before accepting it. Corrections use the same logical
assignment, a new attempt, and the original limits. Workers never self-dispatch.

## Pause, resume, and close

On pause, stop new dispatch and send authorized pause requests to affected chats.
Use actual interruption controls only when exposed and authorized. A sent
message or archived chat is not proof that execution stopped. Reconcile and
report uncertain state. Never use handoff or archive as an invented cancel tool.

On resume, inspect source drift, outstanding chats, pending creation, results,
and approvals before any restart. Preserve attempts and counters. If the
approved contract changed materially, retain the prior run and create a linked
new one with the required scope; never rewrite historical approval into validity.

Apply [acceptance review](acceptance-review.md), check integrated output, and
deliver in the original chat. Unsupported savings, automatic cleanup,
publication, or background-service claims do not belong in completion reports.
