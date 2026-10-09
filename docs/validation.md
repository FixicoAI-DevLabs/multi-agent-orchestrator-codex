# Validation report

Observations: 2026-10-08 through 2026-10-09. Candidate: 0.1.1. The October 8
result-format clarification passed static checks; the October 9 documentation
pilot exercised that source with native worker chats. At this pre-upgrade
checkpoint, 0.1.1 installation/discovery is still unqualified. The separately
installed 0.1.0 trial is recorded below. These are dated observations, not a
claim about the version installed on another user's host.

## Revision 0.1.1

The existing **56 tests passed** again, and skill-creator `quick_validate.py`
reported `Skill is valid!`. The result template now illustrates string artifact
references and a check object with an unavailable outcome. Worker and dispatch
guidance route to the exact field types and allowed status values. Validator
code, the record schema version, and workflow limits are unchanged.

The template's unavailable example must be replaced with actual observations;
it is not successful evidence. Local checks establish format consistency, not
whether future workers will follow the clarified instructions.

## 0.1.1 source-based documentation pilot — 2026-10-09

The original Astra lead at `xhigh` coordinated exactly two native worker chats
in the saved repository project. Sol at `high` authored `docs/first-run.md`.
After the lead inspected, accepted and preserved that output, Luna at `max`
independently checked links, command paths and validator exit behaviour,
result shape, and authorization/acceptance boundaries. Native turn records
confirmed the requested profiles and completion. Both workers returned to
the original lead, which accepted the review and integrated the README link.

There were two worker turns, one active worker at a time, no corrections or
replacements, and no unresolved acceptance-blocking findings. All 56 tests
passed on the guide-bearing source; the six package checks passed again after
README integration. Skill validation passed using an existing isolated
dependency. The final run ledger passed structural validation, separately
from the lead's inspection and acceptance of actual artifacts.

This finite pilot used the 0.1.1 skill from source; it did not upgrade the
installed plugin. It does not qualify optional routes, failure recovery,
larger waves, persistent operation, or cost savings. Private task identities,
results and review evidence remain outside the distributable package.

## Earlier 0.1.0 live trial

One separately authorized synthetic run used the original Astra lead at
`xhigh`, one Sol worker at `high`, and one Luna worker at `max`. The plugin was
installed and discovered by the local runtime; native session records showed
the requested profiles. Two distinct workers returned results to the original
lead, which requested one follow-up per worker and independently inspected the
artifacts before acceptance. The final ledger passed structural validation.

Sol completed the planned script refinement. Luna's checklist was correct, but
its initial result JSON used artifact objects and unsupported check-status
labels. The validator rejected that structure; Luna corrected it within the
approved limit. This observed defect motivated the 0.1.1 clarification.

This was one bounded synthetic job. Desktop picker rendering, optional routes,
failure recovery, shutdown persistence, and cost savings were not established.
Private task identities, configuration backups, and run records remain outside
the distributable package. The installed 0.1.0 copy remains separate from this
0.1.1 candidate.

## Static results

| Check | Observed result |
| --- | --- |
| Standard-library test suite | **56 tests passed** using `python -m unittest discover -s tests -v` |
| Skill-creator `quick_validate.py` | Passed: `Skill is valid!` |
| Skill metadata | Parsed successfully; Codex-only with implicit invocation disabled |
| Primary synthetic example | Validator exited 0 with the explicit authority/artifact verification caveat |
| Reviewed synthetic example | Validator exited 0 with the same caveat |
| Draft run template | Valid without invented approval or dispatched tasks |
| Package references | Local Markdown links resolve inside the package; one skill and one runtime helper |
| License | Byte-for-byte SHA-256 comparison matches the original complete CC0 license |
| Public-content static scan | No personal Windows home paths or native task UUIDs found in candidate source |
| Runtime/service registration | No MCP configuration, hooks, marketplace entry, or installed service in the package |

The tests cover missing and changed approvals, permission for worker replies,
required assignments being removed or relabelled, correlation errors, duplicate
IDs, pending/unknown creation, attention and interruption states, missing and
failed evidence, integration review, dependency failures/cycles, remediation
caps, concurrency declarations, model-role routes, malformed JSON, CLI exit
codes, and read-only behavior. They also confirm a draft can contain more than
three assignments. That is a data-model check, not measured host capacity.

During review, required/optional status was moved into the approved assignment
contract, and declared approved assignments were protected against silent
removal. Synthetic cases exercise those consistency checks.

The bundled Python lacked PyYAML, which the external skill-creator checker needs.
An already-existing isolated dependency was used for that checker and metadata
parsing. No dependency was installed. The shipped helper and all 56 tests use
only the Python standard library.

## What these results establish

This is an authored local plugin candidate with consistent package references,
synthetic records, and tested deterministic validation behavior. Static route
walk-throughs cover the primary Astra-to-Sol/Luna loop and the optional lead and
planning-review choices. The original lead retains coordination and acceptance.

The record validator checks declarations. It does not authenticate a human
message, inspect referenced artifacts, verify actual model selection, enforce
limits against a running host, or establish successful task cancellation.
Manual review of instructions is not a behavioral evaluation by a live model.
The privacy scan is bounded; release review must inspect the exact eventual
publication contents again.

## Remaining coverage and separate action scopes

- Installation/discovery of revision 0.1.1 and any removal test, preserving
  unrelated configuration and run evidence.
- Optional routes, native failure/recovery behavior, and larger approved waves.
- Attributed resource measurements against a declared baseline before any
  savings claim.
- Review of the exact public repository, files, and release before publication.

The October 8 clarification performed no worker dispatch or installation.
The separately authorized October 9 source pilot is described above. Neither
step created a remote repository or public release. Persistent execution across
host shutdown remains outside the qualified scope.

## Reproduce local checks

```sh
python -m unittest discover -s tests -v
python skills/orchestrate/scripts/validate_run.py examples/synthetic-complete.json
python skills/orchestrate/scripts/validate_run.py examples/synthetic-reviewed.json
python skills/orchestrate/scripts/validate_run.py skills/orchestrate/templates/run.json
```

Set `PYTHONDONTWRITEBYTECODE=1` to avoid bytecode output and optionally set
`ORCHESTRATOR_TEST_TMP` to an existing writable scratch directory. Tests create
temporary JSON inputs there and remove only their own temporary directories.
