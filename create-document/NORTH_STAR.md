# NORTH_STAR — create-document (master-router child)

## Context

This command is the **`DOCUMENT`** execution leg for **`master-router`**. The JDex workspace mission treats **`C:\dev`** evolution as highest-tier governance work; deterministic creation plumbing must not drift into silent defaults.

## Principles

1. **Frozen inputs only** — classify upstream in **`master-router`**; this command executes.
2. **No silent overwrite** — filesystem safety overrides convenience.
3. **UTF-8 truth** — write bytes exactly as resolved from handoff/stdin.

## Boundaries

- Does not reinterpret **`tier_locked`** or **`intent_anchor`** — consumed verbatim for logging only if extended later.
- Does not patch **`jdex.yaml`** or relocate JD artifacts — route elsewhere.

## Key concepts

| Term | Meaning |
|------|---------|
| Handoff JSON | Frozen **`handoff_envelope`** subset serialized to disk |
| Subtype | Router **`document_subtype_enum`** member |

## Failure modes

- Missing **`project_root`** directories → **`mkdir`** mitigates for target branch only.
- Operator supplies relative target path → HALT (router must enforce absolute upstream).

## Upstream inheritance

- **`master-router`** output contract SUCCESS_ATOMIC / CHILD_NOT_BUILT transition.
- **`bootstrap`** session-zero remains separate; bootstrap live-root law documented under **`46.06-jdex-session-live-root`**.

## Decision log pointer

- **`c:\dev\00-09-system-administration\00-index\00.02-changelog\CHANGELOG.md`**
- **`c:\dev\40-49-ai-agents-and-prompts\47-outputs-and-artifacts\47.04-ontology-decision-traces\`**
