# ASCII Decision Tree — Rendering Specification

**Purpose:** deterministic format for rendering branching logic (decision
trees, conditional pseudo-code, control flow, dispatch logic, audit
flowcharts) as a connected ASCII tree where vertical = execution order,
horizontal = nesting depth, and every branch is visually tied to its
parent and its outcome.

**Use this format when:** the goal is to *see* the topology of decisions
— who runs first, who decides what, where each branch ends up.

**Use explanatory context mode when:** the topology alone is not enough
to understand why each phase exists, what state changes there, or why a
handoff occurs. Explanatory context stays local to the relevant branch or
label and must remain bounded.

**Do NOT use this format when:** the goal is executable code, prose
explanation, or graphical rendering (Mermaid/PlantUML/etc.).

---

## 1. Trigger phrases

Any of these in a request invokes this format:

- "ASCII decision tree"
- "render this as a connected branch tree"
- "flowchart it in ASCII, code-tree style"
- "tree it out (ASCII tree style)"
- "use the bootstrap-start tree style"
- "ASCII tree (same style as before)"
- "ADT format" (shorthand)

---

## 2. Layout grammar

### 2.1 Axes

| Axis | Meaning |
|---|---|
| Top → bottom | Execution order. First statements at the top of their scope, terminations at the bottom of their branch. |
| Left → right | Nesting depth. Each nested `IF` indents exactly one column unit (4 spaces) to the right of its parent. |

### 2.2 Symbol set (canonical Unicode box-drawing)

| Symbol | Role |
|---|---|
| `│` | Vertical scope line. Means "still inside this scope, more siblings below." Runs continuously down the left edge of the scope. |
| `├─►` | Branch with siblings below it. T-junction. |
| `└─►` | Last branch in its scope. L-junction. No more siblings at this level. |
| `─────►` | Horizontal outcome arrow. Points from a decision/branch body to its destination. Length is whatever's needed to align with sibling outcomes. |
| `[LABEL]` | Named target / handoff point. Brackets always. Examples: `[INGEST]`, `[STOP]`, `[REC]`. |
| `↺` | Loop back to a prior point. Followed by the loop target name, e.g., `↺ loop pre-flight`. |
| `◄──────` | (Optional, in convergence-annotation mode) Reverse arrow at landing points showing where flow arrives from. |

### 2.3 ASCII fallback (when Unicode renders badly)

| Unicode | ASCII |
|---|---|
| `│` | `\|` |
| `├─►` | `+->` |
| `└─►` | `\->` |
| `─────►` | `----->` |
| `↺` | `<->` or `LOOP:` |
| `◄──────` | `<-----` |

Use ASCII fallback only when explicitly requested ("ASCII fallback" modifier) or when the rendering target can't display Unicode box-drawing.

### 2.4 What gets an arrow vs. what doesn't

| Element | Arrow? |
|---|---|
| Decisions (`IF`, `ELSE IF`, `ELSE`) | Yes — branch off with `├─►` / `└─►` |
| Terminations (handoffs, halts, loops, returns) | Yes — horizontal `────►` ending in label |
| Convergence points (where branches rejoin) | Yes — both branches arrow to the same `[LABEL]` |
| Plain statements (assignments, prompts, side effects) | **No** — hang under `│` with leading spaces only |
| Comments / clarifications | **No** — hang under `│` as inline text |

This separation is the core readability principle: **only flow-relevant nodes get arrows.** Statements stay quiet.

### 2.5 Explanatory context lines

Explanatory context lines are allowed when the reader needs enough local
prose to understand the step or decision without leaving the tree.

Use them for:

- the purpose of a phase or label;
- the rule being enforced at a decision point;
- the state change caused by a branch;
- why a handoff target is reached.

Do not use them for:

- full policy text;
- implementation details better kept in source files;
- historical background not needed to follow the branch;
- duplicated prose already obvious from the branch label.

Format:

```text
[INGEST]
│
│   Purpose: load the selected prior bootstrap and prove it is usable.
│   Rule: ingest does not choose files; selection already happened.
│
├─► IF bootstrap loads and validates
│   │   Prior session state is now available.
│   └──────────────────────────────────────────────► [AUDIT]
```

Rules:

- Context lines must hang under the active `│` scope.
- Prefer 1-3 context lines per phase or branch.
- Each context line should be one short sentence or sentence fragment.
- Do not put arrows on context lines.
- If a phase needs more than 3 context lines, move the detail to prose
  outside the tree and keep only the local decision-relevant summary.

### 2.6 Indentation rules

- One nested `IF` = exactly **one column unit (4 spaces)** of right-shift from its parent's `│`.
- Each scope's vertical `│` runs continuously from its first `├─►` down through every sibling, terminating at the `└─►` line.
- Statements indent **2 extra spaces** inside their parent branch's `│` (so they sit under the branch body, not under the `│` itself).
- Empty `│` lines (just the vertical line, no content) separate sibling branches for readability — required between every pair of siblings.

### 2.7 Right-side outcome alignment

- All terminal `►` arrows in a single tree should align to the **same column** where reasonable.
- Pad the gap between branch body and arrow with `─` characters.
- Acceptable to break alignment if a branch label is much longer than others, or if a deeply nested branch would push alignment past ~90 columns.
- Readability beats perfect alignment — never break a branch across two lines just to hit the alignment column.

---

## 3. Convergence and re-entry

### 3.1 Two branches → same outcome

Both branches arrow to the **same `[LABEL]`**:

```
├─► branch A ────────► [SHARED-TARGET]
└─► branch B ────────► [SHARED-TARGET]
```

### 3.2 Loop-back

Use `↺` followed by the named loop target:

```
└─► ELSE ──────────► ↺ loop pre-flight
```

### 3.3 Fall-through to next sequential step

When a branch returns control to the mainline (no jump, no halt), write `fall through to step X`:

```
└─► ELSE (no lock) ──► fall through to step B
```

Don't invent a label for fall-through; `step B` is enough because the reader can see step B directly below in the tree.

### 3.4 Convergence-annotation mode (modifier: "annotate convergence")

At each landing point label, add a comment line listing every source branch:

```
[INGEST]  ◄────── from PATH_1, PATH_2(single confirmed), PATH_2(operator-picked)
```

Use this only when there are 3+ converging sources or when the convergence isn't obvious from spatial proximity.

---

## 4. Hierarchy conventions

### 4.1 Top-level entry

Always begin with `START <command-or-function-name>` at column 0, followed by:

```
START <name>
│
└─► <first scope>
```

The single `└─►` from `START` opens the body. If there are multiple top-level scopes (rare), use `├─►`/`└─►` siblings.

### 4.2 Sequential steps within a scope

Sequential steps are siblings at the same indent level under a parent branch:

```
├─► step A: <description>
│   │
│   ├─► <decisions inside step A>
│   └─► ...
│
└─► step B: <description>
    │
    └─► <decisions inside step B>
```

Step A runs before step B. Inside each step, decisions branch further right.

### 4.3 Returning from a sub-tree

When a sub-tree's outcome is "return to parent and continue," use `fall through` (see §3.3). When it's "exit the parent entirely," arrow to `[STOP]` or whatever the exit label is.

---

## 5. Anti-patterns (do NOT do these)

| Don't | Do |
|---|---|
| Mix Unicode and ASCII symbols (`│` and `\|` in same tree) | Pick one set per tree |
| Use indentation without `│` connecting lines | Every nested scope has a continuous vertical line |
| Put arrows on plain statements | Statements have no arrows — only decisions and terminations |
| Render the tree as Mermaid, PlantUML, or an image | ASCII in a fenced code block, always |
| Put multiple decisions on one line | One decision per line, always |
| Skip the empty `│` separator between siblings | Always include the blank `│` line between siblings |
| Bury branches under long prose blocks | Use bounded explanatory context lines: local, short, and decision-relevant |
| Leave a branch with no outcome arrow and no nested children | Every leaf branch must terminate (arrow or fall-through) |
| Use unbracketed labels | Targets are always `[BRACKETED]` |
| Allow a tree to exceed ~110 columns | Break with shorter branch text or use the convergence-annotation modifier |

---

## 6. Modifiers (append to trigger phrase)

| Modifier | Effect |
|---|---|
| `decisions only` | Suppress all assignments/prompts; show pure branch topology |
| `explanatory context` | Add bounded local prose lines under phases, labels, and branches |
| `include statement arrows` | Statements also get `►` to next statement (verbose mode) |
| `ASCII fallback` | Use `\|`, `+->`, `\->`, `----->` instead of Unicode box characters |
| `with topology summary` | Append a separate convergence-map block below the tree |
| `annotate convergence` | Tag landing points with `◄────── from [SOURCES]` notes |
| `merge with code` | Embed pseudo-code lines verbatim and overlay tree connectors |
| `compact` | Drop empty `│` separators between siblings (denser, less readable) |

Combine modifiers with commas: `"ASCII decision tree, explanatory context, with topology summary"`.

---

## 7. Worked example (canonical reference)

Source pseudo-code:

```
IF operator supplies path:
    use it
ELSE IF existing project, no specific file:
    confirm project_root
    IF lock present:
        prompt remove or halt
        IF NO: stop
        ELSE: remove lock
    scan for candidates
    IF multiple: operator picks
    ELSE IF one: confirm
    ELSE: gap
ELSE IF new project:
    session-zero
ELSE:
    ambiguous, loop
```

Rendered tree:

```
START bootstrap-start
│
└─► PRE-FLIGHT (operator-driven selection)
    │
    ├─► IF @-ref / pasted path / explicit filename
    │   │   selected_path        = PATH_1_SPECIFIC
    │   │   prior_bootstrap_path = <supplied>
    │   └────────────────────────────────────────────────► [INGEST]
    │
    ├─► ELSE IF existing project, no specific file
    │   │   selected_path = PATH_2_EXISTING
    │   │   confirm/prompt project_root
    │   │
    │   ├─► step A: lock check
    │   │   │
    │   │   ├─► IF .lock present
    │   │   │   │   prompt: "remove and continue, or halt?"
    │   │   │   │
    │   │   │   ├─► operator NO ────────────────────────► [STOP] (Q5)
    │   │   │   │
    │   │   │   └─► operator YES
    │   │   │       │   remove lock
    │   │   │       │
    │   │   │       ├─► IF no bootstrap for locked ────► [REC]
    │   │   │       │
    │   │   │       └─► ELSE ────────────────────────► fall through to step B
    │   │   │
    │   │   └─► ELSE (no lock) ──────────────────────► fall through to step B
    │   │
    │   └─► step B: SCAN dir for candidates
    │       │
    │       ├─► IF multiple ─────────────────────────► [INGEST]
    │       │
    │       ├─► ELSE IF exactly one
    │       │   │   propose most-recent
    │       │   │
    │       │   ├─► operator confirms ───────────────► [INGEST]
    │       │   │
    │       │   └─► operator does NOT confirm ──────► [STOP]
    │       │
    │       └─► ELSE zero candidates ────────────────► [GAP]
    │
    ├─► ELSE IF new project
    │   │   selected_path = PATH_3_SESSION_ZERO
    │   │   session_zero_flag = TRUE
    │   └────────────────────────────────────────────► [INIT]
    │
    └─► ELSE (no path matches)
        │   surface 3 path choices; await selection
        └────────────────────────────────────────────► ↺ loop pre-flight
```

This example demonstrates: nested decisions (3 levels deep), convergence (3 branches → `[INGEST]`), fall-through, loop-back, and aligned terminal arrows.

### 7.1 Explanatory context example

Use explanatory context mode when the tree needs to teach the reader what
is happening at each step, not merely show branch topology.

```text
START bootstrap-start
│
└─► SELECT PRIOR STATE
    │   Purpose: decide whether this session resumes, recovers, or starts clean.
    │   Rule: the agent never picks silently; operator supplies or confirms.
    │
    ├─► IF exact bootstrap path supplied
    │   │   The operator gave an @ref, absolute path, or exact YAML filename.
    │   │   The file becomes the resume source.
    │   └────────────────────────────────────────────────► [INGEST]
    │
    ├─► ELSE IF existing project supplied
    │   │   The operator identified a project, not a session file.
    │   │   Inspect the canonical live bootstrap directory.
    │   │
    │   ├─► IF lock present
    │   │   │   A prior session may have ended incorrectly.
    │   │   │   Operator chooses whether to remove the stale lock or halt.
    │   │   │
    │   │   ├─► operator chooses halt ───────────────────► [STOP]
    │   │   │
    │   │   └─► operator removes lock ───────────────────► fall through to scan
    │   │
    │   └─► scan candidates
    │       │   Only canonical bootstrap YAMLs count.
    │       │
    │       ├─► one candidate confirmed ─────────────────► [INGEST]
    │       │
    │       └─► zero candidates; session-zero confirmed ─► [INIT]
    │
    └─► ELSE ambiguous request
        │   Surface the valid start paths and wait.
        └────────────────────────────────────────────────► ↺ loop SELECT PRIOR STATE
```

This example demonstrates bounded local prose. The context lines explain
purpose, state, and operator decision points without replacing the tree
with a full prose specification.

---

## 8. Quality gates (self-check before delivering)

A rendered tree passes if **all** of these are true:

- [ ] Every nested scope has a continuous `│` left edge.
- [ ] Every sibling pair is separated by an empty `│` line.
- [ ] Every leaf branch ends with an outcome arrow OR a fall-through note.
- [ ] No statement has an arrow.
- [ ] Explanatory context, if used, is local, bounded, and decision-relevant.
- [ ] No mixing of Unicode and ASCII symbols.
- [ ] Terminal labels are bracketed: `[LIKE-THIS]`.
- [ ] Right-side arrows are aligned to a consistent column where reasonable.
- [ ] Tree width does not exceed ~110 columns.
- [ ] One decision per line; no multi-decision lines.
- [ ] Hierarchy reads top-to-bottom = execution order, left-to-right = nesting depth.

If any gate fails, fix before delivering.

---

## 9. Versioning

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-29 | Initial specification, derived from the bootstrap-start canonical exemplar. |
| 1.1 | 2026-04-30 | Added explanatory context mode for bounded local prose inside trees. |
