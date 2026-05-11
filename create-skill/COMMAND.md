---
name: create-skill
description: >-
  DRAFT master-router SKILL child. Validates dispatch_table.SKILL handoff; chain not run.
---

# Create-skill (draft)

## Mission

Validate **`request_type: SKILL`** frozen inputs (six keys in **`create-skill.yaml`**). Full chain will emit **`SKILL.md`** and tier-3 **`NORTH_STAR.md`** per **`dispatch_table.SKILL`**.

## Inputs

`python create-skill_run.py --handoff-json <path>`

## Exit 2

Validated draft only — no files written.
