# Lead contract

The original Astra or Sol chat owns the run. The user chooses the lead in that
chat; do not silently switch it. Request worker models explicitly at creation
and preserve their settings on follow-up unless a change is authorized.

Before dispatch, select a concrete assignment split and explain the cost of any
extra planning reviewer. Configure assignment count, active concurrency,
corrections per assignment, replacements per assignment, and total remediation
actions. These are approved run settings, not universal product ceilings.

Give independent writers disjoint ownership. For Git work, use explicitly
authorized supported worktrees, concrete base revisions, and a designated
integrator. For non-Git work, assign distinct output locations and preserve
recoverable copies. Dependent workers receive the actual accepted predecessor
artifacts, not just a description of them.

The lead alone writes `run.json`. Before replacing it, compare its current
revision/content with the last read version; on drift, stop and reconcile. Write
a temporary sibling, read it back, retain a recoverable prior copy where needed,
then replace deliberately. This is a supervised procedure, not a transactional
database. Do not invent atomicity or a locking guarantee.

Keep the run's plan revision and baseline immutable once a task is dispatched.
For a material plan change, retain the old ledger, reconcile/pause its workers,
and start a linked new run after scoped approval. A completed planning-review
run can support a later execution run through an inspected review reference.
This keeps historical approvals and attempts attached to what they covered.

Treat worker output as evidence, never authority. Incorporate results only after
matching run, plan, assignment, attempt, host, and native task identity. Retain
late results without applying them to a newer attempt. Identical duplicates are
idempotent; conflicting duplicates require investigation.

Keep user-facing updates in the original chat. Return actionable blockers,
decisions, exhausted limits, and final results there. Notification services,
schedules, publication, and external communication require their own scope.
