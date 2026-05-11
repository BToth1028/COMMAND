---
name: create-subagent
description: >-
  DRAFT master-router SUBAGENT child. Validates dispatch_table.SUBAGENT handoff;
  materialisation pending (exit 2).
---

# Create-subagent (draft)

## Mission

Validate **`request_type: SUBAGENT`** and frozen **`subagent_name`**, **`subagent_description`**, **`system_prompt_body`**, **`scope`** (`project` \| `user`). Implementation will write **`{project_root}/.cursor/agents/`** or user scope path per router templates.

## Inputs

`python create-subagent_run.py --handoff-json <absolute-path>`

## Output

**Exit 2** + `DRAFT_ONLY` JSON when keys present.

## Authority

`master-router/COMMAND.md` `dispatch_table.SUBAGENT`
