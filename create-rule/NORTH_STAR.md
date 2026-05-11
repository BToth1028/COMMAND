# NORTH_STAR — create-rule (draft)

## Context

**RULE** produces **`.mdc`** (or equivalent) under **`.cursor/rules`**. Distinct from **SKILL** and **COMMAND** request types.

## Principles

1. **`scope_kind`** / **`scope_value`** must map to Cursor rule application mode (`alwaysApply` vs globs).
2. **No silent merge** with existing rules — future implementation needs collision policy.
3. **Upstream skill** remains normative for content shape until this runner encodes it.

## Draft

Handoff validation only; no filesystem writes.
