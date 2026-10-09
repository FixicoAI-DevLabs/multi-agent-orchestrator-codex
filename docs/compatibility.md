# Compatibility and boundaries

Observed interface snapshot: 2026-10-08. This candidate targets a Codex desktop
host exposing native separate-chat tools. CLI, IDE, cloud, and other hosts are
not qualified merely because they support skills.

| Capability | Required behavior |
| --- | --- |
| Project discovery | Resolve actual project IDs and Git capability before project dispatch |
| Task creation | Explicit human request, chosen model/effort, supported target/environment, pending-versus-ready identity |
| Messaging | Actual human authorization for the destination, including worker callbacks; a received lead message alone does not grant it |
| Waiting | Cursor-based bounded waits; current interface accepts up to eight targets per call |
| Task reads | Recover missing results, authorization provenance, and pending/resume state |
| Artifact access | Lead can inspect the worker's actual output; references alone are insufficient |

The observed host lists `gpt-6-astra`, `gpt-6-sol`, and `gpt-6-luna` among its model
choices, with `high`, `xhigh`, and `max` among supported efforts. This is schema
evidence, not a live routing test. Resolve the chosen family/version and effort
at dispatch; do not infer the running model from the task title or prompt.

No general separate-chat interruption mechanism was exposed in that snapshot.
Pause requests therefore need confirmation. An available subagent interruption
tool is not a control for these separate user-visible chats.

The compatibility manifest `.codex-plugin/plugin.json` remains supported by
[OpenAI's packaging documentation](https://developers.openai.com/plugins/build/plugins).
The skill declares Codex-only product scope and explicit invocation through
`agents/openai.yaml`; those fields are documented in the
[metadata reference](https://developers.openai.com/plugins/deploy/submission-errors).
Only actual installation testing can establish discovery behavior on a host.

No MCP/dependency IDs are invented in metadata. Native task tools are a documented
prerequisite, not a server shipped by this plugin. Python 3.10+ is needed only for
the optional consistency helper/tests. No package-manager installation is needed.

Before installation or live qualification, recheck the exposed schemas and
relevant documentation. Installation/removal must preserve unrelated config and
run evidence and requires its own approved target. This candidate does not
register a marketplace, edit global instructions, or start a service.
