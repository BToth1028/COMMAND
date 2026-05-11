# NORTH_STAR — create-bootstrap (draft)

## Context

**BOOTSTRAP** applies session-zero layout when **`project_root`** exists but the live bootstrap subtree does not. Router text warns: if bootstrap already exists, this is session lifecycle, not creation.

## Principles

1. **Never duplicate bootstrap** — detect existing subtree before writes.
2. **Absolute paths only** — match **`hard_input_requirements`** in master-router.
3. **Delegate to canonical YAML** — **`bootstrap-start.yaml`** owns protocol detail.

## Draft boundary

Runner validates frozen inputs only until **`bootstrap-start`** invocation is implemented.
