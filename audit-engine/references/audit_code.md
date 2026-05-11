---
name: code-audit
description: >-
  Single-domain code auditor. Runs an 8-layer code audit framework
  (Correctness, Security, Performance, Maintainability, Testability, API
  Design, Concurrency, Structural Quality) over source files, modules,
  packages, PR diffs, or whole repos. Also hosts the subagent two-stage
  gate methodology for subagent-driven development. Imports the engine for
  mode taxonomy, Mode 5 iterative loop, halt protocols, output contract,
  and anti-drift safeguards. Invoke as
  `@code-audit [<scope_type>] [<mode>]`. Audits only — never modifies code.
  The deliverable is an audit report plus a proposal-only remediation plan;
  execution is handed off to a separate session.
---

# Code-Audit

## What this command is

`@code-audit` is the **code-domain auditor**. It owns:

- The 8 code audit layers (L1-COR through L8-STR).
- The 50+ code-specific check IDs and their fail conditions.
- The scope-type enum (FILE, FILE_SET, MODULE, PACKAGE, PR_DIFF,
  COMMIT_RANGE, REPO).
- The language enum (LANG_PY, LANG_JS, LANG_TS, LANG_RS, LANG_GO,
  LANG_JAVA, LANG_KT, LANG_RB, LANG_CS, LANG_CPP, LANG_C, LANG_SWIFT,
  LANG_SCALA, LANG_EX, LANG_CLJ, LANG_LUA, LANG_SH, LANG_PS1, MIXED).
- Code-specific tier overrides (security, correctness, test coverage).
- Code-specific edge cases (vendored code, generated code, binary
  files, deleted-file diffs, oversized files… see §"Code-Specific Edge
  Cases" for the full closed list).
- **The subagent two-stage gate methodology** for subagent-driven
  development workflows.

`@code-audit` does NOT own:

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
producing any audit report. This module is loaded at PF-3 pre-flight.

## Existing skill is unaffected

This command does NOT alter the existing `code-review---iterative` skill.
That skill remains the home for **non-audit review lanes** (requesting
review, receiving review, PR babysit). The audit-flavored content from
that skill — specifically the iterative full-tree review lane and the
subagent two-stage gates lane — is captured here in `@code-audit` (the
8-layer framework + Mode 5 implements the iterative full-tree review;
the subagent two-stage gate section below implements the two-stage
gates).

## Distinction from `code-review---iterative`

| Lane | Owned by `@code-audit` (this) | Owned by `code-review---iterative` (skill) |
| --- | --- | --- |
| Iterative full-tree review (zero-findings) | Yes — implemented as Mode 5 over 8 layers | Lane A in the existing skill (kept for natural-language users; logically equivalent to `@code-audit iterative`) |
| Subagent two-stage gates per task | Yes — see § "Subagent two-stage gate methodology" below | Lane D in the existing skill (kept for natural-language users; pointers across both should stay consistent) |
| Requesting code review (dispatch) | No | Lane B |
| Receiving review feedback | No | Lane C |
| PR merge-ready babysit | No | Lane E |

`@code-audit` answers **"how good is this code structurally?"** with a
scored, layered report. `code-review---iterative` continues to answer
**"how do I run review across this work?"** with lane-specific procedures
for non-audit lanes.

## Invocation

```
@code-audit [<scope_type>] [<mode>]
```

- `<scope_type>` (optional) ∈ `{file, file_set, module, package, pr_diff, commit_range, repo, subagent_two_stage}`.
  If omitted, the command infers from input: a single source file →
  `file`; a folder → `package`; two SHAs given → `commit_range`; a PR
  number/URL → `pr_diff`; a per-task implementer-subagent context →
  `subagent_two_stage`. Ambiguous → asks user.
- `<mode>` (optional) ∈ `{full, targeted, post_mortem, diff, iterative}`.
  **Iterative is the unconditional default** (inherited from `@audit-engine`).
  `iterative` wraps `full`, `post_mortem`, or `diff` via the engine's
  Mode 5 loop.

Examples:

- `@code-audit` — auto-infer scope; iterative (Mode 5) audit; default mode.
- `@code-audit pr_diff iterative` — explicit iterative override on a PR diff.
- `@code-audit repo full` — full (single-pass) audit over an entire repository.
- `@code-audit module diff` — Mode 5 diff between two versions of a module.
- `@code-audit subagent_two_stage` — invoke the per-task two-stage gate
  methodology (see §"Subagent two-stage gate methodology").

This module is loaded by `@audit-engine` as a sub-step of code and
mixed-content runs. Its canonical path is
`C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_code.yaml` (supersedes this file).

---

## Mission

Systematically evaluate source code for correctness, safety, performance,
maintainability, testability, API soundness, concurrency safety, and
structural quality — surfacing every failure mode BEFORE it reaches
production. Additionally, host the per-task two-stage review gate
methodology used by subagent-driven development.

**This command audits code. It does not write or modify code.**

Findings that require code changes route to user action or to a separate
implementation session. Outputs are audit reports and finding queues —
not patches.

---

## Authority Model

**Canonical:**

- The source code under audit (read-only access required).
- For PR / diff scope: the base and head SHAs.
- For subagent two-stage scope: the implementer subagent's task spec
  AND the work product (code) it produced.
- The user's stated intent for the code (what is it supposed to do?).
- The repository's existing test suite (used as evidence for L5-TST).

**Derived:**

- Audit report, layer scores, tier rating, finding classifications,
  routing queues, remediation plan items.

**Rule:** never modify code under audit. Never run code. Never apply a
proposed fix. Static analysis only — augmented by reading existing test
output if provided.

---

## Scope / Non-Scope

**In scope:** running the 8-layer code audit framework. Scoring each
layer. Producing a tier rating. Identifying CRITICAL security and
correctness findings. Routing recommended changes (refactor / test-add /
hardening) to a follow-up session. Per-task subagent two-stage review
gating.

**Never:** rewrite code. Apply fixes. Add tests. Run code (no
execution-based assessment unless test output is supplied as input).
Replace human security review for high-risk changes (escalate instead).
Operate without a defined scope. Dispatch implementer subagents
(that's the caller's job).

---

## STEP 0 — Pre-Audit Setup

> **Pre-flight is engine-owned.** Before STEP 0 runs, the engine's
> §"Pre-flight verification" (PF-1…PF-6) MUST already have passed.
> STEP 0 does NOT duplicate pre-flight; it begins after the engine
> confirms all canonical files, required skills, and the artifact
> under audit are loaded. Any pre-flight failure halts with
> `halt_reason: PRE_FLIGHT_FAILURE` (see `@audit-engine`).

Before any audit work begins:

```
1. Confirm scope is loaded and readable.
   - If no source provided → HALT. Request source.
   - For pr_diff / commit_range: confirm both SHAs exist and are reachable.
   - For repo / package: confirm root path exists and is readable.
   - For subagent_two_stage: confirm BOTH the task spec AND the
     implementer's work product are loaded.

2. Generate audit_id using format CDA-YYYYMMDD-HHMMSS from current timestamp.

3. Identify language(s):
   - Single-language scope → record one language enum value.
   - Multi-language scope → record list; some checks become per-language.
   - Unknown extension → ASK. Do not guess language.

4. Identify scope_type and record:
   - file: single source file
   - file_set: enumerated list of files
   - module: a folder treated as a single import unit
   - package: a folder with build/install metadata, recognized by the
     presence of one or more of the closed manifest list:
     `package.json`, `Cargo.toml`, `pyproject.toml`, `setup.py`,
     `pom.xml`, `build.gradle`, `build.gradle.kts`, `Gemfile`,
     `go.mod`, `mix.exs`, `composer.json`, `pubspec.yaml`,
     `*.csproj`, `*.fsproj`. Any other root manifest file: ASK.
   - pr_diff: a set of changes between two SHAs of the same repo, with
     PR number/URL recorded
   - commit_range: a base..head SHA range
   - repo: an entire repository
   - subagent_two_stage: a per-task subagent context (spec + work product)

5. Confirm the code's stated intent:
   - For PR diffs: extract intent from PR description; if missing, ASK.
   - For repos / packages: extract from README or package metadata; if
     missing, ASK.
   - For subagent_two_stage: the task spec IS the intent (verbatim).
   - Record as `stated_intent`.

6. Confirm session mode (full / targeted / post_mortem / diff / iterative).

7. Viability gate: IF the scope contains no readable source files →
   HALT with finding NOT_CODE. Do not proceed to Layer 1.

8. Test-output capture (optional):
   - If user provides test results (pass/fail counts, coverage report,
     mutation testing output), capture as evidence for L5-TST.
   - If not provided: L5-TST checks operate on test files alone, not
     on test execution.
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

### Layer 1 — Correctness (L1-COR)

*Does the code do what its specification (including its name, signature, comments, docstrings, and stated intent) claims it does?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 1.1 | **Signature / name match** | Function/class name or signature implies behavior the body does not perform (e.g. `is_valid()` returning a value but never validating; `parse_int(s)` accepting any object) |
| 1.2 | **Docstring / comment alignment** | A docstring or comment describes behavior the code does not implement, or the code does something the docstring/comment does not mention |
| 1.3 | **Off-by-one / boundary errors** | Loop bounds, slice indices, or comparison operators that produce wrong results at boundaries (≤ vs <, len() vs len()-1, inclusive vs exclusive ranges) |
| 1.4 | **Null / undefined handling** | Code dereferences/uses values that may be null/undefined without explicit handling (no guard, no Option/Result, no `if x:` check) |
| 1.5 | **Side effects vs purity claims** | Code documented as pure/read-only that performs I/O, mutation, or state change (or vice versa) |
| 1.6 | **Type-coercion correctness** | Implicit type coercion that produces wrong results (string-vs-number comparison in JS, integer-overflow truncation, float equality without epsilon) |
| 1.7 | **Logic dead-end** | Code paths that cannot be reached by any input, OR conditional branches whose conditions are tautological/contradictory (always-true / always-false IFs that mask bugs) |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 7) × 100.

### Layer 2 — Security (L2-SEC)

*Are there exploitable vulnerabilities or unsafe patterns?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 2.1 | **Injection surfaces** | User-controlled input flows into SQL, shell, OS exec, eval, deserialization, template render, or LLM prompt without sanitization or parameterization |
| 2.2 | **Authentication / authorization gaps** | Endpoints, RPC handlers, or sensitive functions without authn/authz check; privilege checks performed AFTER side effects |
| 2.3 | **Secret exposure** | Hardcoded credentials, API keys, tokens, private keys; secrets logged or returned in error messages; `.env` content leaked into VCS |
| 2.4 | **Cryptography misuse** | Custom crypto; ECB mode; static IV/nonce; weak hashes (MD5/SHA1) for security; missing constant-time comparison for secrets |
| 2.5 | **Input validation** | External inputs accepted without bounds, type, format, or schema validation; deserialization of untrusted data into rich types |
| 2.6 | **TOCTOU / race-condition vulnerability** | Time-of-check vs time-of-use gaps that an attacker can exploit (file existence check then open; permission check then operation) |
| 2.7 | **Resource exhaustion** | Unbounded loops, allocations, or recursions on user-controlled input; missing rate limit, size limit, or timeout on external-facing surfaces |
| 2.8 | **Unsafe defaults** | Default-permissive permissions, default-disabled TLS verification, default-on debug/dev features in production code paths |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 8) × 100.

### Layer 3 — Performance (L3-PRF)

*Is the code's resource use proportionate to its purpose?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 3.1 | **Algorithmic complexity** | Use of O(n²) or worse where O(n log n) or O(n) is straightforward; nested loops over the same collection that could be a hash join |
| 3.2 | **N+1 queries / loops over remote calls** | Calls to DB / RPC / HTTP / file I/O inside a loop that could be batched |
| 3.3 | **Allocation hot paths** | Repeated allocations in tight loops (string concat in a loop, fresh collection per iteration, boxing of primitives in hot paths) |
| 3.4 | **Unbounded memory** | Reading entire large file/stream into memory when streaming would suffice; collections that grow without bound |
| 3.5 | **Synchronous I/O on hot paths** | Blocking I/O on the request-serving thread in async runtimes; missing async/await where the platform supports it |
| 3.6 | **Cache absence or invalidation** | Repeated identical computations / fetches that have no caching layer; or caches with no eviction strategy and no TTL |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

**Note on verification limits.** Without runtime profiling, the auditor
flags *patterns* known to underperform — not measured slowness.
Severity is assigned deterministically per `@audit-engine`
§"Deterministic vocabulary":

- **ADVISORY** by default.
- **MAJOR** when the pattern lies on the **primary execution path**
  (per §Deterministic vocabulary > `primary_execution_path`).
- **CRITICAL** only when **all three** conditions hold:
  1. the pattern is on the **primary execution path**, AND
  2. the artifact under audit cites at least one threshold from
     §Deterministic vocabulary > `expected_load`, AND
  3. the pattern would breach that cited threshold (e.g. ≥ O(n²) in
     a loop over a `≥10⁶`-item batch, or unbounded allocation under a
     `≥10 invocations/second` load).

If the artifact does not cite an `expected_load` threshold, severity
caps at MAJOR (per §Deterministic vocabulary > `expected_load` >
`if_artifact_silent`).

### Layer 4 — Maintainability (L4-MNT)

*Can a competent engineer understand, modify, and extend this code?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 4.1 | **Cyclomatic complexity** | Function/method cyclomatic complexity > 15 (warning / PARTIAL) or > 25 (FAIL); measured by a per-language closed tool list — see §"Cyclomatic-complexity tool list" below. If no tool result is supplied, this check is SKIPPED with note `"Cyclomatic complexity not measured — supply tool output for next audit."` Subjective phrases — exhaustively `"feels complex"`, `"looks gnarly"`, `"seems hard"` — are forbidden; this check ONLY consumes deterministic tool output. |
| 4.2 | **Function length** | Function/method body > 100 LOC (warning) or > 200 LOC (FAIL); excludes data definitions and tests |
| 4.3 | **Naming clarity** (closed criteria — see "L4.3 closed criteria" sub-block below) | FAIL if **any one** of conditions (a)–(d) below holds. The four conditions are deterministic and exhaustive; subjective judgment ("feels unclear") is not permitted. |
| 4.4 | **Dead code** | Unreachable functions, commented-out blocks left in source, unused imports/variables, vestigial parameters |
| 4.5 | **Magic numbers / strings** | Numeric or string literals embedded in logic without naming or rationale, when reuse or future change is plausible |
| 4.6 | **Coupling / responsibility** | Single class/module that mixes ≥ 3 unrelated responsibilities; cross-module reach-around (accessing `obj._private` from outside its owner) |
| 4.7 | **Comment quality** | Comments that paraphrase the code instead of explaining intent; absent comments where intent is non-obvious; outdated comments contradicting current behavior |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 7) × 100.

#### L4.3 closed criteria (Naming clarity)

L4.3 FAILs if **any one** of these four conditions holds for an
identifier in scope:

```yaml
l4_3_naming_clarity_criteria:

  a_banned_short_token:
    rule: >
      Identifier matches the closed banned-token regex AND the symbol
      is at module-level or class-level scope (not a loop counter,
      not a short-lived local inside a function body).
    regex: "^(x|y|z|i|j|k|tmp|temp|data|val|var|res|ret|obj|item|thing|stuff|info|misc)\\d*$"
    note: "Loop counters `i`, `j`, `k` inside a `for`/`while` body are exempt."

  b_banned_verb_stem_function_name:
    rule: >
      Identifier is used as a function/method name AND its stem is in
      the closed banned verb-stem list. Suffixed and prefixed variants
      count (e.g. `do_thing_v2`, `process_item`, `handler`).
    closed_list: ["do_thing", "process", "handle", "manage", "run", "execute", "perform", "work", "go", "proc"]

  c_misleading_prefix:
    rule: >
      Identifier prefix promises a behavior the body does not deliver.
      Closed prefix-to-behavior map below; any deviation is a FAIL.
    prefix_behavior_map:
      "validate_*": "MUST return a bool, return a Result, or raise on invalid input."
      "is_*":       "MUST return a bool."
      "has_*":      "MUST return a bool."
      "can_*":      "MUST return a bool."
      "get_*":      "MUST be side-effect-free (no I/O, no mutation)."
      "set_*":      "MUST mutate exactly the named property; nothing else."
      "parse_*":    "MUST consume input and produce structured output (not merely validate)."

  d_unregistered_caps_run:
    rule: >
      Identifier contains ≥ 2 consecutive ALL-CAPS tokens (each token
      length ≥ 2) AND those tokens are NOT a registered acronym in a
      project glossary cited by `stated_intent`. Examples that FAIL
      without a glossary entry: `XML_HTTP_REQ`, `URLDB_LOAD`. Examples
      that PASS: `HTTP_GET` (HTTP / GET both well-known), `JSON_PATH`.
```

The check is computable from the source tree alone (plus the glossary
named in `stated_intent`, if any).

#### Cyclomatic-complexity tool list (closed; L4.1 reference)

L4.1 is deterministic. The auditor consumes tool output, never invents
a complexity number. Per-language tool list:

```yaml
cyclomatic_complexity_tools:
  python:    "radon (cc -s)"
  js_ts:     "eslint-plugin-complexity (or `complexity-report`)"
  rust:      "cargo-geiger or rust-code-analysis"
  go:        "gocyclo"
  java_kt:   "PMD or Checkstyle (CyclomaticComplexity rule)"
  csharp:    "SonarAnalyzer.CSharp"
  ruby:      "rubocop --only Metrics/CyclomaticComplexity"
  c_cpp:     "lizard"

skipped_without_tool:
  rule: >
    If no tool result is supplied as audit input for the language(s)
    in scope, L4.1 is SKIPPED with note
    "Cyclomatic complexity not measured — supply tool output for next audit."
  recording: "decision_trace.auditor_notes"
```

The auditor MUST NOT estimate cyclomatic complexity by inspection.
Either a listed tool's output is supplied, or L4.1 is SKIPPED.

### Layer 5 — Testability (L5-TST)

*Is the code testable, and is it tested?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 5.1 | **Test presence** | Public function/class without an associated test (failure scope: per public surface, not per file) |
| 5.2 | **Edge-case coverage** | Tests cover only the happy path; missing tests for null/empty input, boundary values, malformed input, error paths, concurrency edges (where applicable) |
| 5.3 | **Test determinism** | Tests that depend on wall-clock time, random seeds without fixing them, network calls without mocking, file system without isolation |
| 5.4 | **Test isolation** | Tests that share mutable state, depend on execution order, or leave artifacts that affect later tests |
| 5.5 | **Mock/stub appropriateness** | Tests that mock the code under test (testing nothing), mock so heavily that real-world behavior is invisible, or mock standard library calls without justification |
| 5.6 | **Coverage signal** | If a coverage report was supplied: line coverage < 60% (FAIL) or 60–80% (PARTIAL); branch coverage missing entirely (FAIL when language supports it). If no coverage report: SKIPPED with note. |
| 5.7 | **Hard-to-test design** | Code whose structure makes testing implausible without major refactor: hidden static state, unbounded constructor work, unmockable dependencies hardcoded inside business logic |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 7) × 100.

### Layer 6 — API Design (L6-API)

*Are the public contracts of this code sound?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 6.1 | **Public surface clarity** | Public functions/types whose role in the public API is undocumented; "public by accident" symbols (forgotten to mark private) |
| 6.2 | **Parameter design** | Functions with long, positional parameter lists where named/keyword args are supported by the language; boolean flag parameters that fork behavior (replace with two functions or an enum) |
| 6.3 | **Return-type clarity** | Functions that return polymorphic results (sometimes a value, sometimes null, sometimes a list, sometimes an exception) without a unified Result/Either type or documented contract |
| 6.4 | **Error contracts** | Functions that document a happy-path return but don't document failure modes (which errors? which exceptions? which sentinels?) |
| 6.5 | **Backward compatibility (diff/PR scope only)** | Changes that break a public signature, behavior, or schema without a documented deprecation path, version bump, or migration note |
| 6.6 | **Version pinning** | Public APIs that depend on internal/private symbols of dependencies, or pin versions to a narrow range without rationale |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

### Layer 7 — Concurrency (L7-CNC)

*Is concurrent code safe and correct?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 7.1 | **Shared mutable state** | Mutable state accessed from multiple threads/tasks without synchronization (no lock, no atomic, no actor/channel boundary) |
| 7.2 | **Lock ordering** | Multiple locks acquired in inconsistent orders across code paths (deadlock risk) |
| 7.3 | **Async correctness** | `await` skipped on async-returning calls; `Promise`/`Future` discarded; `async` function called synchronously in a way the language's runtime treats as fire-and-forget |
| 7.4 | **Cancellation handling** | Long-running async operations with no cancellation token / signal / timeout; resource cleanup on cancellation absent |
| 7.5 | **Race-condition surfaces** | Compound check-then-act on shared state without atomicity (e.g. read counter, increment, write — without atomic increment) |
| 7.6 | **Deadlock / livelock surfaces** | Patterns prone to circular waits (acquire A then B in one path, B then A in another); spin-loops without backoff or termination condition |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

**SKIPPED rule (deterministic, per-language keyword check).** ALL L7
checks are SKIPPED and the layer score is excluded from the overall
average (renormalize weights) **iff** the entire scope qualifies as
**`single_threaded_synchronous`** per `@audit-engine` §"Deterministic
vocabulary" — that is, the scope contains **zero** occurrences of the
language-specific concurrency keywords listed there:

```yaml
l7_skipped_decision:
  per_language_match:
    python:    "regex: async|await|asyncio|threading|multiprocessing|concurrent\\.futures"
    js_ts:     "regex: async|await|Promise|Worker|setImmediate|setTimeout.*callback|queueMicrotask"
    rust:      "regex: async|await|tokio|rayon|std::thread|std::sync"
    go:        "regex: \\bgo\\s+\\w|goroutine|\\bchan\\s|\\bselect\\s*\\{"
    java_kt:   "regex: CompletableFuture|ExecutorService|Thread|coroutine|suspend"
    ruby:      "regex: Thread|Fiber|Async|Concurrent::"
    csharp:    "regex: async|await|Task|Thread|Parallel"
    c_cpp:     "regex: pthread|std::thread|std::async|OpenMP|MPI"
  decision:
    on_zero_matches_in_all_files: "L7 entire layer = SKIPPED."
    on_one_or_more_matches:       "L7 runs as normal; SKIPPED forbidden."
  recording:
    field: "decision_trace.auditor_notes"
    value: "L7-CNC SKIPPED via single_threaded_synchronous keyword check (zero matches across <N> files in scope)."
```

The match is performed file-by-file across the scope. Comments and
string literals are NOT excluded — concurrency keywords inside string
literals are conservative-included (they still indicate intent / risk
of templated concurrency code). Regex matching is case-sensitive
(language keywords are case-sensitive in every supported language
above).

### Layer 8 — Structural Quality (L8-STR)

*Is the codebase organized in a way that supports change over time?*

| ID | Check | What Fails It |
| --- | --- | --- |
| 8.1 | **Module/package boundary clarity** | Modules with no clear single purpose; package contents that span unrelated concerns; "util" or "helpers" packages that have grown into junk drawers |
| 8.2 | **Dependency direction** | Layered architecture with cycles (A imports B, B imports A); domain logic depending on infrastructure layer instead of the reverse |
| 8.3 | **File organization** | Source files containing unrelated definitions; one file per public class/symbol violated without justification (where the language convention is one-per-file) |
| 8.4 | **Build / dependency hygiene** | Unpinned dependencies in build manifests; redundant dependencies; dev-only packages in production manifests; missing lockfile |
| 8.5 | **Configuration management** | Configuration values hardcoded where environment variables or config files are appropriate; environment-specific code paths chosen by hostname/timestamp instead of explicit config |
| 8.6 | **Repository hygiene** | Generated files committed to VCS (build outputs, IDE state, OS metadata); large binaries without LFS; license/README absence in shippable artifacts |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

---

## Layer Weights & Tier Overrides

### Code layer weights (used in overall score)

```yaml
code_layer_weights:
  L1-COR (Correctness):           0.20    # Highest — wrong is worse than slow
  L2-SEC (Security):              0.20    # Tied — exploitable is worse than wrong-but-safe
  L3-PRF (Performance):           0.10
  L4-MNT (Maintainability):       0.10
  L5-TST (Testability):           0.15
  L6-API (API Design):            0.10
  L7-CNC (Concurrency):           0.10    # Renormalized away if all L7 SKIPPED
  L8-STR (Structural Quality):    0.05
                                  -----
                                   1.00
```

### Code-specific tier overrides

These stack on top of the universal overrides defined in `@audit-engine`.

```yaml
code_overrides:
  - condition: "Layer 1 (Correctness) has ≥ 2 FAILed checks"
    cap: "D"
    reason: "Multiple correctness FAILs indicate the code does not do what its surface claims. Trust is broken."
    # Same check-level threshold semantics as workflow-audit's L1.

  - condition: "Layer 2 (Security) has any CRITICAL severity finding"
    cap: "D"
    reason: "Exploitable security vulnerabilities block deployment regardless of other layer scores."

  - condition: "Layer 2 (Security) has ≥ 2 MAJOR-or-higher findings (not CRITICAL — those are caught above)"
    cap: "C"
    reason: "Multiple security MAJORs indicate systemic gaps in defensive posture."

  - condition: "Layer 5 (Testability) score < 40 AND scope_type is one of {package, repo, pr_diff, commit_range}"
    cap: "C"
    reason: "Untested code at meaningful scope is not deployable. (Single-file scope is exempted; experimentation is OK.)"

  - condition: "Layer 7 (Concurrency) has any race-condition or deadlock CRITICAL finding (not SKIPPED)"
    cap: "D"
    reason: "Concurrency bugs are nondeterministic in production and effectively unfixable without a redesign."
```

When combined with engine universal overrides, conflicts are resolved by
taking the **stricter** cap.

---

## Code `category` enum extensions

Code findings extend the universal `category` enum with these
code-specific values:

- `CORRECTNESS_BUG` — semantic bug; code does not do what surface claims.
- `SECURITY_VULN` — exploitable vulnerability.
- `PERFORMANCE_PATTERN` — known anti-pattern; not a measured slowness.
- `RACE_CONDITION` — concurrency bug.
- `RESOURCE_LEAK` — file handle, connection, memory not released.
- `API_BREAKAGE` — public-surface change without compatibility path.
- `TEST_GAP` — missing or inadequate test coverage.
- `DEAD_CODE` — unreachable or unused code.
- `BUILD_HYGIENE` — build/dependency config issue.

These coexist with the universal values
(`AMBIGUITY | BROKEN_REF | STALE_REF | UNREACHABLE | UNHANDLED |
CONTRADICTION | SCOPE_LEAK | ASSUMPTION | REDUNDANCY | STRUCTURAL |
UNVERIFIABLE`).

---

## Code-Specific Edge Cases

```yaml
edge_cases:
  vendored_code:
    condition: >
      Source under audit includes a vendored / third-party copy. Closed
      path-marker list (any path that matches one or more of these
      substrings, case-sensitive): `/vendor/`, `/third_party/`,
      `/node_modules/`, `/external/`, `/deps/`, `/lib/external/`. No
      other paths qualify as vendored without an explicit user
      declaration in `stated_intent`.
    action: >
      SKIP all layers for vendored paths. Emit a single ADVISORY finding
      in L8-STR noting the vendored directory and recommending it be
      excluded from CI lints if not already. Record the matched paths in
      `artifact_format.vendored_paths`.

  generated_code:
    condition: >
      Files declared as generated, recognized by **one or more** of the
      following closed criteria:
        (1) Filename matches `*.gen.<ext>`, `*_pb2.py`, `*.pb.go`,
            `*.pb.cc`, `*.pb.h`, `*-generated.*`.
        (2) First 5 non-blank lines contain a header comment matching
            the closed regex
            `/^\s*(#|\/\/|\/\*|<!--|--).*\b(@?generated|DO[\s_-]*NOT[\s_-]*EDIT|auto[\s_-]*generated|GENERATED FILE|machine[\s_-]*generated|This file was generated)\b/i`.
        (3) File is a **build artifact** per `@audit-engine`
            §Deterministic vocabulary > `build_artifact`.
    action: >
      SKIP L4-MNT (Maintainability) for generated files entirely. Other
      layers apply ONLY where the generator itself is in scope. Note in
      decision_trace which files were treated as generated and which of
      criteria (1)/(2)/(3) matched per file. Record the matched paths
      in `artifact_format.generated_paths`.

  binary_files:
    condition: "Non-text file (image, font, compiled binary, archive) appears in input"
    action: >
      Record an ADVISORY finding in L8-STR (repository hygiene) if the
      file is in source-tree without LFS or justification. Do not
      attempt to audit binary contents.

  pr_diff_with_deletions:
    condition: "PR diff includes deleted files"
    action: >
      For each deleted file: run L6.5 (Backward compatibility) to check
      whether deletion breaks public API. Other layers do NOT apply to
      deleted files (there is no code there to audit).

  empty_diff:
    condition: "scope_type=pr_diff or commit_range, but base..head has no changes (or only whitespace/comment changes)"
    action: >
      HALT at viability gate. Emit finding NOTHING_TO_AUDIT. Suggest
      user verify SHAs.

  language_extension_unknown:
    condition: "File extension not in the language enum"
    action: >
      ASK the user explicitly. Do not guess language. Possibilities:
      proprietary DSL, unsupported language, or test fixture data.

  monorepo_with_multiple_languages:
    condition: "scope_type=repo or package contains multiple languages"
    action: >
      Run audit per-language partition. Aggregate layer scores by
      language-weighted average (weight = LOC per language, normalized).
      Report each language's tier separately AND the aggregate tier.

  test_files_in_scope:
    condition: "Test files (matched via test directory or naming convention) included in scope"
    action: >
      Apply L1-COR, L4-MNT, L8-STR with relaxed thresholds (cyclomatic
      complexity allowance +5; function length allowance +50 LOC). L5-TST
      checks treat test files AS the artifact under audit — meta-tests
      are out of scope.

  syntax_errors:
    condition: "Source file contains syntax errors that prevent parsing"
    action: >
      Record a CRITICAL finding in L1-COR. If a parser produces partial
      AST, audit the parseable portion. If unreadable, invoke
      layer-failure protocol (engine).

  no_stated_intent_for_repo:
    condition: "scope_type=repo or package, no README or package metadata, user declines to state intent"
    action: >
      Proceed with a degraded audit. L1.2 (docstring/comment alignment)
      and L6 (API design) become advisory-only — without intent, the
      auditor cannot judge whether the API matches purpose. Record
      degradation in decision_trace.auditor_notes.

  oversized_file:
    condition: "A single file in scope exceeds 5,000 LOC (non-blank, non-comment per `@audit-engine` §Deterministic vocabulary > `non_blank_line`)."
    action: >
      Audit per-element only (function/method/class boundary per the
      Mode 5 element-boundary rule). Do NOT load the full file body
      into a single context for whole-file checks. Record in
      `decision_trace.auditor_notes` which files exceeded the threshold
      and the per-element pass count for each. L8-STR.3 (file
      organization) emits an ADVISORY finding by default for any
      oversized file; MAJOR if the file mixes ≥ 3 unrelated
      responsibilities (per `@audit-engine` §Deterministic vocabulary >
      `junk_drawer`).
```

---

## Code-Specific Error Policy

| Condition | Action |
| --- | --- |
| No source provided | HALT. Request source. Do not audit nothing. |
| Scope ambiguous (path could be file, folder, or PR ref) | HALT. Ask user to specify scope_type. |
| Cannot parse a file in scope | Record as CRITICAL finding in L1-COR. Continue audit on parseable files. |
| Language not in enum | HALT. Ask user. Do not guess. |
| User asks to skip a layer in Mode 1 (FULL) | Refuse. Offer Mode 2 (TARGETED) instead. |
| User asks for "performance audit only" | Run Mode 2 with layers = [L3-PRF]. Do not pretend other layers passed. |
| Audit would require executing code (e.g. fuzz test, profile) | Refuse. Code-audit is static analysis only. Recommend a separate execution-based session. |
| Out-of-scope request ("fix this for me", "add tests for X", "refactor this module") | Emit structured refusal. Route to user action / separate implementation session. |
| Test output contradicts code-audit findings (test passes despite finding) | Keep the finding. Note the contradiction in decision_trace.auditor_notes. The code may be wrong AND the test may be wrong. |

---

## Output Contract additions

The base `audit_report` and `finding` schemas are owned by `@audit-engine`.
This command populates:

- `domain` = `CODE`
- `audit_id` prefix = `CDA-`
- `artifact_format` = a structured object:

```yaml
artifact_format:
  scope_type:    [enum]      # FILE | FILE_SET | MODULE | PACKAGE | PR_DIFF | COMMIT_RANGE | REPO | SUBAGENT_TWO_STAGE
  language:      [list<enum>]   # one or more LANG_* values; MIXED reserved for hetero scopes
  loc:           [integer]   # Total non-blank, non-comment LOC in scope
  base_sha:      [string | null]   # Only for PR_DIFF / COMMIT_RANGE
  head_sha:      [string | null]   # Only for PR_DIFF / COMMIT_RANGE
  pr_url:        [string | null]   # Only for PR_DIFF
  generated_paths: [list<string>]  # Paths skipped per generated_code edge case
  vendored_paths:  [list<string>]  # Paths skipped per vendored_code edge case
  subagent:                            # Only for SUBAGENT_TWO_STAGE
    task_id:        [string | null]
    task_spec:      [string]
    work_product:   [list<string>]    # File paths produced by implementer
    stage:          [enum | null]     # SPEC_COMPLIANCE | CODE_QUALITY | FINAL_REVIEW
    iteration:      [integer | null]  # Re-review iteration counter for this stage
```

The `layers[]` array contains 8 entries (L1-COR through L8-STR) in Mode 1
(FULL) and Mode 5 (ITERATIVE). A subset in Mode 2 (TARGETED). L7-CNC
MAY be SKIPPED for synchronous-only scopes (renormalize weights when
this happens).

In Mode 5, the engine's iteration block and remediation_plan block apply
verbatim. The Mode 5 procedure (steps M5-1 through M5-10) is owned by
the engine; this command supplies the layer set, check definitions, and
the element-boundary rule that each granular pass uses.

---

## Element boundary for Mode 5 (M5-3)

For code-audit Mode 5 granular passes, the element boundary is (use the
first matching level — never blend levels):

1. **Function / method** — the smallest function or method definition,
   regardless of language. Lambdas / closures / anonymous functions
   nested inside another function are NOT separate elements; they are
   evaluated as part of their enclosing function.
2. **Class / type** — when the class has no method body in scope (e.g.
   data class, struct, interface), the class itself is the element.
3. **Module-level statements** — top-level statements outside any
   function/class (imports, constants, side-effecting initialization).
   Treated as a single element per file.
4. **File** — when none of levels 1–3 apply (rare; configuration-only
   files, or files with one large block).

Element boundaries are language-aware. The closed cross-language map
for level 1 (function/method) is:

```yaml
function_method_keyword_map:
  python:    "def | async def"
  js_ts:     "function | const <name> = (...) => | class method"
  rust:      "fn | async fn"
  go:        "func"
  java:      "method declaration inside class (any visibility)"
  kotlin:    "fun | suspend fun"
  csharp:    "method declaration inside class (any visibility)"
  ruby:      "def"
  swift:     "func"
  scala:     "def"
  elixir:    "def | defp"
  clojure:   "defn | defn-"
  cpp_c:     "function definition (any non-class top-level or member)"
```

Any keyword not in this map: ASK before scoring; do not invent a
boundary.

`finding.location` MUST cite the element-boundary level used (e.g.
`"Function (level 1): src/parser.py:parse_input @ L42-L88"` or
`"File (level 4): config/defaults.yaml @ L1-L20"`).

---

## Subagent two-stage gate methodology

Use this section when `@code-audit` is invoked from a subagent-driven
development workflow — i.e. the caller runs an implementer subagent per
task and uses code-audit as the review gate before advancing to the next
task.

### Why two stages

Combining "does this match the task spec?" with "is this code well-built?"
into a single review pass tends to weight one concern over the other and
produces inconsistent gates. Splitting the review into two strictly-ordered
stages makes each gate produce a clean signal: stage 1 fails = work
product diverged from spec; stage 2 fails = work product matches spec but
isn't well-built. The two stages are dependent (stage 2 cannot start
until stage 1 is green) so a stage-1 failure short-circuits the review
without wasting stage-2 work.

### Stage 1 — Spec Compliance

**Question answered:** does the work product match the task spec?

**Layer scope (TARGETED mode):**

- L1-COR (full layer) — does the code do what the spec describes?
- L6-API (full layer) — does the public surface match what the spec asks for?
- L4-MNT.4.3 (Naming clarity) only — do names match the spec's terminology?

All other L4 checks, all of L2 / L3 / L5 / L7 / L8 are **excluded** from
Stage 1. They run in Stage 2.

**Pass criteria:**

- Zero CRITICAL findings.
- Zero MAJOR findings.
- MINOR and ADVISORY findings are permitted (they don't block Stage 2).

**Loop until Stage 1 is green:**

1. Run targeted audit (L1-COR, L6-API, L4-MNT.4.3 only).
2. If pass criteria met → record `stage = SPEC_COMPLIANCE` complete; advance to Stage 2.
3. If pass criteria not met → return findings to the implementer subagent. The implementer revises. Re-run Stage 1 audit. Increment `subagent.iteration`.
4. **Hard cap: 3 Stage-1 iterations.** If still not green on the third → escalate as `BLOCKED` (see Status Taxonomy). Do not advance to Stage 2.

### Stage 2 — Code Quality

**Question answered:** is the work product well-built?

**Pre-condition:** Stage 1 must be green. Refuse to start Stage 2
otherwise.

**Layer scope (TARGETED mode):**

- L2-SEC (full layer)
- L3-PRF (full layer)
- L4-MNT (full layer except L4-MNT.4.3, which already passed in Stage 1)
- L5-TST (full layer)
- L7-CNC (full layer; SKIPPED if synchronous-only)
- L8-STR (full layer)

L1-COR and L6-API are **excluded** from Stage 2 (they passed in Stage 1
and re-running them is wasted work — but if Stage 2 surfaces evidence
that contradicts a Stage 1 PASS — including evidence that
L4-MNT.4.3 was scored on stale names — that contradiction is itself a
Stage 2 finding).

**Pass criteria:**

- Zero CRITICAL findings.
- Zero MAJOR findings.
- MINOR findings are permitted but flagged.
- ADVISORY findings are informational.

**Loop until Stage 2 is green:**

1. Run targeted audit (L2-SEC, L3-PRF, L4-MNT minus L4-MNT.4.3, L5-TST, L7-CNC, L8-STR).
2. If pass criteria met → record `stage = CODE_QUALITY` complete; the
   task is done.
3. If pass criteria not met → return findings. Implementer revises.
   Re-run Stage 2 audit (NOT Stage 1 — Stage 1 stays green). Increment
   `subagent.iteration`.
4. **Hard cap: 3 Stage-2 iterations.** If still not green on the third
   → escalate as `BLOCKED`.

### Per-task vs final review

- **Per-task:** Stage 1 then Stage 2, as above. Run after each
  implementer-subagent task, before advancing to the next task.
- **Final review:** After all tasks complete, run a **full Mode 1 audit**
  (`@code-audit <scope> full`) on the entire implementation. The final
  review is NOT two-stage — it's a complete 8-layer audit on the
  whole work, intended to catch cross-task issues that per-task gates
  cannot see: architecture coherence across tasks, dependency cycles
  between tasks, test-suite consistency, and any contradictions
  between per-task PASS verdicts and the integrated whole.
  - If the final review surfaces CRITICAL or MAJOR findings: return to
    implementer for whole-implementation revisions. Re-run final review.
    Hard cap: 3 final-review iterations.

### Subagent two-stage cognitive-load contract

Subagent two-stage scope activates the **9-slot** cognitive-load profile
from `@audit-engine` §"Mode 5 state externalization > Effect on
cognitive load (closed state-slot list)". The slots are:

```yaml
subagent_two_stage_active_slots:
  S1_pass_number:                  "Mode 5 pass counter (still in use)"
  S2_intent_anchor:                "task spec is the intent_anchor (immutable)"
  S3_current_pass_findings_buffer: "current Stage findings"
  S4_scratchpad_id:                "engine bootstrap scratchpad"
  S5_halt_evaluation_state:        "NORMAL | PENDING_HALT | HALTED"
  S6_stage:                        "SPEC_COMPLIANCE | CODE_QUALITY | FINAL_REVIEW"
  S7_iteration_counter:            "Stage 1 / Stage 2 / Final iteration counter (cap 3)"
  S8_spec_anchor:                  "task spec verbatim (== intent_anchor for this scope)"
  S9_work_product_paths:           "list of file paths produced by implementer"

design_target: "9 active slots → cognitive-load check is PARTIAL (per engine list)."

forbidden_extra_slots: >
  Tokenizers, file-readers, regex engines, AST parsers, the implementer
  subagent's own internal state, and the iteration cap constants are
  NOT counted as slots in this scope.
```

Auditor MUST NOT introduce new slots. The closed-list of forbidden
inventions: no Stage-1.5, no Stage-2.5, no "reviewer mood", no
"implementer trust score", no "session sentiment" (see §"Red flags"
for the canonical no-invent rule). Adding a tenth slot — by any name —
is a PARTIAL → FAIL transition for the cognitive-load check.

### Subagent status taxonomy

When the caller orchestrating subagents asks code-audit for the result
of a per-task review, code-audit returns one of these statuses:

- **DONE** — Stage 1 green, Stage 2 green. Task complete. Advance.
- **DONE_WITH_CONCERNS** — Both stages green; MINOR findings remain.
  Note them in the `audit_report.routing.informational` queue. Advance,
  but the caller may opt to fix MINOR findings before the final review.
- **NEEDS_CONTEXT** — Audit cannot complete because the task spec or
  the work product is incomplete or ambiguous (e.g. missing function
  signatures, ambiguous spec terminology, work product references files
  that are not in scope). Halt the audit. Return the specific gap.
  Caller's job to resolve before re-invoking.
- **BLOCKED** — Audit completed but the work product cannot pass within
  the iteration cap. Surface the consolidated findings. Caller MUST
  intervene (re-spec the task, replace the implementer, or escalate to
  human). Code-audit will NOT loop further.

### Reviewer prompt templates (pointers, not duplicates)

The actual prompt templates for the implementer, the spec-compliance
reviewer, and the code-quality reviewer live in the upstream
`subagent-driven-development` skill. Do NOT duplicate them here. When
running a per-task gate, the auditor (code-audit operating in Stage 1
or Stage 2) reads:

- Implementer prompt template:
  `%USERPROFILE%\.cursor\plugins\cache\cursor-public\superpowers\b7a8f76985f1e93e75dd2f2a3b424dc731bd9d37\skills\subagent-driven-development\` (folder; resolve template filename from that folder's contents).
- Spec-compliance reviewer prompt: same folder.
- Code-quality reviewer prompt: same folder.

**Cache-path warning.** The hash segment
(`b7a8f76985f1e93e75dd2f2a3b424dc731bd9d37`) is plugin-cache-version-
specific and may change on plugin update. The auditor handles a stale
cache path **deterministically** (no improvisation):

1. Treat the path as a pre-flight target. The engine's
   §"Pre-flight verification" PF-4 / PF-5 are the structural
   precedents; this is an additional template-readability check
   layered on top.
2. If the canonical path resolves and is readable, proceed.
3. If the canonical path fails to resolve, run
   `Get-ChildItem \"$env:USERPROFILE\.cursor\plugins\cache\cursor-public\superpowers\"`
   to enumerate the current cache directory, then resolve under
   `<cache-dir>\skills\subagent-driven-development\`. This is the
   ONLY permitted recovery; do not search elsewhere.
4. If recovery still fails → HALT with `halt_reason: PRE_FLIGHT_FAILURE`
   per `@audit-engine` §"Pre-flight verification". Do NOT proceed to a
   stage that depends on the missing template.

The unified `code-review---iterative` skill (when installed under
`%USERPROFILE%\.cursor\skills-cursor\code-review---iterative\SKILL.md`)
also references these templates with the same path; `code-review---iterative`
§3.7 is the deduplicated narrative for this lane. If that file is absent,
treat the skill as unregistered and rely on this command plus the
superpowers `receiving-code-review` / `requesting-code-review` skills for
non-audit review lanes.

### Red flags (forbidden moves)

- **NEVER** start Stage 2 before Stage 1 is green.
- **NEVER** run a "code quality only" audit and call it complete — that
  bypasses Stage 1.
- **NEVER** let self-review replace real review. The implementer
  subagent's own claim that the work is correct is not evidence; the
  audit produces evidence. Do not weight the implementer's status
  message in the audit's PASS/FAIL judgment.
- **NEVER** advance to the next task while the current task has
  CRITICAL or MAJOR findings open. MINOR is acceptable per the
  pass criteria.
- **NEVER** run implementer subagents in parallel for the same task.
  The audit cannot reason about race conditions in the development
  process itself; serialize per task.
- **NEVER** silently retry an audit pass after the iteration cap. Halt
  with `BLOCKED`.
- **NEVER** invent a stage 1.5 or 2.5. The two-stage gate is exactly
  two stages.

### Model-tier policy

When the caller dispatches roles to different model tiers, code-audit
recommends:

- **Implementer:** the **least-capable** model that fits the role's
  language and complexity. Saves cost; the gate catches errors.
- **Spec-compliance reviewer (Stage 1):** a **mid-tier** model. Stage 1
  is structurally narrower than Stage 2; it does not benefit
  proportionally from a top-tier model.
- **Code-quality reviewer (Stage 2):** the **strongest available**
  model. Stage 2 has the broadest layer scope and the highest cost of
  a missed finding.
- **Final reviewer (whole implementation):** the **strongest available**
  model. Same rationale as Stage 2, plus cross-task coherence requires
  the largest reasoning surface.

This is a recommendation, not a requirement. The caller decides; the
audit's PASS/FAIL judgment is independent of the reviewer's model tier.

---

## Companion Commands

- **`@audit-engine`** (`C:\Users\rtoth\.cursor\commands\audit-engine\COMMAND.md`)
  — Orchestrator. Owns the loop semantics. Required reading before any audit.
- **`references/audit_workflow.md`**
  (`C:\Users\rtoth\.cursor\commands\audit-engine\references\audit_workflow.md`)
  — Sibling workflow-domain module. Loaded by `@audit-engine` for the workflow
  partition of mixed-content runs.
- **`code-review---iterative`** (skill) — Companion skill for non-audit
  review *lanes* (request, receive, PR babysit). When this audit's
  findings need to be dispatched to a separate reviewer, that skill
  hosts the request/receive cycle. The iterative full-tree review and
  subagent two-stage gates lanes from that skill ARE captured here in
  `@code-audit`; the other lanes remain there.
- **`context-bootstrap`** (skill) — Session continuity. Mode 5 always
  crosses sessions, so a bootstrap entry is required at handoff to the
  implementation session.
- **`deterministic-prompt-builder`** (skill) — RARELY invoked from
  code-audit (it's for prompts, not code). Used only when the code
  under audit is a prompt artifact (e.g. an LLM tool's system-prompt
  string baked into source); routes via `prompt_builder_substeps`.

---

## Procedure Summary

```
INVOCATION: @code-audit [<scope_type>] [<mode>]
            (or loaded by @audit-engine on code partition;
             canonical: audit-engine/references/audit_code.md)

STEP 0:  Pre-Audit Setup
         → Confirm scope → Generate audit_id (CDA-...) → Identify language(s)
         → Confirm scope_type → Confirm intent → Capture optional test output
         → Run viability gate

STEP 1:  Execute Audit Layers 1–4 (correctness + posture)
         For each layer (L1-COR, L2-SEC, L3-PRF, L4-MNT):
           → Run all checks (engine per-check error protocol applies)
           → Record findings
           → Calculate layer score
           → If layer cannot complete → invoke engine layer-failure protocol

CHECKPOINT: Summarize Layers 1–4 findings before continuing.
            Pay special attention to L2-SEC CRITICAL findings;
            those cap the tier at D regardless of remaining layers.

STEP 2:  Execute Audit Layers 5–8 (testability + design + concurrency + structure)
         For each layer (L5-TST, L6-API, L7-CNC, L8-STR):
           → Run all checks
           → Record findings
           → Calculate layer score
           → L7-CNC: SKIP all checks if scope is synchronous-only;
             renormalize layer weights accordingly.

STEP 3:  Calculate overall score and tier
         → Weighted average with code_layer_weights
         → Apply universal overrides (engine) + code_overrides
         → Stricter cap wins on conflict

STEP 4:  Classify and route findings
         → Severity per engine severity_definitions
         → Sort: severity DESC, layer order ASC
         → Routing: USER_ACTION (most code findings),
                    INFORMATIONAL (advisory style/perf),
                    PROMPT_BUILDER (rare — only for prompt-string code)

STEP 5:  Assemble report
         → Populate audit_report (engine schema)
         → domain = CODE; audit_id = CDA-...
         → Populate artifact_format with scope_type, language list, LOC,
           SHAs/PR-URL if applicable, generated/vendored path lists.

STEP 6:  Present to user
         → Deliver the audit report
         → Highlight CRITICAL security and correctness findings first.
         → Offer: "Want me to drill into any layer or specific finding?"
         → If post_mortem: present root_cause mapping
         → If diff: present comparative table
         → If iterative (Mode 5): proceed per engine M5 procedure

STEP 7:  Route on user confirmation
         → User confirms routing queues
         → Findings routed to user action or implementation session.
         → For review-workflow handoff: cite code-review---iterative skill.

MODE 5:  Steps M5-1 through M5-10 are owned by @audit-engine.
         Each granular pass (M5-3) runs all 8 code layers per the engine's
         per-check protocol. Element boundary for M5-3:
           1. Function / method
           2. Class / type (when no method body in scope)
           3. Module-level statements
           4. File (when none of 1–3 apply)
         (Use the first matching level; never blend levels.)

SUBAGENT TWO-STAGE: scope_type=subagent_two_stage
         Stage 1 (TARGETED: L1-COR, L6-API, L4-MNT.4.3 only)
           → Loop until zero MAJOR-or-higher; cap 3 iterations.
           → On cap: BLOCKED.
         Stage 2 (TARGETED: L2-SEC, L3-PRF, L4-MNT minus L4-MNT.4.3, L5-TST, L7-CNC, L8-STR)
           → Pre-condition: Stage 1 green (canonical at §"Stage 2 — Code Quality > Pre-condition").
           → Loop until zero MAJOR-or-higher; cap 3 iterations.
           → On cap: BLOCKED.
         Final review (after all tasks): full Mode 1 audit.
         Status taxonomy: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED.
```
