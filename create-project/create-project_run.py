"""DRAFT runner — validate PROJECT handoff shape; no chain execution yet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUEST_TYPE = "PROJECT"
REQUIRED_FROZEN = (
    "project_name",
    "project_root_absolute",
    "project_mission",
    "first_milestone_minimum_fields",
    "intent_anchor_per_tier_locked",
)
DRAFT_EXIT = 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff-json", type=Path, required=True)
    args = parser.parse_args()
    handoff = json.loads(args.handoff_json.read_text(encoding="utf-8"))
    if not isinstance(handoff, dict):
        print("HALT: handoff must be object", file=sys.stderr)
        return 1
    if handoff.get("request_type") != REQUEST_TYPE:
        print(f"HALT: request_type must be {REQUEST_TYPE}", file=sys.stderr)
        return 1
    frozen = handoff.get("required_inputs_frozen") or {}
    if not isinstance(frozen, dict):
        print("HALT: required_inputs_frozen must be object", file=sys.stderr)
        return 1
    missing = [k for k in REQUIRED_FROZEN if k not in frozen]
    if missing:
        print(f"HALT: missing required_inputs_frozen keys: {missing}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "DRAFT_ONLY",
                "request_type": REQUEST_TYPE,
                "message": "Draft child: chain execution not implemented",
                "validated_keys": list(REQUIRED_FROZEN),
            }
        )
    )
    return DRAFT_EXIT


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"HALT: {exc}", file=sys.stderr)
        raise SystemExit(1)
