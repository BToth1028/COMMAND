---
name: create-code
description: >-
  DRAFT master-router CODE child. Validates dispatch_table.CODE handoff;
  materialisation pending (exit 2 DRAFT_ONLY).
---

# Create-code (draft)

## Mission

Validate **`request_type: CODE`** with **`language_label`**, absolute **`target_path_absolute`**, **`module_or_function_purpose`**. Future: write **`body`** (or stub) with overwrite gate like **`create-document`**.

## Inputs

`python create-code_run.py --handoff-json <absolute-path>`

## Output

**Exit 2** = validated draft. **Exit 1** = HALT.

## Authority

- `master-router/COMMAND.md` `dispatch_table.CODE`
- `create-code.yaml`
