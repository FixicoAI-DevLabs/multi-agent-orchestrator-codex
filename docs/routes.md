# Static route walk-throughs

These are paper checks of instructions and synthetic records, not reports of
live model behavior. `example-*` IDs and `example://` references are fictional.

## Primary: Astra leads Sol and Luna

The user selects Astra High or Very High in the original chat. Astra defines two
independent components and their acceptance checks, proposes Sol High for one
and Luna Max for the other, and records the chosen supported model IDs/efforts.
There is no required planning-reviewer stage.

The user authorizes the two separate chats, their bounded actions, messages in
both directions, concurrency, and correction limits. Astra records intent and
dispatches. Pending creation remains pending. Returned results correlate to the
original run and attempt. Astra reads the actual artifacts, checks them, and
integrates them. See [synthetic complete record](../examples/synthetic-complete.json).

If Sol's first result fails a required check, Astra records `changes_requested`,
then sends a specific correction covered by the same approval. A new attempt
keeps the logical assignment ID and consumes its correction budget. Astra
accepts only the corrected evidence. If a limit or permission is exhausted,
Astra reports the decision needed rather than silently promoting a model or
spawning another worker. The tests exercise both outcomes as declarations.

## Sol lead, direct

The user can instead start with Sol as lead. The approval snapshot and original
chat identity reflect that choice. Sol/Luna implementation roles remain
available. Final review and delivery stay in the original Sol chat. No model is
silently changed by the skill. The synthetic test changes the declared lead and
its matching approval; this is not a live model-selection observation.

## Astra with separate Sol planning review

The user explicitly selects and authorizes a Sol planning-review chat and its
return messages. Sol critiques the strategy, dependencies, and acceptance. Astra
resolves the findings, identifies the final execution plan revision, and asks
for execution authorization if not already covered. The later execution ledger
references the reviewed plan and inspected reviewer evidence. A missing, open,
or stale review blocks the declared reviewed route. See
[synthetic reviewed record](../examples/synthetic-reviewed.json).

## Sol with separate Astra planning review

The same structure applies with Sol leading and Astra reviewing. The original
Sol chat remains responsible for approvals, worker dispatch, evidence checking,
and final delivery. The planning reviewer has no permission to launch workers
merely because it passed the plan.

## Failure and recovery decisions

| Observation | Lead action |
| --- | --- |
| Unknown creation response | Reconcile the existing task before any retry |
| Worker turn completed; artifact missing | Keep assignment unaccepted and request evidence |
| Worker needs attention | Keep it open; resolve the blocker in the original chat |
| Delayed result from an earlier attempt | Retain as historical evidence; do not apply it to the new attempt |
| Dependent worker lacks accepted inputs | Hold dispatch and deliver the actual predecessor outputs |
| Pause requested | Stop dispatch, request worker pause, and distinguish requested from confirmed stop |
| Changed scope or baseline | Preserve prior run, reconcile workers, and obtain the required new scope |
| Run looks complete but integration is unchecked | Keep it incomplete until integrated acceptance |

## First live qualification, only after separate approval

Use a small synthetic fixture from an Astra lead with one Sol High and one Luna
Max worker. Specify the exact workspace, actions, message destinations, model
IDs/efforts, maximum active tasks, and correction envelope before launch. Observe
creation, callback, artifact review, one correction, and final delivery in the
same lead. Record requested versus confirmed model information honestly.

This tests the reusable package around the established native coordination
mechanism. It is not a new feasibility investigation. Optional routes,
installation/removal, failure handling, and scale require their own observed
acceptance before advertising full support. No live test is launched by these
instructions or by the static test suite.
