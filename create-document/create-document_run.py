"""
Execute master-router DOCUMENT dispatch: write file bytes from handoff envelope.

Usage:
  python create-document_run.py --handoff-json path\\to.json [--overwrite]

handoff JSON must include target_path_absolute, request_type == DOCUMENT,
subtype_or_operation_or_language_label (yaml|md|txt|...).

Body resolution order:
  1) optional_inputs_frozen.body_or_content_brief (string)
  2) required_inputs_frozen.body (string)
  3) stdin if --stdin-body and body keys absent
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_handoff(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("handoff must be a JSON object")
    return data


def resolve_body(h: dict, stdin_body: bool) -> str:
    opt = h.get("optional_inputs_frozen") or {}
    req = h.get("required_inputs_frozen") or {}
    if isinstance(opt, dict) and isinstance(opt.get("body_or_content_brief"), str):
        return opt["body_or_content_brief"]
    if isinstance(req, dict) and isinstance(req.get("body"), str):
        return req["body"]
    if stdin_body:
        return sys.stdin.read()
    raise ValueError(
        "No body found (optional_inputs_frozen.body_or_content_brief, "
        "required_inputs_frozen.body, or stdin with --stdin-body)"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff-json", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--stdin-body", action="store_true")
    args = parser.parse_args()

    handoff = load_handoff(args.handoff_json)
    if handoff.get("request_type") != "DOCUMENT":
        print("HALT: request_type must be DOCUMENT", file=sys.stderr)
        return 1

    target = handoff.get("target_path_absolute")
    if not isinstance(target, str) or not target.strip():
        print("HALT: target_path_absolute missing", file=sys.stderr)
        return 1
    dest = Path(target)

    subtype = handoff.get("subtype_or_operation_or_language_label")
    if not isinstance(subtype, str) or not subtype.strip():
        print("HALT: subtype missing", file=sys.stderr)
        return 1

    if dest.exists() and not args.overwrite:
        print(f"HALT: target exists (use --overwrite): {dest}", file=sys.stderr)
        return 1

    body = resolve_body(handoff, args.stdin_body)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"status": "written", "path": str(dest.resolve()), "subtype": subtype}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 -- CLI surface
        print(f"HALT: {exc}", file=sys.stderr)
        raise SystemExit(1)
