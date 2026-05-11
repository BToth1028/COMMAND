"""
validate_bootstrap.py — schema validator for context-bootstrap YAML files.

Authority location for the context-bootstrap protocol:
    C:/Users/rtoth/.cursor/commands/bootstrap/COMMAND.md
    (and sibling command YAMLs: bootstrap-{start,ingest,audit,init,checkpoint,finalize}.yaml)

Authority location for the task carry-forward matrix vocabulary:
    corpus/charter--1a017eabb2e8.yaml
    block: payload.session_continuity_vocabulary.task_carry_forward_matrix
    status: TEMPORARY_TENANT — pending extraction to a dedicated
    bootstrap-vocabulary--{shortUUID}.yaml corpus envelope. See the
    charter block's `todo` field for extraction conditions.

Usage:
    python validate_bootstrap.py path/to/Bootstrap_YYMMDD-HHMM.yaml
    python validate_bootstrap.py --finalized path/to/Bootstrap_YYMMDD-HHMM.yaml

Modes:
    default     — checks required structure of an in-flight or finalized bootstrap
    --finalized — additionally requires session.ended, session.session_summary,
                  and next_session_kickoff populated (finalize protocol)

Hard-fail behavior. Prints all errors and exits 1 on any violation.
Exits 0 only when every check passes.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Any

try:
	import yaml
except ImportError:
	sys.stderr.write("PyYAML required: pip install pyyaml\n")
	sys.exit(2)


REQUIRED_TOP_LEVEL = ["project", "session", "tasks", "decisions", "environment", "context_file_audit"]
OPTIONAL_TOP_LEVEL = ["issues", "supplemental", "supersedes", "next_session_kickoff"]
TASK_STATUSES = {"ACTIVE", "BLOCKED", "DEFERRED", "DONE", "CANCELLED"}
PRIORITIES = {"HIGH", "MEDIUM", "LOW"}
AUDIT_STATUSES = {"CURRENT", "STALE", "NEEDS_UPDATE", "DUPLICATE"}
SEVERITIES = {"HIGH", "MEDIUM", "LOW"}

SESSION_ID_RE = re.compile(r"^\d{6}-\d{4}$")
ISO8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})$")
TASK_ID_RE = re.compile(r"^T-\d{3,}$")
DECISION_ID_RE = re.compile(r"^D-\d{3,}$")
ISSUE_ID_RE = re.compile(r"^I-\d{3,}$")
FILENAME_RE = re.compile(r"^([A-Za-z0-9_]+)_(\d{6}-\d{4})(S)?\.yaml$")


class Errors:
	def __init__(self) -> None:
		self.items: list[str] = []

	def add(self, msg: str) -> None:
		self.items.append(msg)

	def __bool__(self) -> bool:
		return bool(self.items)


def _is_nonempty_str(v: Any) -> bool:
	return isinstance(v, str) and v.strip() != ""


def _check_top_level(doc: dict, errors: Errors) -> None:
	if not isinstance(doc, dict):
		errors.add("ROOT: bootstrap must be a YAML mapping")
		return
	for key in REQUIRED_TOP_LEVEL:
		if key not in doc:
			errors.add(f"ROOT: missing required top-level key '{key}'")
	allowed = set(REQUIRED_TOP_LEVEL) | set(OPTIONAL_TOP_LEVEL)
	for key in doc.keys():
		if key not in allowed:
			errors.add(f"ROOT: unknown top-level key '{key}'")


def _check_project(doc: dict, errors: Errors) -> None:
	p = doc.get("project")
	if not isinstance(p, dict):
		errors.add("project: must be a mapping")
		return
	for f in ("name", "summary", "scope", "non_scope"):
		if not _is_nonempty_str(p.get(f)):
			errors.add(f"project.{f}: missing or empty")


def _check_session(doc: dict, filename_session_id: str | None, errors: Errors, finalized: bool) -> str | None:
	s = doc.get("session")
	if not isinstance(s, dict):
		errors.add("session: must be a mapping")
		return None
	sid = s.get("id")
	if not _is_nonempty_str(sid) or not SESSION_ID_RE.match(sid):
		errors.add(f"session.id: missing or not in YYMMDD-HHMM format (got {sid!r})")
	elif filename_session_id and sid != filename_session_id:
		errors.add(f"session.id: '{sid}' does not match filename session id '{filename_session_id}'")
	started = s.get("started")
	if not _is_nonempty_str(started) or not ISO8601_RE.match(started):
		errors.add(f"session.started: missing or not ISO 8601 with offset (got {started!r})")
	ended = s.get("ended")
	if finalized:
		if not _is_nonempty_str(ended) or not ISO8601_RE.match(ended):
			errors.add(f"session.ended: required when --finalized but missing or invalid (got {ended!r})")
		if not _is_nonempty_str(s.get("session_summary")):
			errors.add("session.session_summary: required when --finalized but missing or empty")
	else:
		if ended not in (None, "") and not ISO8601_RE.match(ended):
			errors.add(f"session.ended: present but not ISO 8601 (got {ended!r})")
	return sid if isinstance(sid, str) else None


def _check_supplemental_pair(doc: dict, errors: Errors) -> None:
	supp = doc.get("supplemental")
	supersedes = doc.get("supersedes")
	if supp is True:
		if not _is_nonempty_str(supersedes) or not SESSION_ID_RE.match(supersedes):
			errors.add(f"supersedes: required when supplemental=true and must be YYMMDD-HHMM (got {supersedes!r})")
	elif supp is False or supp is None:
		if supersedes is not None and supersedes != "":
			errors.add("supersedes: present but supplemental is not true")
	elif supp is not None:
		errors.add(f"supplemental: must be boolean true or omitted (got {supp!r})")


def _check_tasks(doc: dict, errors: Errors) -> None:
	tasks = doc.get("tasks")
	if not isinstance(tasks, list):
		errors.add("tasks: must be a list")
		return
	seen_ids: set[str] = set()
	for i, t in enumerate(tasks):
		ctx = f"tasks[{i}]"
		if not isinstance(t, dict):
			errors.add(f"{ctx}: must be a mapping")
			continue
		tid = t.get("id")
		if not _is_nonempty_str(tid) or not TASK_ID_RE.match(tid):
			errors.add(f"{ctx}.id: missing or not T-NNN format (got {tid!r})")
		elif tid in seen_ids:
			errors.add(f"{ctx}.id: duplicate id '{tid}' within session")
		else:
			seen_ids.add(tid)
		if not _is_nonempty_str(t.get("title")):
			errors.add(f"{ctx}.title: missing or empty")
		status = t.get("status")
		if status not in TASK_STATUSES:
			errors.add(f"{ctx}.status: invalid (got {status!r}, expected one of {sorted(TASK_STATUSES)})")
		if not _is_nonempty_str(t.get("session_origin")):
			errors.add(f"{ctx}.session_origin: missing or empty")
		if not _is_nonempty_str(t.get("description")):
			errors.add(f"{ctx}.description: missing or empty")
		pr = t.get("priority")
		if pr not in (None, "") and pr not in PRIORITIES:
			errors.add(f"{ctx}.priority: invalid (got {pr!r}, expected one of {sorted(PRIORITIES)})")
		if status == "BLOCKED" and not _is_nonempty_str(t.get("blockers")):
			errors.add(f"{ctx}.blockers: required when status=BLOCKED")
		if status == "DEFERRED" and not _is_nonempty_str(t.get("deferred_reason")):
			errors.add(f"{ctx}.deferred_reason: required when status=DEFERRED")
		if status == "CANCELLED" and not _is_nonempty_str(t.get("cancelled_reason")):
			errors.add(f"{ctx}.cancelled_reason: required when status=CANCELLED")
		if status in ("DONE", "CANCELLED") and not _is_nonempty_str(t.get("session_completed")):
			errors.add(f"{ctx}.session_completed: required when status={status}")


def _check_decisions(doc: dict, current_session_id: str | None, errors: Errors) -> None:
	decisions = doc.get("decisions")
	if decisions is None:
		errors.add("decisions: missing (use empty list [] if no decisions this session)")
		return
	if not isinstance(decisions, list):
		errors.add("decisions: must be a list")
		return
	seen_ids: set[str] = set()
	for i, d in enumerate(decisions):
		ctx = f"decisions[{i}]"
		if not isinstance(d, dict):
			errors.add(f"{ctx}: must be a mapping")
			continue
		did = d.get("id")
		if not _is_nonempty_str(did) or not DECISION_ID_RE.match(did):
			errors.add(f"{ctx}.id: missing or not D-NNN format (got {did!r})")
		elif did in seen_ids:
			errors.add(f"{ctx}.id: duplicate id '{did}' within session")
		else:
			seen_ids.add(did)
		so = d.get("session_origin")
		if not _is_nonempty_str(so):
			errors.add(f"{ctx}.session_origin: missing or empty")
		elif current_session_id and so != current_session_id:
			errors.add(f"{ctx}.session_origin: '{so}' does not match current session.id '{current_session_id}' (decisions are session-scoped — only THIS session's decisions belong here)")
		for f in ("domain", "outcome", "rationale"):
			if not _is_nonempty_str(d.get(f)):
				errors.add(f"{ctx}.{f}: missing or empty")


def _check_environment(doc: dict, errors: Errors) -> None:
	e = doc.get("environment")
	if not isinstance(e, dict):
		errors.add("environment: must be a mapping")
		return
	if not isinstance(e.get("tools"), list):
		errors.add("environment.tools: must be a list (use [] if empty)")
	if not isinstance(e.get("key_paths"), (list, dict)):
		errors.add("environment.key_paths: must be a list or mapping (use [] if empty)")


def _check_context_file_audit(doc: dict, errors: Errors) -> None:
	cfa = doc.get("context_file_audit")
	if not isinstance(cfa, list):
		errors.add("context_file_audit: must be a list")
		return
	for i, e in enumerate(cfa):
		ctx = f"context_file_audit[{i}]"
		if not isinstance(e, dict):
			errors.add(f"{ctx}: must be a mapping")
			continue
		if not _is_nonempty_str(e.get("filename")):
			errors.add(f"{ctx}.filename: missing or empty")
		status = e.get("status")
		if status not in AUDIT_STATUSES:
			errors.add(f"{ctx}.status: invalid (got {status!r}, expected one of {sorted(AUDIT_STATUSES)})")
		if status != "CURRENT" and not _is_nonempty_str(e.get("note")):
			errors.add(f"{ctx}.note: required when status != CURRENT")


def _check_issues(doc: dict, errors: Errors) -> None:
	issues = doc.get("issues")
	if issues is None:
		return
	if not isinstance(issues, list):
		errors.add("issues: must be a list when present")
		return
	seen_ids: set[str] = set()
	for i, iss in enumerate(issues):
		ctx = f"issues[{i}]"
		if not isinstance(iss, dict):
			errors.add(f"{ctx}: must be a mapping")
			continue
		iid = iss.get("id")
		if not _is_nonempty_str(iid) or not ISSUE_ID_RE.match(iid):
			errors.add(f"{ctx}.id: missing or not I-NNN format (got {iid!r})")
		elif iid in seen_ids:
			errors.add(f"{ctx}.id: duplicate id '{iid}' within session")
		else:
			seen_ids.add(iid)
		if not _is_nonempty_str(iss.get("summary")):
			errors.add(f"{ctx}.summary: missing or empty")
		sev = iss.get("severity")
		if sev not in SEVERITIES:
			errors.add(f"{ctx}.severity: invalid (got {sev!r}, expected one of {sorted(SEVERITIES)})")
		if not _is_nonempty_str(iss.get("session_origin")):
			errors.add(f"{ctx}.session_origin: missing or empty")


def _check_next_session_kickoff(doc: dict, errors: Errors, finalized: bool) -> None:
	nsk = doc.get("next_session_kickoff")
	if finalized:
		if not isinstance(nsk, dict):
			errors.add("next_session_kickoff: required when --finalized but missing or not a mapping")
			return
	else:
		if nsk is None:
			return
		if not isinstance(nsk, dict):
			errors.add("next_session_kickoff: must be a mapping when present")
			return

	def req_str(label: str, v: Any) -> None:
		if not _is_nonempty_str(v):
			errors.add(f"next_session_kickoff.{label}: missing or empty")

	req_str("bootstrap_file_absolute", nsk.get("bootstrap_file_absolute"))
	req_str("project_root", nsk.get("project_root"))
	req_str("project_name", nsk.get("project_name"))
	req_str("path_1_operator_template", nsk.get("path_1_operator_template"))

	fi = nsk.get("frozen_intent")
	if not isinstance(fi, list) or len(fi) < 1:
		errors.add("next_session_kickoff.frozen_intent: must be a non-empty list of strings")
	else:
		for i, x in enumerate(fi):
			if not _is_nonempty_str(x):
				errors.add(f"next_session_kickoff.frozen_intent[{i}]: must be non-empty string")

	ta = nsk.get("truth_anchors")
	if not isinstance(ta, dict):
		errors.add("next_session_kickoff.truth_anchors: must be a mapping")
	else:
		req_str("truth_anchors.command_md", ta.get("command_md"))
		req_str("truth_anchors.schema_yaml", ta.get("schema_yaml"))
		vs = ta.get("validate_script")
		if vs is not None and not isinstance(vs, str):
			errors.add("next_session_kickoff.truth_anchors.validate_script: must be string or omitted")
		ex = ta.get("extra")
		if ex is None:
			ex = []
		if not isinstance(ex, list):
			errors.add("next_session_kickoff.truth_anchors.extra: must be a list")
		else:
			for i, p in enumerate(ex):
				if not _is_nonempty_str(p):
					errors.add(f"next_session_kickoff.truth_anchors.extra[{i}]: must be non-empty string")

	rf = nsk.get("read_first")
	if not isinstance(rf, list) or len(rf) < 2:
		errors.add("next_session_kickoff.read_first: must list at least 2 path strings (governance + this bootstrap minimum)")
	else:
		for i, p in enumerate(rf):
			if not _is_nonempty_str(p):
				errors.add(f"next_session_kickoff.read_first[{i}]: must be non-empty string")

	for label in ("assumptions_next_session_must_hold", "known_gaps", "do_not_request_from_operator_unless"):
		ls = nsk.get(label)
		if ls is None:
			if finalized:
				errors.add(f"next_session_kickoff.{label}: must be present (use [] if none)")
			continue
		if not isinstance(ls, list):
			errors.add(f"next_session_kickoff.{label}: must be a list")
			continue
		for i, x in enumerate(ls):
			if not _is_nonempty_str(x):
				errors.add(f"next_session_kickoff.{label}[{i}]: must be non-empty string")


def _filename_session_id(path: str) -> tuple[str | None, bool]:
	base = os.path.basename(path)
	m = FILENAME_RE.match(base)
	if not m:
		return None, False
	return m.group(2), bool(m.group(3))


def validate(path: str, finalized: bool) -> int:
	errors = Errors()
	if not os.path.isfile(path):
		print(f"ERROR: file not found: {path}", file=sys.stderr)
		return 2
	with open(path, "r", encoding="utf-8") as f:
		try:
			doc = yaml.safe_load(f)
		except yaml.YAMLError as e:
			print(f"ERROR: YAML parse failed for {path}\n  {e}", file=sys.stderr)
			return 1
	if doc is None:
		print(f"ERROR: empty YAML document: {path}", file=sys.stderr)
		return 1

	filename_sid, is_supplemental_filename = _filename_session_id(path)
	if filename_sid is None:
		errors.add(f"FILENAME: '{os.path.basename(path)}' does not match {{Project}}_YYMMDD-HHMM[S].yaml pattern")

	_check_top_level(doc, errors)
	if errors:
		_emit_and_exit(path, errors)
		return 1

	_check_project(doc, errors)
	current_sid = _check_session(doc, filename_sid, errors, finalized)
	_check_supplemental_pair(doc, errors)
	if is_supplemental_filename and doc.get("supplemental") is not True:
		errors.add("supplemental: filename ends with 'S' but supplemental is not true")
	_check_tasks(doc, errors)
	_check_decisions(doc, current_sid, errors)
	_check_environment(doc, errors)
	_check_context_file_audit(doc, errors)
	_check_issues(doc, errors)
	_check_next_session_kickoff(doc, errors, finalized)

	if errors:
		_emit_and_exit(path, errors)
		return 1

	mode = "finalized" if finalized else "draft"
	print(f"OK: {path} ({mode}, {len(doc.get('tasks', []))} tasks, {len(doc.get('decisions', []))} decisions)")
	return 0


def _emit_and_exit(path: str, errors: Errors) -> None:
	print(f"FAIL: {path}", file=sys.stderr)
	for e in errors.items:
		print(f"  - {e}", file=sys.stderr)
	print(f"  ({len(errors.items)} error(s))", file=sys.stderr)


def main(argv: list[str]) -> int:
	parser = argparse.ArgumentParser(description="Validate a context-bootstrap YAML file (authority: C:/Users/rtoth/.cursor/commands/bootstrap/COMMAND.md).")
	parser.add_argument("--finalized", action="store_true", help="Require session.ended, session.session_summary, and next_session_kickoff (finalized on-disk)")
	parser.add_argument("path", help="Path to bootstrap YAML")
	args = parser.parse_args(argv)
	return validate(args.path, args.finalized)


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
