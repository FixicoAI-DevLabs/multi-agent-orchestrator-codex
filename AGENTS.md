# Contributor scope

This repository develops a native Codex task-orchestration plugin. Work on this
repository does not itself invoke the packaged skill or authorize worker chats.

- Preserve the original lead chat as coordinator, approval location, acceptance
  reviewer, and final delivery destination.
- Preserve Astra/Sol lead choice, optional planning review, and Sol/Luna workers.
- Keep one explicitly invoked skill. Use native separate chats, not subagents as
  substitutes. Do not add a scheduler, inference runtime, server, or database.
- Keep run evidence and private task data out of distributable source. Examples
  and fixtures must be synthetic. Preserve the complete CC0 license.
- Static validation checks declarations and consistency; it cannot authenticate
  approval, inspect model execution, enforce budgets, or accept real artifacts.
- Local build permission does not authorize installation, worker creation or
  messaging, live tests, shared configuration changes, or publication.

Run `python -m unittest discover -s tests -v` and the skill-creator validator when
available. Report live checks separately. Do not silently install dependencies.
