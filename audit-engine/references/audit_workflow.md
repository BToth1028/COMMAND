---
name: workflow-audit
description: >-
  Single-domain workflow auditor. Runs the 8-layer workflow audit framework
  (Determinism, Reference Integrity, Outcome Achievability, Completeness,
  Internal Consistency, Scope Coherence, Agent Executability, Structural
  Quality) over any agent workflow document — YAML prompts, SKILL.md files,
  markdown runbooks, COMMAND.md files. Imports the engine for mode taxonomy,
  Mode 5 iterative loop, halt protocols, output contract, and anti-drift
  safeguards. Invoke as `@workflow-audit [<mode>]`. Audits only — never
  modifies. The deliverable is an audit report plus a proposal-only
  remediation plan; execution is handed off to a separate session.
---

# Workflow-Audit

## What this command is

`@workflow-audit` is the **workflow-domain auditor**. It owns:

- The 8 workflow audit layers (L1-DET through L8-STR).
- The 50+ workflow-specific check IDs and their fail conditions.
- The workflow-format enum (YAML_PROMPT, SKILL_MD, COMMAND_MD,
  MARKDOWN_RUNBOOK, MIXED, FREEFORM).
- Workflow-specific tier overrides.
- Workflow-specific edge cases (oversized doc, non-English, syntax
  errors, self-referential workflow… see §"Workflow-Specific Edge
  Cases" for the full closed list).

`@workflow-audit` does NOT own:

- The audit-mode taxonomy → owned by `@audit-engine`.
- The Mode 5 iterative loop (steps M5-1 through M5-10) → owned by
  `@audit-engine`.
- Halt protocols → owned by `@audit-engine`.
- The `audit_report` / `finding` / `iteration` / `remediation_plan`
  schemas → owned by `@audit-engine`.
- Anti-drift safeguards → owned by `@audit-engine`.
- Content-type detection or mixed-content dispatch → owned by
  `@audit-engine`.

This module **is embedded within `@audit-engine`**. The engine's COMMAND.md
(`C:\Users\rtoth\.cursor\commands\audit-engine\COMMAND.md`) is the source of
truth for loop semantics, schemas, and halt protocols and MUST be read before
producing any audit report. This module is loaded at PF-2 pre-flight.

## Existing skill is unaffected

This command does NOT alter the existing `workflow-auditor` skill. That
skill still auto-fires on natural-language audit prompts. Use
`@workflow-audit` when you want the engine-based framework explicitly.

## Invocation

```
@workflow-audit [<mode>]
```

- `<mode>` (optional) ∈ `{full, targeted, post_mortem, diff, iterative}`.
  **Iterative is the unconditional default** (inherited from `@audit-engine`).
  `iterative` wraps `full`, `post_mortem`, or `diff` via the engine's
  Mode 5 loop.

Examples:

- `@workflow-audit` — iterative (Mode 5) audit; default mode.
- `@workflow-audit iterative` — explicit iterative override (same as default).
- `@workflow-audit post_mortem` — Mode 5 post-mortem on a workflow that
  failed in production.
- `@workflow-audit diff` — Mode 5 diff between two workflow versions.

This module is loaded by `@audit-engine` as a sub-step of workflow and
mixed-content runs. Its canonical path is
`C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_workflow.yaml` (supersedes this file).

---

## Mission

Systematically evaluate any agent workflow document for structural
soundness, internal consistency, and real-world executability — surfacing
every failure mode BEFORE the user discovers it in production.

**This command audits workflows. It does not build or modify them.**

Findings that require workflow reconstruction route to
`deterministic-prompt-builder` (for YAML prompts) or to user action (for
other formats). Outputs are audit reports and finding queues — not
revised workflows.

---

## Authority Model

**Canonical:** the workflow document being audited; the user's stated
intent for it.

**Derived:** audit report, layer scores, tier rating, finding
classifications, routing queues, remediation plan items.

**Rule:** never modify the workflow under audit. Never assume intent the
user has not stated. If the workflow's purpose is ambiguous, halt and
ask before auditing — an audit without a known target is meaningless.

---

## Scope / Non-Scope

**In scope:** running the 8-layer workflow audit framework. Scoring each
layer. Producing an overall tier rating with workflow-specific overrides.
Classifying findings by severity. Routing findings to remediation paths.
Comparing two workflow versions. Post-mortem analysis.

**Never:** rewrite the workflow. Fix findings directly. Author new
prompts or skills. Make domain-truth judgments about the workflow's
subject matter. Skip layers. Soften findings. Operate without a workflow
document loaded.

---

## STEP 0 — Pre-Audit Setup

> **Pre-flight is engine-owned.** Before STEP 0 runs, the engine's
> §"Pre-flight verification" (PF-1…PF-6) MUST already have passed. STEP
> 0 does NOT duplicate pre-flight; it begins after the engine confirms
> all canonical files, required skills, and the artifact under audit
> are loaded. Any pre-flight failure halts with
> `halt_reason: PRE_FLIGHT_FAILURE` (see `@audit-engine`).

Before any audit work begins:

```
1. Confirm the workflow document is loaded and readable.
   - If not provided → HALT. Request workflow.
   - If provided as a file path → read the file.
   - If provided inline → capture it.

2. Generate audit_id using format WFA-YYYYMMDD-HHMMSS from current timestamp.

3. Identify the workflow format:
   - YAML_PROMPT: Structured YAML following deterministic-prompt-builder spec
   - SKILL_MD: Skill file with YAML frontmatter + markdown body
   - COMMAND_MD: Cursor command file with YAML frontmatter + markdown body
   - MARKDOWN_RUNBOOK: Markdown instructions without YAML structure
   - MIXED: Combination of formats
   - FREEFORM: Unstructured prose instructions
   → Record as `workflow_format` in the audit report.

4. Confirm the workflow's stated intent:
   - Extract the mission/objective/purpose statement if present.
   - If no mission statement exists → ask the user: "What is this
     workflow supposed to accomplish?" Do not proceed without this.
   → Record as `stated_intent`.

5. Confirm session mode (full / targeted / post_mortem / diff / iterative).

6. If post_mortem → collect failure description from user.
   If diff → confirm both versions are loaded.

7. Viability gate: IF the document contains no instructions, no steps,
   and no recognizable structure (no headings, no numbered items, no
   conditional logic) → HALT with finding NOT_A_WORKFLOW. Do not proceed
   to Layer 1.
```

---

## Audit Framework — 8 Layers

Layers execute in order 1 → 8. Each layer produces a score (0–100) and a
list of findings. A layer with zero findings scores 100. Per-check error
protocol (PASS / FAIL / PARTIAL / SKIPPED) is owned by `@audit-engine`.

> **Vocabulary is engine-owned.** Every term used as a severity-bias
> trigger or scope qualifier — `primary execution path`, `downstream
> system`, `primary use-case`, `expected load`, `long-form rewriting`,
> `single-threaded synchronous`, `implicit knowledge`, `task complexity`,
> `non-blank line`, `junk drawer`, `stricter cap`, `build artifact` —
> resolves to its closed definition in `@audit-engine` §"Deterministic
> vocabulary". This command does NOT redefine these terms locally.

### Layer 1 — Determinism (L1-DET)

*Given identical inputs, will this workflow produce identical outputs every time?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 1.1 | **Ambiguous verb scan** | Presence of any token in the closed list: `consider`, `try`, `attempt`, `explore`, `think about`, `look into`, `might`, `perhaps`, `maybe`, `could`, `should consider`, `various`, `some`, `several`, `a few`, `many`, `often`, `evaluate` (when used as directive), `assess` (when used as directive), `review` (when not citing a closed procedure), `examine` (when not citing specific evidence), `determine` (when no determination criteria given), `ensure` (when no verification mechanism given), `generally`, `typically`, `usually`, `mostly`, `commonly`, `normally`, `in most cases`, `in general`. |
| 1.2 | **Open enumeration scan** | Presence of any token in the closed list: `etc.`, `such as`, `for example`, `including but not limited to`, `and more`, `among others`, `and similar`, `like` (as a list opener), `things like`, `or so`, `thereabouts`, `approximately` (as a quantity hedge), `roughly`, `about` (as a quantity hedge), `and similar items`, `items like`, `things include`, OR a trailing `…` (Unicode ellipsis U+2026 or `...`) at the end of a list item that has no closing closed-set citation. |
| 1.3 | **Ordering stability** | Any list or output sequence without an explicit sort key and direction |
| 1.4 | **Conditional completeness** | Any IF without an ELSE or explicit default. Any branching logic without exhaustive case coverage |
| 1.5 | **Implicit discretion** | Instructions that rely on agent judgment without defined criteria: "use your best judgment", "as appropriate", "when relevant", "if necessary" |
| 1.6 | **Reproducibility test** | Could two different agents reading this workflow independently arrive at different outputs for the same input? If yes → FAIL |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

### Layer 2 — Reference Integrity (L2-REF)

*Do all references in this workflow point to things that actually exist?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 2.1 | **File path validation** | Any referenced file path that cannot be verified as existent or is not qualified (relative paths without a base) |
| 2.2 | **Cross-reference validation** | References to other skills, prompts, or documents that are not identified by a concrete locator (name, path, ID) |
| 2.3 | **Tool/capability references** | References to tools, APIs, or capabilities that the executing agent may not have access to |
| 2.4 | **Schema references** | References to data schemas, field names, or structures that are not defined within the workflow or a cited source |
| 2.5 | **Stale marker scan** | References that include version numbers, dates, or identifiers that may have changed since authoring |
| 2.6 | **Circular reference check** | Any reference chain that loops back to itself (A → B → C → A) |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

**Note on verification limits:** the auditor cannot always confirm that
an external file or tool exists — it flags references it *cannot verify*
rather than asserting they are broken. Findings in this layer use
severity UNVERIFIABLE when existence cannot be confirmed and BROKEN when
absence can be confirmed.

### Layer 3 — Outcome Achievability (L3-OUT)

*Can the stated mission actually be accomplished by following the defined steps?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 3.1 | **Mission-to-steps coverage** | The stated intent requires actions that no step in the workflow addresses |
| 3.2 | **Step output chain** | A step requires input that no prior step produces (broken data flow) |
| 3.3 | **Terminal state reachability** | The workflow has no defined end state, or the end state cannot be reached via the defined steps |
| 3.4 | **Precondition satisfaction** | A step has preconditions that are never guaranteed by prior steps |
| 3.5 | **Output contract fulfillment** | The final output (if defined) requires fields or data that the workflow never generates |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 5) × 100.

### Layer 4 — Completeness (L4-CMP)

*Are all paths, errors, and edge cases handled?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 4.1 | **Error handling coverage** | Any step that can fail but has no on_failure, fallback, or error path defined |
| 4.2 | **Edge case coverage** | Workflow does not address one or more of the following mandatory edge case categories: (1) empty/null input, (2) malformed/corrupt input, (3) boundary values (min/max/zero), (4) wrong-type input, (5) maximum-size input, (6) minimal-size input, (7) input with missing required fields, (8) input that exactly matches a boundary condition. Check each category; FAIL if ≥1 unaddressed. |
| 4.3 | **Branch exhaustiveness** | Decision points that do not cover all reachable cases |
| 4.4 | **Scope boundary handling** | No defined behavior for inputs or requests that fall outside the workflow's stated scope |
| 4.5 | **Graceful degradation** | No defined behavior for partial failures — one of several data sources unavailable, a referenced file missing, a tool returning an error instead of data |
| 4.6 | **Exit conditions** | No defined mechanism for the agent to halt, escalate, or abort when stuck |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

### Layer 5 — Internal Consistency (L5-CON)

*Does the workflow contradict itself?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 5.1 | **Gate-state alignment** | A validation gate checks for a format or condition that a prior step has already transformed — validating lowercase after a step that uppercases, checking for nulls after a step that provides defaults |
| 5.2 | **Example compliance** | Provided examples (positive, negative, edge) that would fail the workflow's own validation rules |
| 5.3 | **Scope-algorithm alignment** | The algorithm contains steps that fall outside declared scope, or the scope declares capabilities the algorithm never exercises |
| 5.4 | **Definition consistency** | A term is defined differently in two places within the workflow |
| 5.5 | **Authority conflict** | Multiple canonical sources declared, or derived data treated as canonical |
| 5.6 | **Constraint contradiction** | Two rules that cannot both be satisfied simultaneously |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

### Layer 6 — Scope Coherence (L6-SCP)

*Does the workflow stay in its lane?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 6.1 | **Scope declaration exists** | No explicit in-scope / out-of-scope / never lists |
| 6.2 | **Scope specificity** | Scope declarations so broad they impose no real constraint ("handles all user requests") |
| 6.3 | **Drift surface area** | Number of points where the agent could plausibly be prompted to leave scope, with no guardrails defined |
| 6.4 | **Anti-drift mechanisms** | No explicit drift prevention (identity anchors, refusal templates, scope-check steps) |
| 6.5 | **Companion routing** | Workflow does not define where out-of-scope requests should be routed |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 5) × 100.

### Layer 7 — Agent Executability (L7-EXE)

*Can the intended executor actually do what this workflow demands?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 7.1 | **Context window feasibility** | Estimate total token count: workflow + all referenced files + expected average input. PASS if <80K tokens. PARTIAL if 80K–150K tokens. FAIL if >150K tokens. If token count cannot be estimated, record as PARTIAL with note. |
| 7.2 | **Tool availability assumptions** | The workflow assumes tools (web search, file I/O, code execution, MCP servers) without verifying availability |
| 7.3 | **Permission assumptions** | The workflow assumes permissions (file write, API access, network access) that may not be granted |
| 7.4 | **Multi-turn state assumptions** | The workflow assumes the agent retains state across turns or sessions without defining a persistence mechanism |
| 7.5 | **Cognitive load assessment** | Count concurrent state slots the agent must track per the **closed state-slot list** in `@audit-engine` §"Mode 5 state externalization > Effect on cognitive load (closed state-slot list)". Only slots S1–S9 in that list count; nothing else qualifies as state. PASS if ≤ 5 slots active. PARTIAL if 6–9 slots active (subagent two-stage scope). FAIL if any non-listed item is treated as a state slot OR > 9 slots are active. |
| 7.6 | **Instruction clarity for zero-context agent** | Could an agent with NO prior context on this project execute this workflow? If it requires implicit knowledge, it fails |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

### Layer 8 — Structural Quality (L8-STR)

*Is the workflow well-organized, navigable, and maintainable?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 8.1 | **Progressive disclosure** | All information frontloaded with no hierarchy; no clear "read this first, reference that later" structure |
| 8.2 | **Section organization** | Related instructions scattered across non-adjacent sections |
| 8.3 | **Redundancy** | Same instruction stated in multiple places (maintenance risk — they will diverge) |
| 8.4 | **Length proportionality** | Workflow length is disproportionate to task complexity (either bloated or underspecified) |
| 8.5 | **Naming clarity** | Section names, step names, or variable names that don't clearly communicate purpose |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 5) × 100.

---

## Layer Weights & Tier Overrides

### Workflow layer weights (used in overall score)

```yaml
workflow_layer_weights:
  L1-DET (Determinism):           0.20    # Highest — foundational
  L2-REF (Reference Integrity):   0.15
  L3-OUT (Outcome Achievability): 0.15
  L4-CMP (Completeness):          0.15
  L5-CON (Internal Consistency):  0.15
  L6-SCP (Scope Coherence):       0.08
  L7-EXE (Agent Executability):   0.07
  L8-STR (Structural Quality):    0.05
                                  -----
                                   1.00
```

### Workflow-specific tier overrides

These stack on top of the universal overrides defined in `@audit-engine`.

```yaml
workflow_overrides:
  - condition: "Layer 1 (Determinism) has ≥ 2 FAILed checks (i.e. ≥ 2 of the 6 L1 checks scored 0 individually)"
    cap: "D"
    reason: "Non-deterministic workflows are fundamentally unreliable. A single FAILed L1 check is a serious finding but may be local; two or more constitute systemic non-determinism."
    # NOTE: the threshold is at the *check* level (count of L1 checks with
    # result=FAIL), not at the layer aggregate level. PARTIAL counts as 0.5
    # and does NOT count toward the FAIL count. SKIPPED is excluded entirely.

  - condition: "Layer 3 (Outcome Achievability) score < 40"
    cap: "D"
    reason: "Workflow cannot achieve its stated purpose"
```

When combined with engine universal overrides, conflicts are resolved by
taking the **stricter** cap.

---

## Workflow `category` enum

Workflow findings use the universal `category` enum (defined in
`@audit-engine`'s `finding` schema):

`AMBIGUITY | BROKEN_REF | STALE_REF | UNREACHABLE | UNHANDLED |
CONTRADICTION | SCOPE_LEAK | ASSUMPTION | REDUNDANCY | STRUCTURAL |
UNVERIFIABLE`

No workflow-specific extensions.

---

## Workflow-Specific Edge Cases

```yaml
edge_cases:
  empty_document:
    condition: "Workflow has frontmatter but no body, or body has no instructions"
    action: "HALT at Step 0 viability gate. Emit finding NOT_A_WORKFLOW."

  oversized_document:
    condition: "Workflow exceeds 3,000 lines or estimated 100K tokens"
    action: >
      Proceed with audit but add ADVISORY finding in L8-STR noting size.
      If token count risks context window overflow during audit, split
      into two passes: Layers 1–4 first, then Layers 5–8 with findings
      summary from the first pass carried forward.

  non_english_workflow:
    condition: "Workflow is written in a language other than English"
    action: >
      Proceed with audit. Checks 1.1 (ambiguous verb scan) and 1.2 (open
      enumeration scan) use English-language markers only — SKIP these
      checks and note language limitation. All structural checks (Layers
      2–8) apply regardless of language.

  self_referential_workflow:
    condition: "Workflow references itself (an auditor skill auditing itself)"
    action: >
      Proceed normally. The audit evaluates structural quality, not
      domain recursion. Note in decision_trace.auditor_notes that the
      workflow is self-referential.

  minimal_prose_only:
    condition: "Workflow is a single paragraph or short block of prose"
    action: >
      Record format as FREEFORM. Many checks will produce PARTIAL or
      FAIL due to lack of structure. This is expected — the score
      reflects the workflow's actual quality, not a format penalty.

  syntax_errors:
    condition: "YAML frontmatter has syntax errors, or markdown is malformed"
    action: >
      Record a CRITICAL finding in L2-REF. If the workflow is still
      readable despite syntax errors, proceed with audit on the readable
      portions. If unreadable, invoke layer-failure protocol (engine).

  workflow_with_no_stated_purpose:
    condition: "No mission/objective found AND user declines to provide one"
    action: >
      HALT. An audit without a target cannot evaluate outcome
      achievability (Layer 3). Record in decision_trace and exit cleanly.

  workflow_includes_significant_code:
    condition: "Workflow contains fenced code blocks ≥ 20 non-blank lines or with declared runnable language"
    action: >
      The input is mixed-content. RECOMMEND user invoke @audit-engine
      mixed instead of @workflow-audit alone. If user insists on
      workflow-only audit, proceed but note in decision_trace that the
      embedded code was treated as opaque text and was NOT audited
      against the L1-COR through L8-STR layers owned by @code-audit.
```

---

## Workflow-Specific Error Policy

| Condition | Action |
| --- | --- |
| No workflow document provided | HALT. Request workflow. Do not audit nothing. |
| Workflow purpose ambiguous | HALT. Ask user to state intent. Do not audit without a target. |
| Cannot verify an external reference | Record as UNVERIFIABLE finding (not BROKEN). Note verification limits. |
| Workflow format unrecognizable | Record format as FREEFORM. Proceed with audit. Note that format-specific checks (YAML structure, frontmatter) will be SKIPPED. |
| Layer produces ambiguous result | Record as PARTIAL. Include both interpretations in the finding. Never round up. |
| User asks to skip a layer in Mode 1 (FULL) | Refuse. Offer Mode 2 (TARGETED) instead. A FULL audit with skipped layers is a lie. |
| Out-of-scope request ("fix this for me", "rewrite this section", "improve the wording") | Emit structured refusal. Route to appropriate skill or user action. |

---

## Output Contract additions

The base `audit_report` and `finding` schemas are owned by `@audit-engine`.
This command populates the `domain` field as `WORKFLOW`, the
`artifact_format` field with one of the workflow_format enum values, and
the `audit_id` with prefix `WFA-`.

The `layers[]` array contains exactly 8 entries (L1-DET through L8-STR)
in Mode 1 (FULL) and Mode 5 (ITERATIVE), or a subset in Mode 2
(TARGETED).

In Mode 5, the engine's iteration block and remediation_plan block apply
verbatim. The Mode 5 procedure (steps M5-1 through M5-10) is owned by
the engine; this command supplies the layer set and check definitions
that each granular pass executes.

---

## Companion Commands

- **`@audit-engine`** (`C:\Users\rtoth\.cursor\commands\audit-engine\COMMAND.md`)
  — Orchestrator. Owns the loop semantics. Required reading before any audit.
- **`references/audit_code.md`**
  (`C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_code.md`)
  — Sibling code-domain module. Loaded by `@audit-engine` for the code
  partition of mixed-content runs.
- **`deterministic-prompt-builder`** (skill) — Construction skill for
  YAML prompts. Plan items with `routing == PROMPT_BUILDER` are listed
  under `remediation_plan.prompt_builder_substeps` with rationale. The
  executor session invokes this skill, NOT the auditor.
- **`ontology-axiom-compliance`** *(planned skill — not yet registered;
  recommendation only)* — IF the workflow under audit governs an
  ontology system (schema definitions, entity relationships, constraint
  enforcement) → recommend axiom-level compliance audit in a separate
  session **once the skill is registered**. Until then, surface the
  recommendation as an `ADVISORY` finding in `decision_trace.auditor_notes`
  rather than routing to a non-existent skill. ELSE → skip.
- **`context-bootstrap`** (skill) — Session continuity. Mode 5 always
  crosses sessions, so a bootstrap entry is required at handoff.

---

## Procedure Summary

```
INVOCATION: @workflow-audit [<mode>]
            (or loaded by @audit-engine on workflow partition;
             canonical: audit-engine/references/audit_workflow.md)

STEP 0:  Pre-Audit Setup
         → Load workflow → Generate audit_id (WFA-...) → Identify format
         → Confirm intent → Select mode → Run viability gate

STEP 1:  Execute Audit Layers 1–4 (foundational checks)
         For each layer (L1-DET, L2-REF, L3-OUT, L4-CMP):
           → Run all checks (engine per-check error protocol applies)
           → Record findings
           → Calculate layer score
           → If layer cannot complete → invoke engine layer-failure protocol

CHECKPOINT: Summarize Layers 1–4 findings before continuing.

STEP 2:  Execute Audit Layers 5–8 (structural checks)
         For each layer (L5-CON, L6-SCP, L7-EXE, L8-STR):
           → Run all checks
           → Record findings
           → Calculate layer score

STEP 3:  Calculate overall score and tier
         → Weighted average with workflow_layer_weights
         → Apply universal overrides (engine) + workflow_overrides
         → Stricter cap wins on conflict

STEP 4:  Classify and route findings
         → Severity per engine severity_definitions
         → Sort: severity DESC, layer order ASC
         → Routing (PROMPT_BUILDER | USER_ACTION | INFORMATIONAL)

STEP 5:  Assemble report
         → Populate audit_report (engine schema)
         → domain = WORKFLOW; audit_id = WFA-...

STEP 6:  Present to user
         → Deliver the audit report
         → Offer: "Want me to drill into any specific layer or finding?"
         → If post_mortem: present root_cause mapping
         → If diff: present comparative table
         → If iterative (Mode 5): proceed per engine M5 procedure

STEP 7:  Route on user confirmation
         → User confirms routing queues
         → Findings routed to companion skills or user action

MODE 5:  Steps M5-1 through M5-10 are owned by @audit-engine.
         Each granular pass (M5-3) runs all 8 workflow layers per the
         engine's per-check protocol. Element boundary for M5-3 is:
           1. Numbered/lettered list item
              (regex: ^\s*(\d+|[A-Za-z]|[ivxIVX]+)[\.\)]\s+)
           2. Markdown heading section (#…######)
           3. Fenced code block
           4. Prose paragraph
         (Use the first matching level; never blend levels.)
```
