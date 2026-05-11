---
name: create-rule
description: >-
  DRAFT master-router RULE child. Validates dispatch_table.RULE handoff;
  materialisation pending.
---

# Create-rule (draft)

## Mission

Prepare **`RULE`** execution: validate **`rule_name`**, **`rule_description`**, **`scope_kind`**, **`scope_value`**, **`rule_body`**. Target template `{project_root}/.cursor/rules/{rule_name}.mdc`.

## Inputs

`python create-rule_run.py --handoff-json <path>`

## Output

**Exit 2** `DRAFT_ONLY` on success validation.

## Upstream

Router cites **`create-rule`** skill under **`skills-cursor`** — implementation may shell to agent skill or port template logic.
