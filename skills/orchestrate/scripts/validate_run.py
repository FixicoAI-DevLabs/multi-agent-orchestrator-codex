#!/usr/bin/env python3
"""Read-only declaration checks. Does not authenticate approval or inspect artifacts."""

import argparse
import json
import math
from pathlib import Path
import sys

VERSION = 1
MAX_BYTES = 2_000_000
DISPOSITIONS = {"open", "changes_requested", "accepted", "rejected"}
EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
LIMIT_KEYS = {"assignments", "active", "corrections", "replacements", "remediations"}


class ShapeError(ValueError):
    pass


def obj(value, path, keys):
    if not isinstance(value, dict):
        raise ShapeError(f"{path}: expected object")
    missing = set(keys) - value.keys()
    if missing:
        raise ShapeError(f"{path}: missing {', '.join(sorted(missing))}")
    return value


def seq(value, path):
    if not isinstance(value, list):
        raise ShapeError(f"{path}: expected array")
    return value


def text(value, path):
    if not isinstance(value, str) or not value.strip():
        raise ShapeError(f"{path}: expected nonempty string")
    return value


def texts(value, path, nonempty=False):
    seq(value, path)
    if nonempty and not value:
        raise ShapeError(f"{path}: expected nonempty array")
    for item in value:
        text(item, path)
    if len(set(value)) != len(value):
        raise ShapeError(f"{path}: duplicate value")
    return value


def integer(value, path, minimum=0):
    if type(value) is not int or value < minimum:
        raise ShapeError(f"{path}: expected integer >= {minimum}")


def boolean(value, path):
    if type(value) is not bool:
        raise ShapeError(f"{path}: expected boolean")


def choice(value, path, choices):
    text(value, path)
    if value not in choices:
        raise ShapeError(f"{path}: invalid value {value!r}")


def identity(value, path):
    obj(value, path, {"thread_id", "host_id"})
    for field in ("thread_id", "host_id"):
        text(value[field], f"{path}.{field}")


def profile(value, path, families):
    obj(value, path, {"family", "model_id", "effort"})
    choice(value["family"], path + ".family", families)
    text(value["model_id"], path + ".model_id")
    choice(value["effort"], path + ".effort", EFFORTS)


def review(value, path):
    obj(value, path, {"disposition", "evidence", "reason"})
    choice(value["disposition"], path + ".disposition", DISPOSITIONS)
    texts(value["evidence"], path + ".evidence")
    text(value["reason"], path + ".reason")


def contract(value, path):
    obj(value, path, {"required", "role", "objective", "model", "environment", "owned_paths",
                      "actions", "dependencies", "acceptance"})
    boolean(value["required"], path + ".required")
    choice(value["role"], path + ".role", {"worker", "planning_reviewer"})
    families = {"sol", "luna"} if value["role"] == "worker" else {"astra", "sol"}
    profile(value["model"], path + ".model", families)
    text(value["objective"], path + ".objective")
    env = obj(value["environment"], path + ".environment",
              {"kind", "workspace_ref", "project_ref", "baseline"})
    choice(env["kind"], path + ".environment.kind", {"project", "projectless", "worktree"})
    text(env["workspace_ref"], path + ".environment.workspace_ref")
    text(env["baseline"], path + ".environment.baseline")
    if env["kind"] != "projectless":
        text(env["project_ref"], path + ".environment.project_ref")
    elif env["project_ref"] is not None:
        raise ShapeError(path + ".environment.project_ref: projectless must use null")
    for key in ("owned_paths", "actions", "dependencies", "acceptance"):
        texts(value[key], path + "." + key, nonempty=key in {"actions", "acceptance"})


def validate(data):
    """Return errors, never mutate input. Success covers declarations only."""
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    try:
        obj(data, "run", {"schema_version", "run_id", "ledger_revision", "origin",
                          "lead", "plan", "route", "planning_review", "limits",
                          "limit_enforcement", "approvals", "assignments", "status",
                          "integration_review"})
        require(type(data["schema_version"]) is int and data["schema_version"] == VERSION,
                "run.schema_version: unsupported version")
        text(data["run_id"], "run.run_id")
        integer(data["ledger_revision"], "run.ledger_revision", 1)
        identity(data["origin"], "run.origin")
        profile(data["lead"], "run.lead", {"astra", "sol"})
        plan = obj(data["plan"], "run.plan", {"revision", "reference", "baseline"})
        for key in plan:
            text(plan[key], "run.plan." + key)
        choice(data["route"], "run.route", {"direct", "reviewed"})
        choice(data["status"], "run.status", {"draft", "active", "paused", "blocked", "complete"})
        choice(data["limit_enforcement"], "run.limit_enforcement", {"lead-supervised"})
        limits = obj(data["limits"], "run.limits", LIMIT_KEYS)
        for key in LIMIT_KEYS:
            integer(limits[key], "run.limits." + key, 1 if key in {"assignments", "active"} else 0)
        review(data["integration_review"], "run.integration_review")
        pr = data["planning_review"]
        if pr is not None:
            review(pr, "run.planning_review")
            obj(pr, "run.planning_review", {"plan_revision", "reviewer", "source_ref"})
            text(pr["plan_revision"], "run.planning_review.plan_revision")
            profile(pr["reviewer"], "run.planning_review.reviewer", {"astra", "sol"})
            text(pr["source_ref"], "run.planning_review.source_ref")

        approvals = {}
        for i, approval in enumerate(seq(data["approvals"], "run.approvals")):
            p = f"approvals[{i}]"
            obj(approval, p, {"id", "human_source_ref", "plan", "origin", "lead",
                              "limits", "contracts", "permissions"})
            aid = text(approval["id"], p + ".id")
            text(approval["human_source_ref"], p + ".human_source_ref")
            require(aid not in approvals, p + ": duplicate approval id")
            obj(approval["contracts"], p + ".contracts", set())
            for key, value in approval["contracts"].items():
                text(key, p + ".contracts key")
                contract(value, p + ".contracts." + key)
            permissions = obj(approval["permissions"], p + ".permissions",
                              {"create_tasks", "messages_to_workers", "replies_to_origin"})
            for key in ("create_tasks", "messages_to_workers", "replies_to_origin"):
                boolean(permissions[key], p + ".permissions." + key)
            approvals[aid] = approval

        assignments = {}
        for i, assignment in enumerate(seq(data["assignments"], "run.assignments")):
            p = f"assignments[{i}]"
            obj(assignment, p, {"id", "contract", "attempts"})
            aid = text(assignment["id"], p + ".id")
            contract(assignment["contract"], p + ".contract")
            seq(assignment["attempts"], p + ".attempts")
            require(aid not in assignments, p + ": duplicate assignment id")
            assignments[aid] = assignment
        require(len(data["assignments"]) <= limits["assignments"], "run: assignment limit exceeded")
        for approval in approvals.values():
            for aid, approved_contract in approval["contracts"].items():
                require(aid in assignments, f"{aid}: approved assignment removed from run")
                if aid in assignments:
                    require(approved_contract == assignments[aid]["contract"],
                            f"{aid}: approval contract mismatch")

        # Kahn's algorithm avoids recursion on long dependency chains.
        deps = {key: set(a["contract"]["dependencies"]) for key, a in assignments.items()}
        for key, dependencies in deps.items():
            require(dependencies <= assignments.keys(), f"{key}: unknown dependency")
        pending = {key: set(value) for key, value in deps.items()}
        while pending:
            ready = {key for key, value in pending.items() if not value}
            if not ready:
                require(False, "run: cyclic or unresolved dependencies")
                break
            pending = {key: value - ready for key, value in pending.items() if key not in ready}

        attempt_ids, live, task_owners = set(), set(), {}
        latest = {}
        dependencies_to_check = []
        remediations = 0
        dispatched_workers = False
        for aid, assignment in assignments.items():
            corrections = replacements = 0
            attempts = assignment["attempts"]
            for i, attempt in enumerate(attempts):
                p = f"{aid}.attempts[{i}]"
                obj(attempt, p, {"id", "kind", "approval_id", "plan_revision", "task",
                                  "turn_status", "outcome", "dependency_evidence", "result", "review"})
                attempt_id = text(attempt["id"], p + ".id")
                require(attempt_id not in attempt_ids, p + ": duplicate attempt id")
                attempt_ids.add(attempt_id)
                choice(attempt["kind"], p + ".kind", {"initial", "correction", "replacement"})
                require((i == 0) == (attempt["kind"] == "initial"), p + ": invalid attempt sequence")
                corrections += attempt["kind"] == "correction"
                replacements += attempt["kind"] == "replacement"
                require(attempt["plan_revision"] == plan["revision"], p + ": stale plan revision")
                task = obj(attempt["task"], p + ".task",
                           {"state", "thread_id", "client_thread_id", "host_id"})
                choice(task["state"], p + ".task.state", {"intent", "pending", "ready", "unknown"})
                text(task["host_id"], p + ".task.host_id")
                for key in ("thread_id", "client_thread_id"):
                    if task[key] is not None:
                        text(task[key], p + ".task." + key)
                if task["state"] == "ready":
                    text(task["thread_id"], p + ".task.thread_id")
                    require(task["client_thread_id"] != task["thread_id"], p + ": pending ID reused as ready ID")
                    task_key = (task["host_id"], task["thread_id"])
                    require(task_key != (data["origin"]["host_id"], data["origin"]["thread_id"]),
                            p + ": worker task is origin")
                    require(task_owners.get(task_key, aid) == aid, p + ": task assigned to two logical assignments")
                    task_owners[task_key] = aid
                else:
                    require(task["thread_id"] is None, p + ": non-ready task has ready ID")
                if task["state"] == "pending":
                    text(task["client_thread_id"], p + ".task.client_thread_id")
                if task["state"] == "intent":
                    require(task["client_thread_id"] is None, p + ": intent already has pending ID")

                choice(attempt["turn_status"], p + ".turn_status",
                       {"not_started", "running", "completed", "needs_attention", "interrupted", "unknown"})
                choice(attempt["outcome"], p + ".outcome", {"open", "succeeded", "failed", "blocked"})
                review(attempt["review"], p + ".review")
                dep_evidence = obj(attempt["dependency_evidence"], p + ".dependency_evidence", set())
                dispatched = task["state"] != "intent"
                if dispatched:
                    require(data["status"] != "draft", p + ": dispatched task in draft run")
                    dispatched_workers |= assignment["contract"]["role"] == "worker"
                    approval_id = text(attempt["approval_id"], p + ".approval_id")
                    approval = approvals.get(approval_id)
                    require(approval is not None, p + ": missing approval declaration")
                    if approval:
                        for key in ("plan", "origin", "lead", "limits"):
                            require(approval[key] == data[key], p + ": approval scope mismatch: " + key)
                        require(approval["contracts"].get(aid) == assignment["contract"],
                                p + ": approval contract mismatch")
                        require(all(approval["permissions"][key] for key in
                                    ("create_tasks", "messages_to_workers", "replies_to_origin")),
                                p + ": creation or bidirectional messaging not approved")
                    require(set(dep_evidence) == deps[aid], p + ": dependency evidence mismatch")
                    dependencies_to_check.append((aid, dep_evidence))
                else:
                    require(attempt["turn_status"] == "not_started" and attempt["result"] is None
                            and attempt["outcome"] == "open" and attempt["review"]["disposition"] == "open",
                            p + ": intent claims execution or review")

                unresolved = task["state"] in {"pending", "unknown"}
                unresolved |= task["state"] == "ready" and attempt["turn_status"] not in {"completed", "interrupted"}
                if unresolved:
                    live.add((task["host_id"], task["thread_id"] or task["client_thread_id"] or attempt_id))
                if i < len(attempts) - 1:
                    require(not unresolved, p + ": predecessor attempt still unresolved")
                    require(attempt["review"]["disposition"] != "accepted", p + ": accepted attempt has unplanned successor")

                result = attempt["result"]
                if result is not None:
                    obj(result, p + ".result", {"run_id", "plan_revision", "assignment_id", "attempt_id",
                                                "task", "artifacts", "checks", "unmet_criteria", "blockers",
                                                "resource_observations"})
                    for key, expected in (("run_id", data["run_id"]), ("plan_revision", plan["revision"]),
                                          ("assignment_id", aid), ("attempt_id", attempt_id)):
                        require(result[key] == expected, p + ": result identity mismatch: " + key)
                    identity(result["task"], p + ".result.task")
                    require(task["state"] == "ready" and result["task"] ==
                            {"thread_id": task["thread_id"], "host_id": task["host_id"]},
                            p + ": result task mismatch")
                    for key in ("artifacts", "unmet_criteria", "blockers"):
                        texts(result[key], p + ".result." + key)
                    checks = seq(result["checks"], p + ".result.checks")
                    for check in checks:
                        obj(check, p + ".result.check", {"name", "status", "evidence"})
                        text(check["name"], p + ".result.check.name")
                        choice(check["status"], p + ".result.check.status", {"passed", "failed", "unavailable"})
                        text(check["evidence"], p + ".result.check.evidence")
                    resources = obj(result["resource_observations"], p + ".result.resource_observations",
                                    {"cost", "tokens", "source"})
                    for key in ("cost", "tokens"):
                        amount = resources[key]
                        require(amount is None or (type(amount) in (int, float) and math.isfinite(amount) and amount >= 0),
                                p + ": invalid resource observation")
                    if resources["cost"] is not None or resources["tokens"] is not None:
                        text(resources["source"], p + ".result.resource_observations.source")

                accepted = attempt["review"]["disposition"] == "accepted"
                if attempt["outcome"] == "succeeded":
                    require(result is not None, p + ": success without result")
                if accepted:
                    require(task["state"] == "ready" and attempt["turn_status"] == "completed"
                            and attempt["outcome"] == "succeeded", p + ": accepted work is not completed success")
                    require(bool(attempt["review"]["evidence"]), p + ": acceptance missing evidence")
                    require(result is not None, p + ": acceptance missing result")
                    if result is not None:
                        require(bool(result["artifacts"]) and bool(result["checks"]), p + ": acceptance missing artifact/checks")
                        require(not result["unmet_criteria"] and not result["blockers"], p + ": acceptance has unmet work")
                        require(all(c["status"] == "passed" for c in result["checks"]), p + ": acceptance has failed/unavailable check")
                latest[aid] = attempt
            require(corrections <= limits["corrections"], aid + ": correction limit exceeded")
            require(replacements <= limits["replacements"], aid + ": replacement limit exceeded")
            remediations += corrections + replacements

        require(len(live) <= limits["active"], "run: active concurrency limit exceeded")
        require(remediations <= limits["remediations"], "run: remediation limit exceeded")
        for aid, evidence in dependencies_to_check:
            for predecessor, item in evidence.items():
                obj(item, aid + ".dependency_evidence", {"attempt_id", "artifacts"})
                text(item["attempt_id"], aid + ".dependency_evidence.attempt_id")
                texts(item["artifacts"], aid + ".dependency_evidence.artifacts", nonempty=True)
                previous = latest.get(predecessor)
                require(previous is not None and previous["review"]["disposition"] == "accepted",
                        aid + ": predecessor not accepted")
                if previous is not None:
                    require(item["attempt_id"] == previous["id"], aid + ": predecessor attempt mismatch")
                    result = previous["result"]
                    require(result is not None and set(item["artifacts"]) <= set(result["artifacts"]),
                            aid + ": predecessor artifacts mismatch")

        if data["route"] == "reviewed" and (dispatched_workers or data["status"] == "complete"):
            require(pr is not None, "run: required planning review missing")
            if pr is not None:
                require(pr["disposition"] == "accepted" and pr["plan_revision"] == plan["revision"]
                        and bool(pr["evidence"]), "run: required planning review not accepted for current plan")
                require(pr["reviewer"]["family"] != data["lead"]["family"], "run: reviewed route expects other lead family")
        if data["status"] == "complete":
            require(bool(assignments), "run: empty run cannot be complete")
            require(not live, "run: completion with unresolved native tasks")
            for aid, assignment in assignments.items():
                if assignment["contract"]["required"]:
                    require(aid in latest and latest[aid]["review"]["disposition"] == "accepted",
                            aid + ": required assignment not accepted")
            integration = data["integration_review"]
            require(integration["disposition"] == "accepted" and bool(integration["evidence"]),
                    "run: integrated result not accepted with evidence")
    except ShapeError as exc:
        errors.append(str(exc))
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number: " + value)


def load_record(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError(f"record exceeds {MAX_BYTES} bytes")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args(argv)
    try:
        errors = validate(load_record(args.record))
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("INVALID: " + error, file=sys.stderr)
        return 1
    print("STRUCTURE VALID: independently verify human authority, host state, and artifacts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
