# The Multi-Agent Orchestrator — Codex

**Version 0.1.2 · Codex desktop plugin · CC0-1.0**

Plan in an Astra chat at High or Very High, assign approved work to separate Sol
High or Luna Max chats, and bring the results back to the same Astra chat for
review, correction, continuation, and final delivery.

Users may instead choose Sol as lead or request a separate planning reviewer.
Those options do not insert mandatory stages into the primary workflow.

For Claude Code, use the separate
[Claude Code edition](https://github.com/FixicoAI-DevLabs/cost-aware-session-orchestrator).
Each edition has its own installation instructions, host integration, version
history, and validation evidence.

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
lead review, and ledger checks. Installation and native skill discovery were
verified locally for 0.1.1 and the 0.1.2 naming update. The earlier 0.1.1
source-based pilot exercised Sol High authoring and Luna Max review. See the
[validation record](docs/validation.md) for the exact scopes and remaining checks.

## Start a run

To use this checkout directly, open it in a compatible Codex host and ask:

> Read and use skills/orchestrate/SKILL.md. Keep this chat as lead and plan the
> work. Show me the assignments and limits before creating worker chats.

Reading the source does not install a plugin. If a separately authorized copy
is installed and discovered, use that host's skill invocation:

Invoke the packaged `orchestrate` skill explicitly (use the installed skill name
shown by your host). Its display name is **The Multi-Agent Orchestrator**;
the existing `orchestrate` shortcut and package identifier remain compatible.
For example:

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

The [validation report](docs/validation.md) separates static checks, the installed
0.1.0 trial, the 0.1.1 source pilot, and 0.1.1/0.1.2 installation and discovery.
The [route walk-throughs](docs/routes.md) use
synthetic evidence only. Cost savings have not been measured. Limits are
lead-supervised unless a host separately provides enforcement; account-level
usage percentages must not be described as this run's cost.

## Release scope and lineage

This is a separate Codex adaptation of the concepts in
[cost-aware-session-orchestrator](https://github.com/FixicoAI-DevLabs/cost-aware-session-orchestrator),
whose source baseline is `85c371ab7d5307054fa58c0a3ade4975d8db1613`.
The Claude edition retains its own installer and history. The full original
[CC0-1.0 license](LICENSE) is preserved. This Codex edition is maintained in
`FixicoAI-DevLabs/multi-agent-orchestrator-codex`; its stable plugin identifier
remains `codex-cost-aware-orchestrator` and its skill shortcut remains
`orchestrate`. The repository name and installed display name do not change
those existing identifiers.

Installation, live task trials, publication, and persistent operation after
host shutdown are not established by static validation.
