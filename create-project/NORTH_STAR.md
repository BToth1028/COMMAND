# NORTH_STAR — create-project (draft)

## Context

**PROJECT** is the heaviest **`master-router`** chain: session-zero bootstrap, milestone plan triplet, and anchor documents. This folder currently ships **spec + handoff validation only**.

## Principles

1. **Router freezes inputs** — this command must not re-classify **`request_type`**.
2. **Absolute `project_root_absolute`** — parity with **`G05`** / bootstrap law for JD workspaces.
3. **No partial project trees** without explicit chain semantics (follow **`dispatch_table`** order).

## Boundaries

- Does not replace **`bootstrap`** or **`project-plan-builder`** — orchestrates or delegates to them when BUILT.
- Does not write **`c:\dev`** JDex IDs without **`jd_propose`** / placement gate upstream.

## Draft exit

Runner **exit 2** = validated handoff, execution intentionally omitted until implemented.
