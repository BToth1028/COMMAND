---
name: audit-engine
description: >-
  Domain-agnostic iterative audit orchestrator. Runs the 5-mode audit framework
  (FULL / TARGETED / POST_MORTEM / DIFF / ITERATIVE) and dispatches to the
  embedded workflow-audit and code-audit reference modules, or both, depending
  on content type. Owns the Mode 5 iterative loop, halt protocols,
  atomic-clause coverage at plan-Intent review, state externalization,
  tier-rating skeleton, output-contract skeleton, anti-drift safeguards,
  content-type detection, mixed-content dispatch, and the integration-audit
  framework. Reference modules live at
  `references/audit_workflow.yaml` and `references/audit_code.yaml` inside this
  command's folder. Invoke as `@audit-engine` (auto-detect with user
  confirmation), `@audit-engine workflow`, `@audit-engine code`, or
  `@audit-engine mixed`. Audits only — never modifies. The deliverable is an
  audit report plus a proposal-only remediation plan; execution is handed off
  to a separate session.
---

# Audit-Engine

> **Directive vocabulary.** The keywords MUST, MUST NOT, REQUIRED, SHALL,
> SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this
> document and in `references/audit_workflow.yaml` / `references/audit_code.yaml`
> are to be interpreted as described in
> [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and
> [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174). This citation is
> stated once here; reference modules inherit it by reference.

## What this command is

`@audit-engine` is the **orchestrator** for all audit work in this command
family. It owns:

- The audit-mode taxonomy (Modes 1–5) and the per-check protocol
  (PASS / FAIL / PARTIAL / SKIPPED).
- The Mode 5 iterative loop (10 steps), including all halt protocols.
- The output-contract skeleton (`audit_report` shape, `finding` schema,
  `iteration` block, `remediation_plan` block).
- The tier-rating skeleton (A–F bands + universal overrides).
- Anti-drift safeguards.
- **Content-type detection** — closed-rule heuristic that decides whether
  the input is a workflow, code, or mixed; followed by a user-confirmation
  gate before dispatch.
- **Mixed-content dispatch** — partitions input, runs single-domain
  sub-audits, then runs the integration audit.
- The **integration-audit framework** — nine layers covering the
  workflow ↔ code seam.

`@audit-engine` does NOT own:

- Workflow-specific audit layers / checks → `references/audit_workflow.yaml` owns these.
- Code-specific audit layers / checks → `references/audit_code.yaml` owns these.
- Domain-specific tier overrides (each reference module contributes its own).

## Embedded reference modules

- **`references/audit_workflow.yaml`** — workflow-domain auditor (prompts,
  SKILL.md files, runbooks, YAML agent specs, COMMAND.md files; see
  §"Content-type detection" Rule 2.1 for the closed extension list).
  Canonical path: `C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_workflow.yaml`.
- **`references/audit_code.yaml`** — code-domain auditor (source files,
  packages, PRs, repos). Also hosts the subagent two-stage gate methodology
  for subagent-driven development.
  Canonical path: `C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_code.yaml`.

`@audit-engine` loads and invokes these modules as substeps in domain and mixed-content runs.

## Existing skills are unaffected

This command does NOT alter the existing `workflow-auditor` and
`code-review---iterative` skills. Those still auto-fire on natural-language
audit prompts. Use `@audit-engine` (with its embedded reference modules) when
you want the engine-based framework explicitly.

---

## Authority Model

**Canonical (ground truth):**

- The artifact being audited (workflow, code, or both — as provided by user).
- The user's stated intent for the artifact.
- For mixed-content audits: the workflow side is canonical for "what this
  is supposed to do"; the code side is canonical for "what this actually
  does." Mismatches → integration findings.

**Derived (rebuildable from canonical):**

- Audit reports, layer scores, tier ratings, finding queues, remediation plans.

**Rule:** Never modify the artifact under audit. Never assume intent the
user has not stated. If the artifact's purpose is ambiguous, halt and ask
before auditing — an audit without a known target is meaningless.

---

## Scope / Non-Scope

**In scope:** Running the 5-mode audit framework. Dispatching to
domain-specific commands. Running the integration audit on mixed content.
Producing scored reports with tier ratings and proposal-only remediation
plans. Comparing two versions of an artifact. Post-mortem analysis after a
production failure.

**Never:** Rewrite or fix anything. Author new content. Make domain truth
judgments about subject matter. Skip layers. Soften findings. Operate
without an artifact loaded. Apply a remediation plan even after user
approval — execution is a separate session.

---

## Invocation

```
@audit-engine [<content_type>] [<mode>]
```

- `<content_type>` (optional) ∈ `{workflow, code, mixed}`. If provided,
  detection is skipped (explicit-override fast-path). If omitted, the
  engine automatically determines content type from the document's leading
  content (see §"Content-type detection"). The engine NEVER asks the user
  to declare or confirm content type.
- `<mode>` is always `iterative`. **Iterative is the unconditional default
  for all content types and all runs. The agent never prompts the user for
  a mode and never accepts a mode negotiation.** `iterative` wraps `full`,
  `post_mortem`, or `diff` as the base mode.

Examples:

- `@audit-engine` — auto-detect from document leading content; iterative mode always.
- `@audit-engine workflow` — explicit override: skip detection, force workflow audit, iterative.
- `@audit-engine code` — explicit override: skip detection, force code audit, iterative.
- `@audit-engine mixed` — explicit override: skip detection, force mixed sequencing, iterative.

---

## Pre-flight verification

Run BEFORE any audit (Phase 0 detection, single-domain dispatch, or
mixed-content dispatch). The checks are deterministic and execute in
strict order. Any failure halts immediately with
`halt_reason: PRE_FLIGHT_FAILURE`; record the specific check that
failed in `iteration_log[0].notes` (Mode 5) or
`decision_trace.auditor_notes` (Modes 1–4).

```yaml
preflight_checks:
  PF-1:
    description: "Engine canonical file is loaded and readable."
    target: "C:\\Users\\rtoth\\.cursor\\commands\\audit-engine\\COMMAND.md"
    fail_condition: "File missing, unreadable, or zero bytes."
  PF-2:
    description: "Workflow-audit reference file is loaded and readable."
    target: "C:\\Users\\rtoth\\.cursor\\commands\\audit-engine\\references\\audit_workflow.yaml"
    fail_condition: "File missing, unreadable, or zero bytes."
  PF-3:
    description: "Code-audit reference file is loaded and readable."
    target: "C:\\Users\\rtoth\\.cursor\\commands\\audit-engine\\references\\audit_code.yaml"
    fail_condition: "File missing, unreadable, or zero bytes."
  PF-4:
    description: "context-bootstrap command is present and readable."
    target: "C:\\Users\\rtoth\\.cursor\\commands\\bootstrap"
    fail_condition: "Command folder missing or unreadable."
  PF-5:
    description: "deterministic-prompt-builder skill is registered for the agent."
    target: "skill: deterministic-prompt-builder"
    fail_condition: "Skill not present in available_skills."
  PF-6:
    description: "Artifact under audit is loaded and read-once."
    target: "user-supplied artifact path(s)"
    fail_condition: >
      No artifact loaded, OR an artifact path was loaded more than once
      in this run (re-reads must be explicit, not implicit).

on_any_failure:
  action: "HALT immediately."
  halt_reason: "PRE_FLIGHT_FAILURE"
  record:
    - field: "iteration_log[0].notes (Mode 5) OR decision_trace.auditor_notes"
      value: "PF-N failed: <check description>"
  do_not: "Proceed to detection, partition, or any sub-audit."
```

Pre-flight is mandatory; it MUST NOT be skipped by explicit-override
invocation (`@audit-engine workflow|code|mixed`). The override skips
content-type detection, not pre-flight.

---

## Audit-Mode Taxonomy

### Mode 1 — FULL (default for single-domain)

Run all the domain's layers in order. None optional. Emit a complete audit
report with per-layer scores and an overall tier rating.

### Mode 2 — TARGETED

Run a user-specified subset of layers. All checks within selected layers
still execute — no partial layers. Emit a scoped audit report.

### Mode 3 — POST_MORTEM

The artifact has already failed in production. User provides the artifact
plus a failure description. Run all layers, then trace the failure back to
specific findings. Emit a post-mortem report with root-cause mapping.

### Mode 4 — DIFF

Compare two versions of an artifact. Run all layers against both. Emit a
comparative report showing which version scores higher per layer and
whether changes introduced regressions.

### Mode 5 — ITERATIVE

Wrap Mode 1, 3, or 4 in a multi-pass loop with explicit user gates. Each
pass runs all the domain's layers against the artifact. Findings persist
across passes. **Loop exits only after two consecutive clean passes.** The
loop produces the standard `audit_report` PLUS a `remediation_plan`.

The plan is **proposal-only** (see §Anti-Drift §7 for the canonical
no-execute rule). A separate agent in a separate session is the
executor.

Mode 5 is the **unconditional default for all runs** — single-domain and
mixed. The agent never prompts for or negotiates a mode. The explicit
Intent gate at Step M5-2 benefits every audit, not just mixed-content.

---

## Per-Check Error Protocol

Every check produces one of: PASS, FAIL, PARTIAL, or SKIPPED.

```yaml
per_check_error_handling:
  PARTIAL:
    trigger: "Check cannot produce a definitive PASS or FAIL"
    action: >
      Record result as PARTIAL. Include both possible interpretations in
      the finding record. Weight as 0.5 in layer scoring (half credit).
    required_fields: "Both interpretations must appear in finding.evidence"

  SKIPPED:
    trigger: "Check is inapplicable to the artifact's format/language"
    action: >
      Record result as SKIPPED. Exclude from layer score denominator
      (do not penalize for inapplicable checks). Note reason in
      finding.description.
    examples:
      - "YAML structure checks SKIPPED for FREEFORM workflows"
      - "Concurrency checks SKIPPED for synchronous-only code"
```

---

## Layer-Failure Protocol

If a layer cannot complete (corrupted content, unreadable section, agent
uncertainty on every check):

```yaml
layer_failure:
  action:
    - Record layer score as INCOMPLETE (not 0, not estimated)
    - Continue to next layer — do not halt the full audit
    - Set audit_report.overall.tier_overrides to include:
        condition: "Layer [ID] could not complete"
        cap: "C"
        reason: "Incomplete layer — audit results are partial"
    - Record in decision_trace.auditor_notes: which layer failed and why
  rule: "An incomplete layer is better than a halted audit."
```

---

## Scoring & Tier Rating Skeleton

### Layer Scores

Each layer produces a score 0–100. The exact formula is owned by the domain
command (workflow-audit / code-audit / integration). Convention: each check
within a layer is weighted equally; `score = (checks_passed / N) × 100`.
PARTIAL counts as 0.5; SKIPPED is excluded from the denominator.

### Overall Score

Weighted average of layer scores. Layer weights are defined per domain
(see `references/audit_workflow.yaml` and `references/audit_code.yaml`).
The weights MUST sum to 1.0.

### Tier Map (universal A–F)

```yaml
TIER_MAP:
  A: 90–100   # Production-ready. Minor advisory findings only.
  B: 75–89    # Deployable with known risks. No critical findings.
  C: 60–74    # Needs work. One or more layers have serious gaps.
  D: 40–59    # Significant rework required. Multiple critical findings.
  F:  0–39    # Not deployable. Fundamental structural problems.
```

### Universal Tier Overrides (apply to all domains)

```yaml
universal_overrides:
  - condition: "Any CRITICAL severity finding exists in any layer"
    cap: "C"
    reason: "Critical findings must be resolved before deployment"

  - condition: "Layer 5 (or domain equivalent of 'Internal Consistency') has any contradiction finding"
    cap: "C"
    reason: "Self-contradicting artifacts produce unpredictable behavior"
```

### Domain-Specific Override Slot

Each domain command MAY add overrides on top of the universal set. The
combined list is `universal_overrides ∪ domain_overrides`. Conflicts (same
condition with different cap) are resolved by taking the **stricter** cap.

Example: `audit_workflow.yaml` adds a "L1-Determinism ≥ 2 FAILed checks → cap D"
override; `audit_code.yaml` adds a "any CRITICAL security finding → cap D" override.
Both stack on top of the universal overrides.

### Composite Tier (mixed-content runs only)

For mixed-content audits, the engine produces three sub-tiers (workflow,
code, integration) and a **composite tier** = `min(tier_W, tier_C, tier_I)`.
The weakest sub-tier caps the composite. Rationale: a workflow that audits
A but pairs with code that audits D is not deployable as a unit.

---

## Finding Severity Definitions (universal)

```yaml
severity_definitions:
  CRITICAL:
    IS: >
      The artifact will produce wrong results, crash, expose vulnerability,
      or enter an unrecoverable state. Deployment risks wasted hours,
      corrupted outputs, or security incidents.
    IS_NOT: "A style preference. A theoretical concern. An optimization opportunity."

  MAJOR:
    IS: >
      The artifact will produce unreliable, inconsistent, or incomplete
      results under plausible real-world conditions. Not every run will
      fail, but enough will to erode trust.
    IS_NOT: "A guaranteed failure. A minor style issue."

  MINOR:
    IS: >
      The artifact usually works but has rough edges that increase
      fragility, reduce maintainability, or cause occasional unexpected
      behavior.
    IS_NOT: "A deployment blocker. A purely cosmetic issue."

  ADVISORY:
    IS: >
      A recommendation for improvement. The artifact functions correctly
      without this change but would be better with it.
    IS_NOT: "A problem. A finding that requires action."
```

---

## Output Contract Skeleton

### `audit_report` shell

```yaml
audit_report:
  audit_id:           [string]        # Format: AE-YYYYMMDD-HHMMSS (engine-level), or
                                      # WFA-... (workflow-audit), CDA-... (code-audit),
                                      # INT-... (integration), or composite for mixed
  mode:               [enum]          # FULL | TARGETED | POST_MORTEM | DIFF
  domain:             [enum]          # WORKFLOW | CODE | INTEGRATION | COMPOSITE
  artifact_format:    [string]        # Domain-specific (workflow_format or language/repo)
  stated_intent:      [string]        # User-confirmed intent statement
  executed_at:        [timestamp]     # ISO 8601

  overall:
    score:            [integer]       # 0–100 weighted average
    tier:             [enum]          # A | B | C | D | F
    tier_overrides:   [list<override> | null]
    verdict:          [string]        # One-sentence summary

  layers:
    - layer_id:       [string]
      layer_name:     [string]
      score:          [integer]       # 0–100
      weight:         [float]
      checks:
        - check_id:   [string]
          check_name: [string]
          result:     [PASS | FAIL | PARTIAL | SKIPPED]
          findings:   [list<finding>]

  finding_summary:
    total:            [integer]
    by_severity:
      CRITICAL:       [integer]
      MAJOR:          [integer]
      MINOR:          [integer]
      ADVISORY:       [integer]
    by_layer:         [map<layer_id, integer>]

  finding_queue:      [list<finding>]   # Sorted: severity DESC, layer order ASC

  routing:
    prompt_builder_queue:   [list<string>]
    user_action_queue:      [list<string>]
    informational:          [list<string>]

  # POST_MORTEM mode only:
  root_cause:
    failure_description:    [string | null]
    mapped_findings:        [list<string>]
    unmapped_factors:       [list<string>]
    confidence:             [enum]          # HIGH | MEDIUM | LOW

  decision_trace:
    mode_selected:          [string]
    layers_executed:        [list<string>]
    overrides_applied:      [list<string>]
    auditor_notes:          [list<string>]
    detection_path:         [string | null]   # "explicit_override" | "heuristic_confirmed" |
                                              # "heuristic_overridden_by_user" |
                                              # "ambiguous_user_declared" | null
    detection_classification: [enum | null]   # workflow | code | mixed | null

  # Mode 5 only — null otherwise. Schema in §"Mode 5 — output additions".
  iteration:                [iteration_block | null]
  remediation_plan:         [remediation_plan_block | null]

  # Composite (mixed-content) only — null otherwise.
  composite:                [composite_block | null]
```

### `finding` schema

```yaml
finding:
  finding_id:         [string]        # F-<layer_id>-<sequence>
  check_id:           [string]
  layer_id:           [string]
  severity:           [enum]          # CRITICAL | MAJOR | MINOR | ADVISORY
  category:           [enum]          # Domain-specific; common values:
                                      # AMBIGUITY | BROKEN_REF | STALE_REF |
                                      # UNREACHABLE | UNHANDLED | CONTRADICTION |
                                      # SCOPE_LEAK | ASSUMPTION | REDUNDANCY |
                                      # STRUCTURAL | UNVERIFIABLE
                                      # (code-audit and integration-audit may
                                      # extend this enum — see those commands)
  location:           [string]        # Where in the artifact (file:line or step ID)
  description:        [string]
  evidence:           [string]        # Verbatim text or structure that triggered finding
  impact:             [string]
  remediation:        [string]        # Concrete fix recommendation (NOT applied)
  routing:            [enum]          # PROMPT_BUILDER | USER_ACTION | INFORMATIONAL
  pass_number:        [integer | null]   # Mode 5 only — pass on which finding first surfaced
  determinism_certification: [object | null]  # REQUIRED iff remediation is non-empty
                                              # AND mode ∈ {1, 2, 3, 4}. Closed-shape
                                              # block per §"Solution Determinism Gate".
                                              # In Mode 5 this field is null on the
                                              # finding; the certification lives on the
                                              # derived plan item instead.
  gate_attempts:      [integer | null]        # 0..2 — retry counter for §"Solution
                                              # Determinism Gate". Null in Mode 5
                                              # (counter lives on the plan item).
```

### Mode 5 — output additions (`iteration` and `remediation_plan`)

In Mode 5, two additional blocks are populated. In Modes 1–4 these blocks
MUST be `null`.

```yaml
audit_report:
  iteration:                              # Mode 5 only
    enabled:                [bool]
    base_mode:              [enum]        # FULL | POST_MORTEM | DIFF
    pass_count:             [integer]
    pass_budget:            [integer]     # Default 10; user override 4..30
    clean_passes:           [integer]     # Must be 2 for normal exit
    intent_approved_at_pass: [integer]
    bootstrap_scratchpad_id: [string]     # ID of the scratchpad section in
                                          # context-bootstrap holding externalized
                                          # Mode 5 state across passes.
    halt_reason:            [enum | null] # null on normal exit; otherwise:
                                          # INTENT_NOT_APPROVED | INTENT_DRIFT |
                                          # PLAN_REVISION_EXHAUSTED | USER_HALT |
                                          # GRANULAR_PASS_FAILURE | USER_TIMEOUT |
                                          # DEDUP_FAILURE | ITERATION_BUDGET_EXHAUSTED |
                                          # PRE_FLIGHT_FAILURE | PARTITION_FAILURE |
                                          # DETERMINISM_GATE_EXHAUSTED
    iteration_log:
      - pass_number:        [integer]
        started_at:         [timestamp]
        ended_at:           [timestamp]
        findings_count:     [integer]
        new_findings_count: [integer]
        pass_status:        [enum]        # COMPLETE | INCOMPLETE
        notes:              [string | null]

  remediation_plan:                       # Mode 5 only
    intent_anchor:          [string]      # User-approved Intent (immutable in run)
    items:
      - plan_id:            [string]      # P-<sequence>
        finding_ids:        [list<string>]
        action:             [enum]        # ADD | REMOVE | UPDATE | REPLACE | SPLIT | MERGE
        target:             [string]      # Section / step / line range / file:line
        change:             [string]      # Concrete change description (proposal text).
                                          # MUST be ≤ 60 words AND describe action+target only.
                                          # MUST NOT contain a full re-authored section, full
                                          # replacement source body, or complete prose
                                          # paragraphs intended for verbatim insertion.
                                          # Long-form rewrites: route via routing=PROMPT_BUILDER
                                          # and reference under prompt_builder_substeps;
                                          # the executor session generates the new text.
        severity:           [enum]
        routing:            [enum]
        depends_on:         [list<string>]
        locked:             [bool]        # PARTIAL-approval persistence flag.
                                          # false on plan creation; flipped to true at
                                          # Step M5-10 when the user accepts this item
                                          # under user_approval.status = PARTIAL.
                                          # When a re-audit runs after PARTIAL, findings
                                          # already resolved by a locked item are excluded
                                          # from subsequent passes.
        determinism_certification: [object]    # REQUIRED. Closed-shape block per
                                               # §"Solution Determinism Gate". Item MUST
                                               # NOT be present in items[] without a
                                               # certification whose verdict == PASS.
        gate_attempts:      [integer]          # 0..2. Number of times Step M5-8.5
                                               # re-derived this item before PASS.
                                               # Reaching 3 attempts triggers
                                               # DETERMINISM_GATE_EXHAUSTED halt.
    ordering_rule:          "Severity-first (CRITICAL → ADVISORY), then layer order, then dependency topological order."
    prompt_builder_substeps:
      - plan_id:            [string]
        rationale:          [string]
    plan_review:
      satisfies_intent:     [bool]        # Computed by atomic-clause coverage at M5-9
      revision_rounds:      [integer]     # 0–3
      gaps_if_unsatisfied:  [list<string>]   # Verbatim clauses with zero coverage
      intent_clauses:       [list<string>]   # Atomic clauses split from intent_anchor (1–5)
      clause_coverage:
        - clause:                  [string]
          plan_item_ids:           [list<string>]
          existing_step_locations: [list<string>]
    user_approval:
      status:               [enum]        # PENDING | APPROVED | REJECTED | PARTIAL
      rationale:            [string | null]
      decided_at:           [timestamp | null]
```

### Composite (mixed-content) additions

```yaml
audit_report:
  composite:                              # Mixed-content runs only
    workflow_audit_id:      [string]      # WFA-... id of sub-report
    code_audit_id:          [string]      # CDA-... id of sub-report
    integration_audit_id:   [string]      # INT-... id of sub-report
    sub_tiers:
      workflow:             [enum]        # A | B | C | D | F
      code:                 [enum]
      integration:          [enum]
    composite_tier:         [enum]        # min(workflow, code, integration)
    seam_findings:          [list<string>]   # finding_ids classified as seam-only
```

---

## Anti-Drift Safeguards

1. **No modification.** Never edit, rewrite, or "improve" the artifact
   under audit. Findings describe problems. Remediation fields propose
   fixes. The auditor does not apply them.
2. **No skipping.** All checks within an executed layer run. A skipped
   check is an unverified claim.
3. **No grade inflation.** If a check fails, it fails. Do not soften
   findings to avoid difficult conversations.
4. **No domain judgment beyond layer remit.** The auditor evaluates
   structural soundness, internal consistency, and executability — not
   whether the artifact's subject-matter conclusions are correct.
5. **Findings before routing.** Always present the full audit report to
   the user before routing any findings.
6. **Separation of concerns.** Do not mix audit and construction work in
   the same session. Route construction work to a separate skill or
   session.
7. **Mode 5 — plan, do not apply (canonical).** Mode 5 IS permitted to
   author a `remediation_plan`. Mode 5 is **NOT** permitted to apply
   any plan item, EVEN AFTER user approval. Plan execution belongs to
   a separate agent in a separate session. **This is the single
   canonical statement of the no-execute rule.** All other references
   in this command family — including the §Audit-Mode Taxonomy Mode 5
   description and the Step M5-8 closing line — cite §Anti-Drift §7
   rather than re-stating the rule.
8. **Mode 5 Intent immutability.** After Workflow/Artifact Intent is
   approved at Step M5-2, it is the anti-drift anchor for the rest of
   the run and is immutable within that run. If the auditor concludes
   the Intent itself is misstated, HALT (`halt_reason: INTENT_DRIFT`)
   and notify the user. Do not silently revise.
9. **Mode 5 two-pass exit only.** A single clean pass is a candidate,
   never a confirmation. Exit requires **two consecutive clean passes**.
   *Exception — Phase INT-A only:* the integration sub-audit in a
   mixed-content run exits after the **first single clean pass**. Rationale:
   the integration surface is bounded by the two domain audits that each
   already required two consecutive clean passes; a single clean pass is
   sufficient for convergence at the seam level. All other Mode 5 loops
   (Phase A, Phase B, single-domain runs) require two consecutive clean passes.
10. **Mixed-content sub-audits are isolated.** When dispatching to
    `references/audit_workflow.yaml` and `references/audit_code.yaml`, each
    sub-audit runs against its partition independently. Cross-domain
    findings appear ONLY in the integration audit, never as a re-finding
    inside a sub-audit.
11. **Automatic classification only.** The engine determines content type
    from the document's leading content (see §"Content-type detection").
    It never asks the user to declare, confirm, or override content type.
    `decision_trace.detection_path` records the classification path taken.
12. **Solution Determinism Gate.** No proposed remediation may be
    presented for review without a `verdict: PASS`
    `determinism_certification` per §"Solution Determinism Gate". This
    applies to per-finding `remediation` fields (Modes 1–4) and to
    per-plan-item `change` fields (Mode 5). The gate is mechanical, not
    judgmental — the 5-rule rubric is closed and rules MUST NOT be
    softened to coerce a PASS. A remediation that bypasses the gate is
    itself a finding against the auditor and triggers
    `halt_reason: DETERMINISM_GATE_EXHAUSTED` after the bounded retry
    budget defined in §"Solution Determinism Gate" > retry_protocol.

---

## Deterministic vocabulary

This section is the **single canonical source** for terms used as
severity-bias triggers, scope qualifiers, and threshold modifiers
across `@audit-engine`, `references/audit_workflow.yaml`, and
`references/audit_code.yaml`. Reference modules inherit by reference;
no module redefines a term locally. If an audit needs a term not on
this list, add it here first — never inline.

```yaml
deterministic_vocabulary:

  primary_execution_path:
    workflow_definition: >
      The set of steps reachable from the mission/main statement under
      the artifact's default conditional branches (no error branches,
      no opt-in branches, no debug-only branches).
    code_definition: >
      The set of symbols reachable from the public entry point(s) named
      in `stated_intent` via direct call edges (no error-handler edges,
      no debug-only edges, no test fixtures).
    forbidden_synonyms: ["main path", "happy path", "primary flow", "core flow"]

  downstream_system:
    closed_list:
      - "CLI stdout / exit-code consumed by another command"
      - "HTTP / RPC response consumed by another service"
      - "File-system write read by a separate process or user"
      - "Queue / topic publish consumed by another worker"
      - "Database write read by another query path"
      - "IPC channel (pipe, socket, shared memory) read by another process"
      - "Return value consumed by a documented external caller (in stated_intent)"
    note: >
      A use is a downstream system iff it matches at least one bullet
      above. Internal use within the same module/process is NOT
      downstream.

  primary_use_case:
    rule: >
      Any use-case explicitly named in `stated_intent`, OR any use-case
      described under a §Scope / §In-scope / §Use cases heading in the
      artifact under audit. Anything else is NOT a primary use-case for
      severity bias.

  expected_load:
    closed_thresholds:
      throughput: ">= 10 invocations / second"
      input_size: ">= 1 MB single input"
      concurrency: ">= 1000 concurrent users / sessions"
      batch_size: ">= 10^6 items in a single batch"
    if_artifact_silent:
      severity_cap: "MAJOR"
      rule: >
        If none of the above are cited in the artifact, performance
        findings cap at MAJOR (not CRITICAL).

  long_form_rewriting:
    trigger: >
      Proposed `change` text exceeds 60 words, OR would replace one or
      more fenced code blocks, OR would replace one or more numbered
      lists, OR would replace three or more prose paragraphs in the
      artifact under audit.
    routing_rule: >
      Set finding.routing = PROMPT_BUILDER and add the plan_id to
      remediation_plan.prompt_builder_substeps. Mode 5 does NOT author
      the long-form text; the executor session does.

  single_threaded_synchronous:
    rule: >
      Scope contains zero occurrences of language-specific concurrency
      keywords. Per-language closed lists below. The artifact qualifies
      as `single_threaded_synchronous` IFF no listed keyword is present
      anywhere in scope.
    keyword_lists:
      python:    "async | await | asyncio | threading | multiprocessing | concurrent\\.futures"
      js_ts:     "async | await | Promise | Worker | setImmediate | setTimeout.*callback | queueMicrotask"
      rust:      "async | await | tokio | rayon | std::thread | std::sync"
      go:        "go\\s | goroutine | chan\\s | select\\s"
      java_kt:   "CompletableFuture | ExecutorService | Thread | coroutine | suspend"
      ruby:      "Thread | Fiber | Async | Concurrent::"
      csharp:    "async | await | Task | Thread | Parallel"
      c_cpp:     "pthread | std::thread | std::async | OpenMP | MPI"

  implicit_knowledge:
    rule: >
      Any reference to a person, place, decision, convention, or
      external system that is NOT (a) stated within the artifact under
      audit, NOR (b) defined in the agent's documented skill set, NOR
      (c) reachable at a verifiable external URL or filesystem path.

  task_complexity:
    measure: >
      Count of distinct decision points (IF/ELSE branches, loops,
      error-recovery paths) in the algorithm under audit.
    bands:
      simple:    "<= 5"
      moderate:  "6 .. 15"
      complex:   "> 15"

  non_blank_line:
    rule: >
      A line with at least one non-whitespace character that is NOT
      exclusively one of the following comment forms:
        - HTML comment:        `<!-- ... -->`
        - Shell / Python:      `# ...`
        - C / C++ / JS / TS / Rust / Go / Java line comment: `// ...`
        - SQL line comment:    `-- ...`
        - C-style block:       `/* ... */`
    application: >
      Used by Rule 2.1 (20-non-blank-line threshold) and by Phase 0
      partition (20-non-blank-line code block split).

  junk_drawer:
    rule: >
      A module / package containing >= 3 unrelated responsibility
      groups, where "responsibility group" follows the standard SRP
      definition (one reason to change). Naming containing the literal
      tokens `utils`, `helpers`, `misc`, `common`, `shared`,
      `lib_internal` is a strong indicator and triggers manual SRP
      review; the count threshold is the deciding criterion.

  stricter_cap:
    rule: >
      Given two tier caps X and Y from the universal-overrides set or a
      domain-overrides set, the stricter cap is the lower-letter cap in
      the order F < D < C < B < A. If equal, the override is idempotent
      (no change). Example: cap=C overrides cap=B; cap=D overrides cap=C.

  build_artifact:
    rule: >
      A file in the source tree that the project's build system
      produces from non-this-file inputs. Closed examples:
        - Python compiled bytecode:  `.pyc`, `.pyo`, `__pycache__/*`
        - JS/TS transpiler output:   `dist/*`, `build/*`, `out/*`
        - Generated stubs:           `*_pb2.py`, `*.pb.go`, `*.gen.ts` from `.proto`
        - Bundler output:            `bundle.js`, `*.min.js`, `*.map`
    application: >
      Audits SHALL NOT score build artifacts. If a build artifact is
      loaded as audit input, halt with `PRE_FLIGHT_FAILURE` and ask the
      user for the source file.
```

Reference modules cite this section as `§Deterministic vocabulary > <term>`.
No synonyms. Soft phrases like "typically the main path" are findings
under Layer 1 (Determinism) when they appear in the artifact under audit
AND are findings against the auditor itself when they appear in this
command or its reference modules.

---

## Solution Determinism Gate

Every proposed remediation MUST pass this gate before it can appear in any
output presented to the user. The gate is mechanical — closed-shape
certification, closed rubric, closed retry budget. No free judgment.

### Canonical question (verbatim, locked)

> **What is the RIGHT answer? NOT the easiest OR quickest answer; the
> right AND the MOST DETERMINISTIC choice that can be made.**

This text is the canonical, citable phrasing of the gate. Reference
modules cite this section as `§Solution Determinism Gate`. No module
restates or paraphrases the question.

### Scope of application

The gate applies to:

- `finding.remediation` — for every finding whose `remediation` field is
  non-empty, in **all modes** (Mode 1 through Mode 5).
- `remediation_plan.items[].change` — for every plan item, in **Mode 5**.

A remediation that bypasses the gate is itself a finding against the
auditor (Anti-Drift §12).

### `determinism_certification` schema (closed-shape)

Every covered remediation MUST carry a `determinism_certification` block
with these fields and only these fields:

```yaml
determinism_certification:
  alternatives_considered:    [list<string>]   # ≥ 2 entries — the chosen approach
                                               # plus at least one rejected alternative.
                                               # Each entry is a one-sentence summary.
  chosen_approach:            [string]         # Verbatim copy of one entry from
                                               # alternatives_considered.
  authority_citations:        [list<string>]   # ≥ 1 entry citing a normative source
                                               # (file path + line range, schema field,
                                               # rule ID, vocabulary term, etc.) that
                                               # the chosen approach respects.
  sources_of_truth_delta:     [enum]           # REDUCED | UNCHANGED | INCREASED
                                               # Counts sources of truth for the affected
                                               # concern AFTER remediation vs BEFORE.
                                               # INCREASED auto-fails Rule 3.
  same_input_same_output:     [bool]           # Does the remediation surface satisfy
                                               # "same input → same output, every time"
                                               # for the concern it remediates?
  easiest_path_flag:          [bool]           # true iff the chosen approach is also
                                               # the easiest/quickest of the
                                               # alternatives_considered.
  easiest_path_justification: [string | null]  # REQUIRED iff easiest_path_flag = true.
                                               # Must explain why ease and rightness
                                               # coincide here. null otherwise.
  verdict:                    [enum]           # PASS | FAIL — set by rubric below.
  failure_reason:             [string | null]  # REQUIRED iff verdict = FAIL. Cites the
                                               # specific rule(s) the certification
                                               # violated. null on PASS.
```

### Pass rubric (closed; ALL FIVE must be true)

```yaml
pass_rubric:
  rule_1_alternatives_considered:
    requires:
      - "len(alternatives_considered) >= 2"
      - "chosen_approach is a verbatim entry in alternatives_considered"
    fails_when: >
      Either condition is false. Single-option proposals fail; "I'll do X"
      without naming what X was chosen over fails.

  rule_2_authority_grounded:
    requires:
      - "len(authority_citations) >= 1"
      - "Every cited authority is reachable (file path + line range, schema
        field name, vocabulary term, or in-document section reference)"
    fails_when: >
      No authority cited, OR a cited authority cannot be resolved to a
      concrete location. Free-floating "best practice" claims fail.

  rule_3_sources_of_truth_not_increased:
    requires:
      - "sources_of_truth_delta != INCREASED"
    fails_when: >
      The remediation introduces a second authoritative source for a fact
      that already has one (e.g. adding a metadata field that duplicates
      what folder location, an existing field, or upstream system already
      tells us). REDUCED and UNCHANGED both pass.

  rule_4_same_input_same_output:
    requires:
      - "same_input_same_output == true"
    fails_when: >
      The remediation surface — the concern under remediation — would
      produce different outputs from identical inputs across runs after
      the fix is applied.

  rule_5_easiness_check:
    requires:
      - "easiest_path_flag == false, OR easiest_path_justification is non-empty
        AND explicitly cites why ease and rightness coincide for this case"
    fails_when: >
      The chosen approach is the easiest of the alternatives_considered AND
      the certification offers no justification for why ease is not a red
      flag here.

verdict_assignment:
  rule: "verdict = PASS iff all five rules pass; otherwise verdict = FAIL"
  ties: "There are no ties — the rubric is total."
```

### Retry budget and halt protocol

```yaml
retry_protocol:
  budget: 2                             # initial attempt + 2 retries = 3 total
  on_first_fail:
    action: "Re-derive the remediation using failure_reason as guidance."
    increment: "gate_attempts += 1"
    do_not: "Soften the rubric. Do not weaken any rule to force a PASS."
  on_second_fail:
    action: "Re-derive once more."
    increment: "gate_attempts += 1"
  on_third_fail:
    action: "HALT this remediation."
    halt_reason: "DETERMINISM_GATE_EXHAUSTED"
    surface_to_user:
      - field: "Each attempt's chosen_approach"
        verbatim: true
      - field: "Each attempt's failure_reason"
        verbatim: true
      - field: "The finding(s) the remediation was meant to address"
        verbatim: true
    do_not:
      - "Present the failed remediation to the user as a plan item."
      - "Silently drop the finding."
    user_resolution: >
      The user MAY (a) accept a remediation despite gate failure (recorded
      with explicit user_override = true, audit-trail preserved), (b) revise
      the artifact's authorities so a passing remediation becomes derivable,
      or (c) accept the finding as-is without a remediation plan item.
```

### Operational note

The gate is per-remediation, not per-finding. A finding with multiple
candidate remediations (rare; happens when one finding spawns two plan
items) certifies each independently. A finding with no remediation
(`finding.remediation` empty AND no plan item references it) does not
trigger the gate.

---

## Content-type detection

When the user invokes `@audit-engine`, the engine determines content type
automatically — it NEVER asks the user to declare, confirm, or override
content type. The detection rule is deterministic and based solely on
what the document **starts with**.

### Layer 1 — Explicit-override fast-path

If the invocation includes one of `workflow|code|mixed`, that value is
used directly. Skip all detection. Record
`decision_trace.detection_path = "explicit_override"` and
`decision_trace.detection_classification = <value>`. Proceed to dispatch.

### Layer 2 — Leading-content detection (deterministic, no user prompt)

If no explicit override, read the document and classify based on the
**first substantive content block** encountered in document order:

#### Rule 2.1 — Single file

| Extension | Leading content | Decision |
| --- | --- | --- |
| `.md`, `.markdown`, `.mdc`, `.yaml`, `.yml` | First substantive block is prose, headings, or a list | **workflow** |
| `.md`, `.markdown`, `.mdc`, `.yaml`, `.yml` | First substantive block is a fenced code block with a language tag from the code-extension list OR ≥ 20 non-blank lines | **mixed — workflow contains code** (workflow leads) |
| `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.rs`, `.go`, `.java`, `.kt`, `.rb`, `.cs`, `.cpp`, `.c`, `.h`, `.hpp`, `.swift`, `.scala`, `.ex`, `.exs`, `.clj`, `.ml`, `.lua`, `.sh`, `.ps1` | Always | **code** |
| Anything else | n/a | Default to **workflow**. Record `detection_path = "extension_defaulted"`. |

The `code-extension list` is the closed set used for both direct extension
matching and fenced-block language-tag matching.

**"Starts with" sequencing rule for mixed content:** When a document
contains both workflow and code content, the domain that appears **first**
in document order is audited **first** to full iterative completion. The
second domain is audited after the first reaches two consecutive clean
passes. This applies regardless of how many times either domain appears.

#### Rule 2.2 — Multi-file (folder or path list)

Classify each file per Rule 2.1. Sequence audits in the order files are
provided. If all files are the same domain, run as a single-domain audit.
If domains are mixed, sequence by the leading domain of the first file.

#### Rule 2.3 — Determinism guarantee

Same input → same detection → same sequencing, every time. No judgment,
no user prompts, no exceptions. Record `decision_trace.detection_path =
"leading_content_heuristic"` and `decision_trace.detection_classification
= <value>`.

---

## Mixed-content dispatch protocol

### Sequencing rule (non-negotiable)

**Phase A is the leading domain** — whichever domain appears first in the
document (per §"Content-type detection" Rule 2.1 "starts with" rule).
Phase B is the second domain. Phase A MUST reach **two consecutive clean
passes** before Phase B begins. Phase B MUST reach **two consecutive clean
passes** before Phase INT-A begins. These are hard sequential gates — no
phase may start while its predecessor's Mode 5 loop is still running or
incomplete.

When content_type is `mixed` (by Layer 1 explicit override or by Layer 2
leading-content detection), the engine runs three domain audits in strict
sequence: Phase A (leading domain), Phase B (second domain), and
integration (Phase INT-A + INT-B as a single bounded audit):

### Phase 0 — Partition

Split the input into:

- **`workflow_partition`** — files/sections classified as workflow content.
  For a `.md` or `.yaml` file with embedded code blocks, the prose is in
  this partition; the embedded code blocks are NOT (they go to
  `code_partition`) UNLESS the code block is illustrative-only (length
  < 20 non-blank lines AND not declared as a runnable language). The
  20-line threshold matches the detection threshold so partition is
  deterministic.
- **`code_partition`** — source files and embedded code blocks ≥ 20
  non-blank lines.
- **`shared_seam`** — every cross-reference between the two partitions,
  classified per the closed `cross_ref_type` enum below: `SYMBOL_REF`
  (workflow names a code symbol), `OUTPUT_SHAPE`, `INPUT_SHAPE`,
  `SEQUENCE_STEP` (code comment names a workflow step), `ERROR_CODE`,
  `DOC_STATEMENT`. Recorded as a list of `seam_anchor` objects:

```yaml
seam_anchor:
  anchor_id:        [string]
  workflow_location: [string]   # file:section or step ID
  code_location:    [string]    # file:line or symbol
  cross_ref_type:   [enum]      # SYMBOL_REF | OUTPUT_SHAPE | INPUT_SHAPE |
                                # SEQUENCE_STEP | ERROR_CODE | DOC_STATEMENT
  cited_text:       [string]    # The verbatim text that establishes the cross-ref
```

### Phase 0 — Partition-failure protocol

Phase 0 is deterministic; any inability to partition halts the run.
Triggers (closed list):

- **PF0-1** — An input file fails to read (I/O error, permission
  denied, zero bytes after open).
- **PF0-2** — An input file's extension matches none of the closed
  workflow-extension list, the closed code-extension list, or any
  category in §Content-type detection Rule 2.1, AND Layer 4 (ambiguous
  fallback) did not produce a user-declared classification (e.g. the
  user explicitly declared the run `mixed` without resolving the
  unknown file).
- **PF0-3** — A `.md` / `.yaml` workflow-file contains a fenced code
  block whose declared language tag is **not** in the closed
  code-language list AND is **not** the empty/markdown/text tag, so
  partition cannot decide which side the block belongs to.

**Action on any PF0-N trigger:**

```yaml
on_partition_failure:
  action: "HALT immediately."
  halt_reason: "PARTITION_FAILURE"
  surface_to_user:
    - field: "decision_trace.auditor_notes"
      value: "PF0-N triggered: <file_path> — <closed reason text>"
    - field: "iteration_log[0].notes (Mode 5)"
      value: "Same as decision_trace.auditor_notes; do not run sub-audits."
  do_not:
    - "Proceed to Phase A (workflow sub-audit)."
    - "Proceed to Phase B (code sub-audit)."
    - "Guess the partition for the offending file."
    - "Silently drop the offending file."
```

The user resolves PARTITION_FAILURE by either (a) supplying the missing
file content, (b) explicitly declaring the file's partition via a
follow-up invocation that names it under `workflow|code|mixed`, or
(c) excluding the file from the input set.

### Phase A — Workflow sub-audit

Load `references/audit_workflow.yaml` and run the workflow audit on
`workflow_partition` with the user-stated mode (default Mode 5 for mixed
runs). Capture full `audit_report_W`. Sub-audit runs its own loop
independently; the engine waits for completion.

### Phase B — Code sub-audit

Load `references/audit_code.yaml` and run the code audit on `code_partition`
with the same mode. Capture full `audit_report_C`. Sub-audit runs its own
loop independently.

### Phase INT-A — Integration audit (iterative to first clean pass)

Load the integration-audit framework (§"Integration-Audit Framework", 9 layers
I1–I9). Input: `seam_anchor[]` plus `audit_report_W` and `audit_report_C`.

Run the integration audit in **Mode 5 iterative loop**. The loop exits after
the **first single clean pass** (not two consecutive — see rationale below).
Capture the full `audit_report_I_a` including the finding queue and
remediation plan at that exit point.

**Exit criterion:** One pass across all 9 integration layers with zero new
findings. (A single clean pass is sufficient here because the integration
surface is bounded by the already-completed domain audits; convergence is
faster than in an open-ended domain audit.)

### Phase INT-B — Seam-finding verification pass (non-iterative)

After Phase INT-A exits, execute **one additional non-iterative pass** over
I1–I9. Before running the pass, incorporate seam-related findings from both
domain audits:

1. Extract findings from `audit_report_W` and `audit_report_C` whose
   `location` cites a `seam_anchor` or whose `category` is `XREF_BROKEN`,
   `XREF_MISMATCH`, `SHAPE_MISMATCH`, `SEQUENCE_MISMATCH`, `DOC_DRIFT`,
   `SCOPE_MISMATCH`, or `ERROR_PATH_MISMATCH`.
2. Add those findings to the Phase INT-B context as pre-loaded evidence
   (they do NOT restart the INT-A loop; they inform this single pass only).
3. Run one pass over I1–I9 with this enriched context. Verify that every
   seam-related finding from all three audit phases (Domain 1, Domain 2,
   Integration) has been identified and has a corresponding item in the
   consolidated remediation plan.
4. Record any newly discovered findings from this pass in `audit_report_I_b`.

**This phase does not restart the loop.** It is a single bounded verification
pass. Capture `audit_report_I_b`. The final `audit_report_I` is the union
of `audit_report_I_a` and `audit_report_I_b` (deduped per Step M5-5 rules).

### Phase D — Composite assembly

Assemble the composite `audit_report`:

- `composite.workflow_audit_id = audit_report_W.audit_id`
- `composite.code_audit_id     = audit_report_C.audit_id`
- `composite.integration_audit_id = audit_report_I.audit_id`
- `composite.sub_tiers = { workflow, code, integration }`
- `composite.composite_tier = min(sub_tiers.values)` per A>B>C>D>F order
- `composite.seam_findings` = findings from `audit_report_I.finding_queue`
  whose location cites a `seam_anchor`.
- `finding_queue` = union of all three sub-reports' findings (preserve
  origin via `finding.audit_origin`).
- `decision_trace.auditor_notes` records the dispatch sequence.

### Mode 5 in mixed runs

When mode is Mode 5, EACH of the three audits runs its own Mode 5 loop
independently. Step M5-2 (Intent approval) runs three times: once for
the workflow Intent, once for the code Intent, once for the integration
Intent. The integration Intent SHOULD reference both the workflow and
code Intents; if it cannot, that is itself an integration finding
(I5-SCP-COHERENCE).

The user MAY approve all three Intents at the start in a single batch,
but each is recorded separately and is independently immutable within
its sub-audit.

---

## Integration-Audit Framework

The integration audit evaluates the seam between workflow and code in
mixed-content artifacts. It is owned by this command. It runs after both
sub-audits complete.

### Layers (9)

#### I1 — Symbol-reference integrity (I1-XREF)

*Every code symbol named in the workflow text exists in the code partition,
and every workflow step named in code comments/docs exists in the workflow
partition.*

| Check | What Fails It |
| --- | --- |
| I1.1 — Workflow → code symbol exists | A function/class/module/file name appears in workflow prose but is absent from `code_partition`. |
| I1.2 — Code → workflow step exists | A code comment or docstring references "step N" or a workflow section name that is absent from `workflow_partition`. |
| I1.3 — Symbol naming consistency | A symbol is named differently in workflow vs code (e.g. workflow says `parseInput`, code defines `parse_input` and the workflow does not document the casing convention). |
| I1.4 — Visibility match | Workflow says a function is "public-facing" but code marks it private/internal (or vice-versa). |

**Severity bias:** I1.1 / I1.2 → CRITICAL **iff** the symbol is on the
**primary execution path** (per §Deterministic vocabulary >
`primary_execution_path`); MAJOR otherwise. I1.3 / I1.4 → MAJOR by
default.

#### I2 — Output-shape match (I2-OUT-MATCH)

*The workflow's stated outputs match the code's actual returns.*

| Check | What Fails It |
| --- | --- |
| I2.1 — Output field names | Workflow declares output fields the code does not produce (or vice versa). |
| I2.2 — Output types | Workflow says "returns string[]"; code returns a single string or an object. |
| I2.3 — Output cardinality | Workflow says "returns at most 10 items"; code's loop has no upper bound. |
| I2.4 — Optional vs required | Workflow says a field is required; code returns it as nullable (or vice versa). |

**Severity bias:** I2.1 / I2.4 → CRITICAL **iff** the output is consumed
by a **downstream system** (per §Deterministic vocabulary >
`downstream_system` closed list); MAJOR otherwise. I2.2 / I2.3 → MAJOR
by default.

#### I3 — Sequence vs call-graph match (I3-SEQ-MATCH)

*The workflow's described step order is executable by code's actual control
flow.*

| Check | What Fails It |
| --- | --- |
| I3.1 — Step order = call order | Workflow says "first do X, then Y"; code's actual call graph executes Y before X (or in parallel without coordination). |
| I3.2 — Conditional branches | Workflow describes IF/ELSE; code has no equivalent branch (or has additional branches the workflow omits). |
| I3.3 — Loop semantics | Workflow says "for each X in list"; code's loop iterates differently (e.g. uses set, skips duplicates, or short-circuits). |
| I3.4 — Concurrency | Workflow says "wait for both A and B"; code awaits sequentially or runs A only. |

**Severity bias:** Any I3.x failure on the **primary execution path**
(per §Deterministic vocabulary > `primary_execution_path`) → MAJOR by
default; CRITICAL **iff** the mismatch produces a different output
**value** (not merely different timing or resource use). Off-primary-
path I3.x failures cap at MAJOR.

#### I4 — Documentation drift (I4-DOC-DRIFT)

*Prose-described behavior matches actual code behavior.*

| Check | What Fails It |
| --- | --- |
| I4.1 — Behavior description | Workflow describes a behavior (e.g. "rate-limited at 10 req/sec") that the code does not implement (or implements differently). |
| I4.2 — Side effects | Workflow says "this is read-only"; code writes to disk/DB/network. |
| I4.3 — Idempotency claim | Workflow says "safe to retry"; code's retry produces duplicate effects. |
| I4.4 — Error semantics | Workflow says "on failure, returns null"; code throws an exception (or vice versa). |

**Severity bias:** I4.2 / I4.3 → CRITICAL (correctness/safety claims).
I4.1 / I4.4 → MAJOR.

#### I5 — Scope coherence across both (I5-SCP-COHERENCE)

*Workflow's declared scope matches code's actual coverage; nothing in code
is out-of-scope per workflow.*

| Check | What Fails It |
| --- | --- |
| I5.1 — Code beyond workflow scope | Code partition contains functions/modules whose purpose falls outside the workflow's declared in-scope list. |
| I5.2 — Workflow steps without code | Workflow declares a step that has no corresponding code implementation. |
| I5.3 — Out-of-scope guards | Workflow says "out-of-scope: X"; code has X-handling logic. |
| I5.4 — Composition with other systems | Workflow assumes composition with system Y; code calls system Z (or no external system at all). |

**Severity bias:** I5.1 / I5.2 → MAJOR by default; CRITICAL **iff** the
gap covers a **primary use-case** (per §Deterministic vocabulary >
`primary_use_case`).

#### I6 — Error-path alignment (I6-ERR-ALIGN)

*Workflow's described error handling matches code's actual error paths.*

| Check | What Fails It |
| --- | --- |
| I6.1 — Error type coverage | Workflow names error types the code does not raise (or code raises types the workflow does not document). |
| I6.2 — Recovery semantics | Workflow says "on error, retry 3 times with backoff"; code retries 0 or N≠3 times, or no backoff. |
| I6.3 — Escalation path | Workflow says "on persistent error, escalate to human"; code logs-and-continues or silently swallows. |
| I6.4 — Partial-failure handling | Workflow says "on partial success, return partial results"; code returns nothing or all-or-nothing. |

**Severity bias:** I6.3 → MAJOR minimum (silent failure is dangerous).
I6.1 / I6.2 / I6.4 → MAJOR by default.

#### I7 — Contract enforcement integrity (I7-CONTRACT)

*The code actively enforces the governance contracts declared in the workflow —
it does not merely describe them or document them as assumed.*

| Check | What Fails It |
| --- | --- |
| I7.1 — Operator-decision gate | Workflow declares a step requires explicit operator approval (e.g. `operator_decision`); code has no enforcement point — it proceeds without checking for or receiving that approval. |
| I7.2 — Source consultation contract | Workflow specifies "consult Source 1 before proceeding"; code skips the consultation or treats it as optional. |
| I7.3 — Mutation guard | Workflow prohibits automatic mutation of a field or resource without a contract-defined gate; code mutates it silently. |
| I7.4 — Contract version binding | Code references a contract version that does not match the workflow's declared version, or uses no version binding at all. |

**Severity bias:** I7.1 / I7.3 → CRITICAL **iff** the unenforced contract
is on the **primary execution path** (per §Deterministic vocabulary >
`primary_execution_path`) AND its violation would produce an unrecoverable
state or governance breach; MAJOR otherwise. I7.2 / I7.4 → MAJOR by default.

#### I8 — Lifecycle and precondition chain (I8-LIFECYCLE)

*The code honors the workflow's implied "must-be-true-before-this-step"
requirements and handles unmet preconditions gracefully rather than
silently proceeding.*

| Check | What Fails It |
| --- | --- |
| I8.1 — Precondition check presence | Workflow implies a prerequisite state (e.g. "schema must be validated before field removal"); code performs the dependent action without verifying the prerequisite. |
| I8.2 — Unmet precondition handling | When a precondition is unmet, workflow specifies a halt or escalation; code continues execution as if the precondition were satisfied. |
| I8.3 — Lifecycle state ordering | Workflow defines a lifecycle sequence (draft → validated → active); code allows transitions that skip or reverse lifecycle states. |
| I8.4 — Dependency resolution order | Workflow requires step A to complete before step B; code executes B independently of A's completion status. |

**Severity bias:** I8.1 / I8.2 → CRITICAL **iff** the skipped precondition
gates a data-integrity or security boundary; MAJOR otherwise. I8.3 / I8.4
→ MAJOR by default.

#### I9 — Observable behavior alignment / evidence fidelity (I9-OBSERVABLE)

*The code produces observable, verifiable outputs that match the workflow's
stated evidence and provenance requirements — not empty placeholders.*

| Check | What Fails It |
| --- | --- |
| I9.1 — Decision trace population | Workflow states "record decision trace"; code writes an empty, stub, or null decision trace field. |
| I9.2 — Evidence citation content | Workflow requires evidence citations with actual source content; code records citation keys or IDs only, with no retrievable content. |
| I9.3 — Audit trail completeness | Workflow implies a complete audit trail for each mutation; code logs only final state, omitting intermediate decisions or the identity of the deciding agent. |
| I9.4 — Verifiability of outputs | Workflow states an output is "verifiable by an external observer"; code produces outputs that require internal state access to interpret. |

**Severity bias:** I9.1 / I9.2 → MAJOR by default (evidence gaps erode
trust but rarely crash the system). I9.3 → MAJOR. I9.4 → ADVISORY unless
the artifact's stated intent explicitly names external auditability as a
**primary use-case** (per §Deterministic vocabulary > `primary_use_case`),
in which case → MAJOR.

### Integration-audit scoring

Each layer scores 0–100 like the domain layers. Layer weights:

```yaml
integration_layer_weights:
  I1-XREF:           0.20     # Highest — broken refs are runtime failures
  I2-OUT-MATCH:      0.15
  I3-SEQ-MATCH:      0.12
  I4-DOC-DRIFT:      0.10
  I5-SCP-COHERENCE:  0.10
  I6-ERR-ALIGN:      0.08
  I7-CONTRACT:       0.12     # Contract enforcement — governance-critical
  I8-LIFECYCLE:      0.08
  I9-OBSERVABLE:     0.05     # Advisory-heavy layer; lowest weight
                     -----
                     1.00
```

### Integration-specific tier overrides

```yaml
integration_overrides:
  - condition: "Any I1 (Symbol-reference) check FAILs on a primary-path symbol"
    cap: "C"
    reason: "A broken cross-reference on the primary path means the system will not execute as documented."

  - condition: "Any I3 (Sequence) FAIL produces wrong outputs (not merely different timing)"
    cap: "D"
    reason: "Order-dependent correctness violations produce wrong results."

  - condition: "Any I7 (Contract enforcement) check FAILs as CRITICAL on the primary execution path"
    cap: "C"
    reason: "An unenforced governance contract on the primary path is a hard governance breach; the artifact cannot be deployed without operator sign-off."

  - condition: "Any I8 (Lifecycle) check FAILs as CRITICAL (precondition gates a data-integrity boundary)"
    cap: "C"
    reason: "Skipping a data-integrity precondition produces corrupt state that cannot be recovered by re-running."
```

### Integration `category` enum extensions

In addition to the universal `finding.category` values, integration findings
MAY use:

- `XREF_BROKEN` — symbol named in one partition is absent from the other.
- `XREF_MISMATCH` — symbol exists but differs in name/casing/visibility.
- `SHAPE_MISMATCH` — output/input shape disagreement.
- `SEQUENCE_MISMATCH` — order or branching disagreement.
- `DOC_DRIFT` — prose-described behavior diverges from code behavior.
- `SCOPE_MISMATCH` — coverage gap or overrun between partitions.
- `ERROR_PATH_MISMATCH` — error semantics disagreement.
- `CONTRACT_ENFORCEMENT` — code fails to enforce a governance contract declared in the workflow (I7).
- `LIFECYCLE_VIOLATION` — code skips or violates a workflow-implied lifecycle state or precondition (I8).
- `EVIDENCE_GAP` — code produces empty, stub, or unverifiable evidence/provenance outputs where the workflow requires populated, verifiable content (I9).

---

## Iterative Audit Procedure (Mode 5)

Mode 5 wraps the per-domain layer framework in the 10-step loop below.
**STEP 0** (artifact load, format/language detection, Intent extraction,
viability gate) **still runs first**, owned by the domain command. The
loop begins after STEP 0 completes.

**Determinism rule:** During every granular pass, traverse the artifact
under audit in **document order, depth-first**. Same input → same
traversal → same finding order across runs. This is non-negotiable; it
makes Mode 5 reproducible.

### Step M5-1 — High-level review

Read the entire artifact at speed. Capture purpose, scope, tone, structure,
declared mode (if any). No per-element depth yet.

This step uses STEP 0's viability gate; it does not replace it.

The user MAY at this step state a `pass_budget` override (integer 4..30).
Outside that range or non-integer → reject and use default 10. Record in
`audit_report.iteration.pass_budget`.

### Step M5-2 — Summarize Artifact Intent → user approval gate

Author a concise statement of the artifact's overall intent (≤ 3 sentences,
not granular). It MUST encapsulate purpose without prescribing implementation.

Write the summary into `audit_report.stated_intent`. Mode 5 OVERWRITES the
bare STEP-0 intent with this richer, user-approved summary.

Present to the user:

- **2.1 Not approved**
  - 2.1.1 Solicit feedback. Refine the summary. Re-present.
  - **Hard cap: 3 refinement rounds.** If still not approved on the third
    round → HALT (`halt_reason: INTENT_NOT_APPROVED`). Notify the user
    with the three candidate summaries and stop.

- **2.2 Approved**
  - 2.2.1 The approved Intent becomes the **anti-drift anchor** for the
    rest of the run. It is immutable within the run (Anti-Drift §8). It
    is restated at the top of every granular pass (Step M5-3) and at
    every plan-review checkpoint (Step M5-9).
  - 2.2.2 Begin (or continue) the iterative loop at Step M5-3.

In **mixed-content** runs, this step runs three times in sequence (once
per sub-audit: workflow Intent, code Intent, integration Intent). The
user MAY batch-approve all three at start, but each is recorded
separately and is independently immutable within its sub-audit.

### Step M5-3 — Granular per-element review (Pass N)

1. Initialize `pass_number = 1` on first entry; otherwise increment.
2. **Restate the approved Intent** at the top of the pass (record in
   `iteration_log[N].notes`).
3. Walk the artifact under audit **element-by-element in document order,
   depth-first**.
4. For each element, run **all the domain's layers** per the per-check
   protocol (PASS / FAIL / PARTIAL / SKIPPED). The **element boundary**
   is domain-defined:
   - For **workflow** audits: see `references/audit_workflow.yaml` —
     numbered/lettered list item, heading section, fenced code block,
     prose paragraph (in that priority).
   - For **code** audits: see `references/audit_code.yaml` —
     function/method, class, module, file (in that priority).
   - For **integration** audits: each `seam_anchor` is one element.
5. Findings use the `finding` schema and SET `pass_number = N`.
   `finding.location` MUST cite the element-boundary level used.

### Step M5-4 — Classify findings (MISSING / INCORRECT / AMBIGUOUS / OUT_OF_SCOPE)

In addition to the standard `category` enum, Mode 5 emphasizes a four-way
classification when summarizing per-pass results:

- **MISSING** — required element absent for Intent.
- **INCORRECT** — element present but wrong; maps to category enum
  values: `UNHANDLED`, `CONTRADICTION`, `BROKEN_REF`, `UNREACHABLE`,
  `STALE_REF`, `UNVERIFIABLE`, `STRUCTURAL`, `REDUNDANCY`, `ASSUMPTION`,
  `XREF_BROKEN`, `XREF_MISMATCH`, `SHAPE_MISMATCH`, `SEQUENCE_MISMATCH`,
  `DOC_DRIFT`, `SCOPE_MISMATCH`, `ERROR_PATH_MISMATCH`.
- **AMBIGUOUS** — element unclear or non-deterministic; maps to `AMBIGUITY`.
- **OUT_OF_SCOPE** — element exceeds Intent; maps to `SCOPE_LEAK` or
  `SCOPE_MISMATCH`.

Each finding still records the standard `category` plus this surface
label in `finding.description` for the per-pass summary.

### Step M5-5 — Compile and deduplicate

1. Aggregate findings discovered in this pass.
2. Deduplicate against findings already on file from prior passes. Two
   findings are duplicates **iff ALL THREE** of these fields are
   identical (string-exact comparison):
   - `finding.check_id`
   - `finding.category`
   - `finding.location`

   `evidence` similarity is **not** a dedup criterion. Two findings with
   the same `check_id` + `category` + `location` but different `evidence`
   are treated as **the same finding with additional evidence** (apply
   rule 3, below). Two findings with different `check_id` or `category`
   or `location` are **never deduped**, even if their text reads
   similarly.
3. When a new finding is detected as a duplicate (per rule 2), do NOT
   create a new finding record. Instead, append the new finding's
   `evidence` text to the existing finding's `evidence` field as a new
   line, prefixed with `[pass N]:` followed by a single space (where N
   is the current `pass_number`). Do not modify any other field.
4. Update `iteration_log[N].new_findings_count` to count only findings
   that were NOT dedup-matched in this pass.

### Step M5-6 — Pass complete: branch on findings

- **6.1 Findings exist this pass**
  - 6.1.1 Restate the approved Intent.
  - 6.1.2 → return to Step M5-3 for Pass N+1.
- **6.2 Zero findings this pass AND prior pass had findings (first clean pass)**
  - 6.2.1 Note in `iteration_log`: "First clean pass at N=…"
  - 6.2.2 → return to Step M5-3 for Pass N+1 (confirmation pass).
- **6.3 Zero findings this pass AND prior pass also clean (second consecutive clean pass)**
  - 6.3.1 Loop exits. Continue to Step M5-7.

#### Intent-drift halt (any time during M5-3 → M5-6)

HALT the loop with `halt_reason: INTENT_DRIFT` and notify the user **iff
any one** of these three explicit triggers fires in a single pass:

1. **OUT_OF_SCOPE saturation** — the pass produces ≥ **3** findings whose
   four-way classification (Step M5-4) is `OUT_OF_SCOPE`. (Threshold
   fixed at 3: 1 or 2 OUT_OF_SCOPE findings = isolated outliers; ≥ 3
   = systemic intent-vs-artifact mismatch.)
2. **Intent vs declared scope contradiction** — at least one finding in
   this pass reports a `CONTRADICTION` (or `SCOPE_MISMATCH`) between the
   approved Intent statement and the artifact's own declared scope.
   Source contradiction must be cited verbatim in the finding's
   `evidence`.
3. **MISSING-element density** — the pass produces ≥ **5** findings
   classified `MISSING` (Step M5-4) that all cite the same Intent clause
   as the gap. (Same Intent clause = identical substring of the approved
   Intent in the finding's `description` or `remediation` field.)

Trigger evaluation is per-pass (not cumulative across passes). Do NOT
silently revise the Intent — that is forbidden by Anti-Drift §8. The
user must decide whether to restart Mode 5 with a corrected Intent.

#### Mode 5 state externalization

To keep concurrent in-memory state low, Mode 5 externalizes loop state
to a **bootstrap scratchpad** (a dedicated section in `context-bootstrap`).
The scratchpad is the source of truth for cross-pass state; the in-memory
copy is a working buffer.

**Scratchpad contract.** At Step M5-2 approval, allocate a scratchpad
section (record its ID in `audit_report.iteration.bootstrap_scratchpad_id`).
The scratchpad MUST contain exactly these top-level keys, written as a
YAML block:

- `intent_anchor` — the approved Intent string.
- `intent_clauses` — atomic clauses (computed at first M5-9 entry).
- `pass_number` — current pass counter.
- `findings` — cumulative findings list (full schema).
- `plan_items` — current `remediation_plan.items[]` (filled at M5-8).
- `iteration_log` — per-pass entries.
- `halt_flag` — null while running; set to a `halt_reason` enum on halt.

**Read/write rule.** At the start of every pass (Step M5-3 item 1), read
the scratchpad and load `pass_number`, `findings`, and `intent_anchor`
into working memory. At the end of every pass (after Step M5-5), write
back the updated `findings`, `iteration_log`, and `pass_number`. At
Step M5-8, write `plan_items`. At Step M5-9, write `intent_clauses` and
`clause_coverage`. At Step M5-10, write `halt_flag` if applicable.

**Effect on cognitive load (closed state-slot list).** Cognitive load
in this command family is measured by counting concurrent state slots
the agent must track. The list is closed; nothing else counts as state.

```yaml
cognitive_load_state_slots:
  # Mode 5 (default scope): exactly 5 slots — PASS.
  S1_pass_number:                "integer"
  S2_intent_anchor:              "string"
  S3_current_pass_findings_buffer: "list"
  S4_scratchpad_id:              "string"
  S5_halt_evaluation_state:      "enum: NORMAL | PENDING_HALT | HALTED"

  # Subagent two-stage scope only (code-audit Stage 1 ↔ Stage 2):
  # adds 4 more slots — total 9 — PARTIAL.
  S6_stage:                      "enum (subagent_two_stage scope only)"
  S7_iteration_counter:          "integer (subagent_two_stage scope only)"
  S8_spec_anchor:                "string (subagent_two_stage scope only)"
  S9_work_product_paths:         "list (subagent_two_stage scope only)"

design_targets:
  normal_mode_5:           "5 slots → cognitive-load check PASSes"
  subagent_two_stage:      "9 slots → cognitive-load check is PARTIAL"
  external_tools_excluded: >
    Tokenizers, file-readers, regex engines, and similar deterministic
    utilities SHALL NOT be counted as state. They are stateless from
    the agent's perspective.
```

Children that include a Layer 7 cognitive-load check cite this list
verbatim and do not redefine slots locally.

**Granular-pass-failure interaction.** If a granular pass fails before
write-back, the scratchpad still reflects the prior pass's state; the
auditor restarts from there on Pass N+1.

#### Granular-pass-failure protocol

If a per-element pass cannot complete (file segment unreadable, mid-pass
error, unrecoverable layer failure on every element):

- Set `iteration_log[N].pass_status = INCOMPLETE`.
- Do NOT count the pass toward the clean-pass quota.
- Notify the user.
- Proceed to Pass N+1 (do not silently retry the same pass).
- If two consecutive INCOMPLETE passes → HALT
  (`halt_reason: GRANULAR_PASS_FAILURE`).

#### User-timeout protocol

User prompts at Step M5-2 (Intent approval) and Step M5-10 (plan
approval) have a fixed response window of **30 minutes** (configurable
per session if the user states a different limit at start). On window
expiry:

- Save `audit_report` and `remediation_plan` (current state) to the
  session bootstrap.
- HALT (`halt_reason: USER_TIMEOUT`).
- Note in `iteration_log` which prompt timed out (M5-2 vs M5-10) and
  the pass number at the time.

The user may resume in a new session; a resumed run treats the saved
state as authoritative and re-presents the same prompt.

#### Dedup-failure protocol

If Step M5-5 deduplication cannot complete (e.g. malformed `finding`
records prevent the string-exact triple-key comparison, or a finding
lacks one of the three required fields `check_id` / `category` /
`location`):

- Mark the offending finding(s) with `finding.dedup_status = "MALFORMED"`
  (a transient status; not stored in the final report).
- Skip dedup for those specific findings; ALL other findings dedup
  normally per Step M5-5 rule 2.
- If ≥ 1 malformed finding remains after the pass → HALT
  (`halt_reason: DEDUP_FAILURE`).
- If all malformed findings can be repaired by the auditor before the
  next pass (e.g. by filling in a missing `category` from `check_id`),
  the pass continues normally.

#### Iteration-budget protocol

To prevent runaway loops, Mode 5 caps total passes at a fixed budget.

- **Default budget: `pass_budget = 10`.** The user MAY override at Step
  M5-1 by stating an integer between 4 and 30 inclusive. Outside that
  range or non-integer → reject and use 10.
- The budget includes ALL passes — passes that surface findings AND
  clean passes. (Two clean passes still count toward the budget.)
- **Trigger:** at the END of any pass (after Step M5-5 write-back), if
  `pass_count >= pass_budget` AND `clean_passes < 2` → HALT
  (`halt_reason: ITERATION_BUDGET_EXHAUSTED`).
- **On halt:** still consolidate findings discovered through
  `pass_count`, still build the remediation plan at Step M5-8, still
  run plan ↔ Intent review at Step M5-9. The user receives a partial-
  but-actionable report with `halt_reason` set.
- **Rationale:** an artifact that cannot reach two clean passes within
  10 iterations is structurally unstable; further passes are unlikely
  to converge.
- **No retries.** The auditor MUST NOT increase the budget mid-run.

### Step M5-7 — Final consolidated findings summary

- Emit the consolidated set of all findings discovered across all passes,
  deduped, with `pass_number` retained on each.
- Each finding retains the FULL schema. No compression. No softening.
- Severity, routing, evidence, impact, and remediation fields are
  preserved verbatim.

### Step M5-8 — Build remediation plan (proposal-only)

For every consolidated finding, emit a concrete plan item:

- `action`: ADD | REMOVE | UPDATE | REPLACE | SPLIT | MERGE
- `target`: section / step / line range / file:line in artifact
- `change`: concrete change text (proposal — not applied). **Hard limit:
  ≤ 60 words. MUST describe the action and the target only.** It MAY
  include a short example phrase ≤ 10 words inside quotes when needed
  for clarity. It MUST NOT contain a full re-authored section, full
  replacement source body, or complete prose paragraphs intended for
  verbatim insertion. If a finding requires long-form rewriting, set
  `routing = PROMPT_BUILDER`, write a short directive in `change`, and
  add the item to `prompt_builder_substeps` with rationale; the executor
  session authors the long-form text.
- `severity`: inherited from the highest-severity finding the item resolves
- `routing`: inherited from the finding(s)
- `depends_on`: other plan_ids that must land first
- `locked`: bool, defaults to `false` at plan creation (see Step M5-10
  PARTIAL branch).

Ordering: **severity-first (CRITICAL → ADVISORY), then layer order, then
dependency topological order**.

Items with `routing == PROMPT_BUILDER` are also listed under
`remediation_plan.prompt_builder_substeps` with rationale. Mode 5 does
NOT invoke `deterministic-prompt-builder`; the executor session does
(this is a separate, narrower constraint from the no-execute rule).

The plan is **proposal-only** (see §Anti-Drift §7 for the canonical
no-execute rule).

### Step M5-8.5 — Solution Determinism Gate (per plan item)

After Step M5-8 has authored a candidate plan item but BEFORE the item is
added to `remediation_plan.items[]`, run the gate from §"Solution
Determinism Gate" against that item's `change` field.

**Procedure (per item, deterministic):**

1. Construct a `determinism_certification` block per the closed-shape
   schema in §"Solution Determinism Gate".
2. Evaluate the 5-rule pass rubric. Set `verdict` accordingly.
3. **Branch on verdict:**
   - `verdict == PASS` → attach the certification to the plan item; the
     item is eligible for inclusion in `remediation_plan.items[]`.
     Continue to the next plan item, or to Step M5-9 if all items are
     certified.
   - `verdict == FAIL` → DO NOT add the item to the plan. Set
     `failure_reason` per the rubric. Increment the item's
     `gate_attempts` counter. Re-derive the `change` text using the
     failure reason as guidance and return to Step M5-8.5 sub-step 1
     for this same item.
4. **Retry budget enforcement:** the per-item budget is **2 retries**
   (initial attempt + 2 retries = 3 total certifications maximum). On
   the third consecutive `verdict: FAIL` for the same plan item → HALT
   the loop with `halt_reason: DETERMINISM_GATE_EXHAUSTED`. Surface to
   the user (per §"Solution Determinism Gate" > retry_protocol >
   on_third_fail):
   - the verbatim `change` text of each of the three attempts,
   - each attempt's `failure_reason`,
   - the verbatim finding(s) that the plan item was meant to address.

**Forbidden:**

- Softening any rubric rule to coerce a PASS.
- Presenting an uncertified or `verdict: FAIL` plan item to the user at
  Step M5-10.
- Silently dropping a finding because its remediation cannot pass the
  gate. (Halt instead — the user decides resolution.)

**State externalization:** The certification block and `gate_attempts`
counter for each plan item are written to the Mode 5 scratchpad under
`plan_items` (see §"Mode 5 state externalization" — these are part of
the existing `plan_items` slot, not a new top-level key).

**Mode 1–4 application.** In non-iterative modes, the equivalent gate
runs per-finding immediately after `finding.remediation` is authored,
before the finding enters `audit_report.finding_queue`. The retry budget
and halt protocol are identical. Findings with a `verdict: PASS`
certification proceed normally; findings whose remediation cannot pass
within the budget HALT with `halt_reason: DETERMINISM_GATE_EXHAUSTED`.

### Step M5-9 — Plan ↔ Intent review

Verify plan-Intent satisfaction by **atomic-clause coverage**, NOT by
free judgment.

**Procedure:**

1. **Decompose the approved Intent** (`intent_anchor`) into atomic
   clauses. Each clause is one independent declarative claim. Split
   rules:
   - Sentence boundaries (`.`, `?`, `!`) are clause boundaries.
   - Within a sentence, a coordinating conjunction (`and`, `or`, `;`)
     that joins two complete claims (each with its own subject + verb)
     is a clause boundary; the conjunction is dropped.
   - Subordinate clauses introduced by `because`, `so that`, `in order
     to`, `while`, `unless` stay with their parent clause (not split).
   - The total clause count MUST be ≥ 1 and SHOULD be ≤ 5; > 5
     indicates the Intent is too granular and should have been refined
     at Step M5-2.
   - Record the resulting list in `plan_review.intent_clauses`.

2. **Map each clause to coverage** (deterministic noun-phrase rule).
   For every clause C, set `plan_review.clause_coverage[C]` to the
   union of:
   - `plan_item_ids`: list of `remediation_plan.items[].plan_id` whose
     `change` text covers C per the rule below, AND
   - `existing_step_locations`: list of `finding.location`-style
     citations pointing to elements in the artifact under audit that
     already satisfy C without modification (same rule applied to the
     element's body text).

   **Coverage rule.** Plan item P covers clause C **iff** at least one
   of the following two predicates evaluates true:

   - **(P1) Capitalized noun-phrase overlap.** The set of capitalized
     noun phrases in `P.change` shares ≥ 1 element with the set of
     capitalized noun phrases in C. A capitalized noun phrase is a
     contiguous sequence of one or more tokens whose first character
     is `[A-Z]` (Unicode letter); proper-noun acronyms (≥ 2 letters,
     all uppercase) qualify.
   - **(P2) Lowercased non-stop-word noun overlap.** The set of
     lowercased nouns in `P.change` shares ≥ 1 element with the set of
     lowercased nouns in C. A "noun" for this rule is any word
     (`[A-Za-z][A-Za-z0-9_-]*`) of length ≥ 3 that is **not** in the
     closed English stop-word list:

     ```
     a, an, and, are, as, at, be, by, for, from, has, have,
     in, is, it, of, on, or, that, the, this, to, was, were,
     will, with
     ```

   Comparison is case-insensitive on both sides for (P2) and
   case-sensitive for (P1). Tokenization splits on `\s+` and punctuation
   (`[.,;:!?()\[\]{}"']`). Both predicates compute deterministically;
   no natural-language reasoning is permitted.

3. **Compute satisfaction**:
   - `satisfies_intent = true` IFF every clause C has
     `len(plan_item_ids) + len(existing_step_locations) ≥ 1`.
   - `gaps_if_unsatisfied` = the list of clauses C for which both lists
     are empty (verbatim clause text).

4. **Branch**:
   - `satisfies_intent == true` → continue to M5-10.
   - `satisfies_intent == false` → **back-edge to Step M5-8** (revise
     plan to add items covering each gap clause); increment
     `plan_review.revision_rounds`.
   - **Hard cap: 3 revision rounds.** If still unsatisfied on the third
     round → HALT (`halt_reason: PLAN_REVISION_EXHAUSTED`). Deliver the
     partial plan plus the verbatim gap clauses to the user.

This procedure is fully deterministic.

### Step M5-10 — Present plan to user

Deliver the merged artifact: `audit_report` + `iteration` +
`remediation_plan` (plus `composite` block for mixed-content runs).

User options:

- **Approve** → set `user_approval.status = APPROVED`. Mode 5 ends. Hand
  off to the executor session via `context-bootstrap`. Record bootstrap
  entry.
- **Reject** → set `user_approval.status = REJECTED`. Capture rationale
  in `user_approval.rationale`. **Return to Step M5-3** for a fresh
  pass with the rejection rationale carried into `iteration_log`.
- **Partial** → set `user_approval.status = PARTIAL`. Capture rationale
  in `user_approval.rationale`. The user MUST identify each accepted
  plan item by `plan_id`; for every accepted item, set
  `remediation_plan.items[<plan_id>].locked = true`. All other items
  remain `locked = false`. Then return to Step M5-3 with the following
  constraint: any finding whose `finding_id` appears in
  `items[<plan_id>].finding_ids` for a `locked = true` item is
  **excluded** from subsequent passes (it is considered resolved). The
  two-clean-pass exit rule applies to the remaining (non-locked)
  finding surface.

If the user halts the run at any prompt → set
`halt_reason: USER_HALT` and exit cleanly.

### Mode 5 — Halt summary

| Halt reason | Trigger |
| --- | --- |
| `INTENT_NOT_APPROVED` | 3 refinement rounds at Step M5-2 without approval. |
| `INTENT_DRIFT` | Any of the three explicit triggers in §Intent-drift halt fires in a single pass. |
| `GRANULAR_PASS_FAILURE` | Two consecutive INCOMPLETE granular passes. |
| `PLAN_REVISION_EXHAUSTED` | 3 revision rounds at Step M5-9 without satisfaction. |
| `USER_HALT` | User halts at any prompt. |
| `USER_TIMEOUT` | User does not respond at M5-2 or M5-10 within the response window (default 30 min). |
| `DEDUP_FAILURE` | ≥ 1 malformed finding prevents Step M5-5 dedup from completing. |
| `ITERATION_BUDGET_EXHAUSTED` | `pass_count >= pass_budget` (default 10) reached without two consecutive clean passes. |
| `PRE_FLIGHT_FAILURE` | Any §Pre-flight verification check (PF-1…PF-6) fails before audit begins. |
| `PARTITION_FAILURE` | Phase 0 cannot read or classify an input file after Layer 4 fallback (mixed-content runs). |
| `DETERMINISM_GATE_EXHAUSTED` | A plan item (Mode 5) or finding remediation (Modes 1–4) failed §"Solution Determinism Gate" rubric on 3 consecutive authoring attempts (initial + 2 retries). |

---

## Companion Commands

- **`references/audit_workflow.yaml`** — Embedded workflow-domain auditor.
  Owns workflow layers, checks, format detection, and workflow-specific tier
  overrides. Loaded by `@audit-engine` for workflow and mixed-content runs.
  Canonical path: `C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_workflow.yaml`.
- **`references/audit_code.yaml`** — Embedded code-domain auditor. Owns code
  layers, checks, language/repo detection, code-specific tier overrides, AND
  the subagent two-stage gate methodology. Loaded by `@audit-engine` for code
  and mixed-content runs.
  Canonical path: `C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_code.yaml`.
- **`deterministic-prompt-builder`** (skill) — Construction skill for YAML
  prompts. Plan items with `routing == PROMPT_BUILDER` are listed under
  `remediation_plan.prompt_builder_substeps` with rationale. The executor
  session invokes this skill, NOT the auditor.
  Canonical path: `C:\Users\rtoth\.cursor\skills-cursor\prompt-builder\SKILL.md`.
- **`context-bootstrap`** (command) — Session continuity. Mode 5 always
  crosses sessions (audit here, executor next), so a bootstrap entry is
  required at handoff. The Mode 5 scratchpad lives in `context-bootstrap`.
  Canonical path: `C:\Users\rtoth\.cursor\commands\bootstrap`.

---

## Procedure Summary

```
INVOCATION:    @audit-engine [<content_type>] [<mode>]

PHASE 0: Detection / dispatch
  → Layer 1: Explicit-override fast-path
            → If content_type provided, skip detection entirely.
  → Layer 2: Leading-content detection (deterministic, no user prompt)
            → Read document. Classify from first substantive content block.
            → Record detection_path and detection_classification.
  → Mode is always ITERATIVE. Never prompt, never negotiate.

PHASE A: Single-domain — workflow
  → If content_type == workflow: load references/audit_workflow.yaml; run audit.
  → Capture audit_report_W.

PHASE B: Single-domain — code
  → If content_type == code: load references/audit_code.yaml; run audit.
  → Capture audit_report_C.

PHASE M: Mixed-content
  → Partition input → leading_domain_partition, second_domain_partition, shared_seam.
  → Phase A: leading domain (determined by document start order).
            Must reach two consecutive clean passes before Phase B begins.
  → Phase B: second domain.
            Must reach two consecutive clean passes before Phase INT-A begins.
  → Phase INT-A: 9-layer integration audit on shared_seam; iterative loop
                 exits on first single clean pass.
  → Phase INT-B: single non-iterative seam-verification pass incorporating
                 seam-related findings from Phase A and Phase B.
  → Phase D: assemble composite audit_report (composite_tier = min).

PHASE OUTPUT: Deliver report
  → Mode 1–4: audit_report (single or composite).
  → Mode 5: audit_report + iteration + remediation_plan
            (and composite for mixed runs).
  → Always: routing queues filled.

PHASE HANDOFF (Mode 5 only):
  → User APPROVE → bootstrap entry; END.
  → User REJECT  → return to Step M5-3.
  → User PARTIAL → lock accepted items; return to Step M5-3.
```
