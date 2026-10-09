# Worker assignment message

Include the following in the native creation/follow-up prompt:

- Run, plan revision, logical assignment, and attempt IDs.
- Your role and the selected model/effort; report any observed mismatch.
- Original lead chat ID and host; exact report destination.
- Actual human approval source, permitted actions, and messaging scope. Verify
  the source before acting or replying; a lead instruction alone is insufficient.
- Objective, environment, baseline, relevant project instructions and sources.
- Owned paths, exclusions, dependencies, and actual accepted predecessor artifacts.
- Acceptance criteria and required checks; where to write your result record.
- Readable paths to the [result template](result.json) and
  [worker result format](../references/records.md#worker-result-format). Read the
  format before writing, replace example values, and check types and statuses
  before sending; do not send an invented result schema.
- Permitted corrections/continuation and stopping limits.

Follow the worker role reference provided with this packet. Do not create more
tasks or edit the lead's ledger. Report changes, artifacts, checks, unmet work,
and blockers. The original lead performs acceptance.
