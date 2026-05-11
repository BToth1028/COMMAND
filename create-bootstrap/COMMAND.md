---
name: create-bootstrap
description: >-
  DRAFT master-router BOOTSTRAP child. Validates handoff per dispatch_table.BOOTSTRAP;
  does not invoke bootstrap-start yet (runner exit 2 DRAFT_ONLY).
---

# Create-bootstrap (draft)

## Mission

Validate **`request_type: BOOTSTRAP`** and frozen **`project_name`**, **`project_root_absolute`**. Implementation will delegate to **`bootstrap-start`** when live subtree is missing per router notes.

## Current behaviour

Handoff validation only; **no** filesystem or bootstrap protocol execution.

## Inputs

`python create-bootstrap_run.py --handoff-json <absolute-path>`

## Output

- **Exit 2** + stdout JSON `DRAFT_ONLY` when keys present.
- **Exit 1** on HALT.

## Authority

- `C:\Users\rtoth\.cursor\commands\master-router\COMMAND.md`
- `create-bootstrap.yaml`

## Next steps

Wire **`bootstrap-start`** Path 3 / session-zero per **`upstream`** in dispatch table; respect **`WRONG_TOOL`** when bootstrap already exists.
