---
name: create-project
description: >-
  DRAFT master-router PROJECT execution child. Validates frozen handoff for
  dispatch_table.PROJECT; materialisation (bootstrap + plan triplet + NORTH_STAR
  chain) is not implemented — runner exits DRAFT_ONLY (code 2).
---

# Create-project (draft)

## Mission

**DRAFT** package for **`request_type: PROJECT`**. Aligns with **`master-router`** `dispatch_table.PROJECT` (chain: bootstrap-start → plan builder → optional NORTH_STAR → optional rule).

## Current behaviour

| Step | Status |
|------|--------|
| Load `--handoff-json` | Yes |
| `request_type == PROJECT` | Yes |
| Required frozen keys present | Yes |
| Execute bootstrap / plans / writes | **No** (draft) |

## Authority

- `C:\Users\rtoth\.cursor\commands\master-router\COMMAND.md`
- `create-project.yaml` (this folder)

## Inputs

`python create-project_run.py --handoff-json <absolute-path>`

## Output

- Success validation: one JSON line stdout with `"status":"DRAFT_ONLY"`, **exit code 2** (not zero — not BUILT).
- HALT: stderr, exit 1.

## Next implementation steps

1. Invoke or embed **`bootstrap-start`** Path 3 per upstream YAML.
2. Invoke **`project-plan-builder`** `create_milestone_plan`.
3. Optional **`NORTH_STAR.md`** at `{project_root}/NORTH_STAR.md` when tier requires.
4. Optional **`create-rule`** when `initial_rule_content` present.
