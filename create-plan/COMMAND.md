---
name: create-plan
description: >-
  DRAFT master-router PLAN child. Validates operation + payload; project-plan-builder not run.
---

# Create-plan (draft)

## Mission

Validate **`request_type: PLAN`**, **`project_id`**, **`operation`** ∈ {`create_milestone_plan`, `create_execution_plan`}, **`operation_payload`**.

## Inputs

`python create-plan_run.py --handoff-json <path>`

## Authority

`master-router/COMMAND.md` `dispatch_table.PLAN` → **`planning/project-plan-builder.yaml`**.
