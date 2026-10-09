# Codex Cost-Aware Orchestrator

**Local candidate 0.1.1. Result-format clarification and first-run guide.
This source revision completed one bounded documentation pilot with Sol High
and Luna Max. Version 0.1.0 passed an earlier installed synthetic
two-worker trial. See the dated validation record for each scope.**

Plan in an Astra chat at High or Very High, assign approved work to separate Sol
High or Luna Max chats, and bring the results back to the same Astra chat for
review, correction, continuation, and final delivery.

Users may instead choose Sol as lead or request a separate planning reviewer.
Those options do not insert mandatory stages into the primary workflow.

## What the package contains

- One explicit-entry [orchestration skill](skills/orchestrate/SKILL.md).
- Lead, planning-reviewer, worker, and acceptance-review role references.
- Native coordination instructions and compact JSON/Markdown templates.
- One read-only Python validator and synthetic static tests.

The host supplies task creation, messaging, waiting, reading, and continuation.
This package does not bundle those tools, a scheduler, an MCP server, a model
runtime, or API credentials. It does not change the model of the original chat.
Native tools must actually be available; see [compatibility](docs/compatibility.md).

## First run

Start with the [first-run guide](docs/first-run.md) for prerequisites, source or
installed-skill invocation, model choices, bounded authorization, worker results,
lead review, and ledger checks. The source-based documentation pilot does not
establish installation/discovery of 0.1.1, optional routes, or measured savings.

## Intended use after separately authorized installation

Invoke the packaged `orchestrate` skill explicitly (use the installed skill name
shown by your host). For example:

> Use $orchestrate to plan this project with Astra High as lead and separate Sol
> High or Luna Max workers. Present the assignments and limits before dispatch.

The lead prepares the concrete plan, assignment boundaries, and resource limits.
Approve the named worker chats, their actions, and messages in both directions.
Then the lead dispatches, waits, checks artifacts, and continues within that
scope. A run approval is not blanket permission to publish, deploy, or delete.

Keep private run files in a declared location outside this repository. The
coordinator owns the ledger; workers write their assigned outputs and result
records. See the [record contract](skills/orchestrate/references/records.md).

## Local static checks

Python 3.10 or newer; the shipped helper and tests use only the standard library:

```sh
python -m unittest discover -s tests -v
python skills/orchestrate/scripts/validate_run.py examples/synthetic-complete.json
```

The validator never creates chats, contacts a network service, writes records,
or follows artifact references. A valid record is not proof of human approval or
successful work. Lead review remains necessary.

The [validation report](docs/validation.md) records the October 8 static checks
and installed 0.1.0 trial, the October 9 source pilot, and remaining coverage.
The [route walk-throughs](docs/routes.md) use
synthetic evidence only. Cost savings have not been measured. Limits are
lead-supervised unless a host separately provides enforcement; account-level
usage percentages must not be described as this run's cost.

## Release scope and lineage

This is a separate Codex adaptation of the concepts in
[cost-aware-session-orchestrator](https://github.com/FixicoAI-DevLabs/cost-aware-session-orchestrator),
whose source baseline is `85c371ab7d5307054fa58c0a3ade4975d8db1613`.
The original Claude repository is unchanged by this work. The full original
[CC0-1.0 license](LICENSE) is preserved; the candidate has its own local Git
repository. No remote repository or release is created by this package.

Installation, live task trials, publication, and persistent operation after
host shutdown are not established by static validation.
