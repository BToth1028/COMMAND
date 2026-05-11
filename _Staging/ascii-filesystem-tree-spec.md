# ASCII Filesystem Tree — Rendering Specification

**Purpose:** deterministic format for rendering filesystem architectures
(planes, folders, files, lifecycle metadata, identity rules, constraints)
as a connected ASCII tree where vertical = sibling order within a scope,
horizontal = containment depth, and every node carries inline metadata
describing its role, lifecycle class, mutability, and identity rule.

**Use this format when:** the goal is to *see* the topology of a
filesystem architecture — which planes exist at root, what each plane
governs, what lifecycle class each carries, what subdirectory structure
is permitted/forbidden inside each.

**Do NOT use this format when:** the goal is decision flow / control
logic (use `ascii-decision-tree-spec.md`), executable code, prose
explanation, or graphical rendering (Mermaid/PlantUML/etc.).

**Relationship to `ascii-decision-tree-spec.md`:** This spec is a
sibling, not a derivative. Both share the Unicode box-drawing visual
vocabulary and indentation rules, but the semantics differ: this spec
models *containment* (parent contains child); the decision-tree spec
models *flow* (decision branches to outcome). Symbols are mapped
accordingly — most notably, this spec drops the `►` arrowheads on T-/L-
junctions because folders don't "flow to" their children.

---

## 1. Trigger phrases

Any of these in a request invokes this format:

- "ASCII filesystem tree"
- "render the architecture as an ASCII tree"
- "tree out the file structure"
- "filesystem architecture tree"
- "AFT format" (shorthand)
- "render this folder structure"
- "use the filesystem-tree spec"

---

## 2. Layout grammar

### 2.1 Axes

| Axis | Meaning |
|---|---|
| Top → bottom | Sibling order within a scope. Default convention: alphabetical (case-insensitive, Windows/macOS default). |
| Left → right | Containment depth. Each nested level indents exactly one column unit (4 spaces) from the parent's `│`. |

### 2.2 Symbol set (canonical Unicode box-drawing)

| Symbol | Role |
|---|---|
| `│` | Vertical scope line. Means "still inside this scope, more siblings below." Runs continuously down the left edge of the scope. |
| `├──` | T-junction: child node with siblings below it. NO arrowhead — children are contained, not flowed-to. |
| `└──` | L-junction: last child in its scope. NO arrowhead. |
| `[ROLE \| constraint \| identity]` | Inline plane annotation. Square brackets always. Pipe-separated tags. Used for top-level planes and major plane-level subdirectories. |
| `<placeholder>` | Variable node name. Angle brackets always. Indicates "any value matching this slot." Examples: `<slug>`, `<uuid>`, `<project-slug>`. |
| `name/` | Folder: trailing slash mandatory. |
| `name.ext` | File: no trailing slash; extension always shown. |
| Comment under `│   text` | Constraint, rule, or forbidden-behavior note. Hangs under parent `│` with 4-space indent + plain text, NO junction symbol. |

### 2.3 ASCII fallback (when Unicode renders badly)

| Unicode | ASCII |
|---|---|
| `│` | `\|` |
| `├──` | `+--` |
| `└──` | `\--` |

Use ASCII fallback only when explicitly requested ("ASCII fallback"
modifier) or when the rendering target can't display Unicode
box-drawing.

### 2.4 What gets a junction vs. what doesn't

| Element | Junction? |
|---|---|
| Folders | Yes — `├──` or `└──` |
| Files | Yes — `├──` or `└──` |
| Placeholders | Yes — `├──` or `└──` |
| Plane annotation | No — inline on the same line as the node, after the node name |
| Constraint / rule / forbidden notes | No — hang under parent `│` with 4-space indent, no junction |
| Lifecycle / identity tags | No — inline as part of plane annotation `[brackets]` |
| Inline description (for leaves) | No — hang on same line as node, after node name, no brackets |

This separation is the core readability principle: **only structural
nodes get junctions.** Annotations, constraints, and descriptions hang
quietly without competing for visual weight.

### 2.5 Indentation rules

- One nested level = exactly **one column unit (4 spaces)** of right-shift from the parent's `│`.
- Each scope's vertical `│` runs continuously from its first `├──` down through every sibling, terminating at the `└──` line.
- Constraint / rule notes indent **4 extra spaces** inside their parent's `│` (so they sit under the node body, not under the `│` itself).
- Empty `│` lines (just the vertical line, no content) separate sibling nodes for readability — required between every pair of siblings.

### 2.6 Annotation column alignment

- Plane annotations should align to a **consistent column** (typically column 50–60) where reasonable.
- Pad the gap between node name and annotation with **spaces** (NOT `─` characters — those are reserved for connectors).
- Acceptable to break alignment if a node name is much longer than others, or if a deeply nested node would push alignment past ~110 columns.
- Readability beats perfect alignment — never break a node across two lines just to hit the alignment column.

### 2.7 Folder vs file vs placeholder

| Form | Meaning |
|---|---|
| `name/` | Concrete folder (always exists or always allowed in this position) |
| `name.ext` | Concrete file (always exists or always allowed) |
| `<placeholder>/` | Variable folder slot (any matching value) |
| `<placeholder>.<ext>` | Variable file slot |
| `<placeholder>` | Fully variable file slot, extension also variable (rare) |

Trailing `/` on folders is **mandatory** — it is the visual
disambiguator between folders and files at a glance.

---

## 3. Annotation conventions

### 3.1 Plane annotation (at root planes and major subdirectories)

Format: `[ROLE | mutability | identity-rule]`

| Field | Examples |
|---|---|
| ROLE | CANONICAL, EXECUTABLE, LIFECYCLE, HISTORY, DERIVED, ARCHIVE, GENERATED, PROJECT |
| Mutability | immutable post-publish, mutable, append-only, write-locked, regenerable, gitignored |
| Identity rule | UUIDv7+slug, path-based, project-slug, timestamp+session_id, [name].[uuidv7].[ext] |

Example: `[CANONICAL | immutable post-publish | UUIDv7+slug, flat]`

Three-field is the standard. Two-field is acceptable for inner
subdirectories where one field is implied by the parent plane.
One-field is acceptable only for clearly self-explanatory cases.

### 3.2 Constraint / rule notes

Hang under the parent node's `│` with 4-space indent and plain text. Use
these conventional prefixes:

| Prefix | Meaning |
|---|---|
| `no subdirectories permitted` | This plane/folder is flat by rule |
| `subdirs allowed` | Nesting is explicitly permitted under this node |
| `forbidden:` | Explicit prohibition (what cannot live here) |
| `required:` | Explicit requirement (what must be present) |
| `rule:` | Cross-cutting governance rule |
| `e.g., <example>` | Concrete example for clarity |
| `promotion path: X → Y` | Lifecycle transition between planes |
| `triggered by:` | What causes this node to receive content |

### 3.3 Inline description (for leaf nodes)

For example files / placeholders, append a short human-readable
description after the node name with NO brackets — just plain text after
adequate spacing. Example:

```
└── pyproject.toml                                project metadata; canonical config
```

### 3.4 Multiple annotations on one node

Stack constraint notes on consecutive comment lines under the node's
`│`, indented 4 spaces from the `│`:

```
├── corpus/                                        [CANONICAL | immutable post-publish | UUIDv7+slug, flat]
│   │   no subdirectories permitted (FSA closed-world rule)
│   │   recursive structure carried by relation graph, NOT folders
│   │
│   └── <slug>--<short-uuid>.yaml                 governed YAML envelope
```

---

## 4. Hierarchy conventions

### 4.1 Top-level entry

Always begin with `START <architecture-name>` at column 0, followed by a
single `└──` opening to the workspace/project root:

```
START workspace-architecture
│
└── {workspace_root}/
    │
    ├── ...
```

The single `└──` from `START` opens the body. The workspace root itself
is the first node. Architecture name should be a slug describing the
scope (e.g., `workspace-architecture`, `pdkos-v2-fsa`,
`example-project`).

### 4.2 Sibling ordering within scope

**Default sort: alphabetical, case-insensitive** (Windows/macOS
convention).

For workspaces using case-sensitive POSIX sort (Linux default), state
the convention explicitly via the `posix-sort` modifier.

Common ordering exceptions to call out via `rule:` note when applied:

| Exception | When to use |
|---|---|
| Folders before files at same level | Operator preference for visual grouping |
| Numeric-prefix nodes by numeric value | PARA `0_inbox/`, `1_projects/`, etc. — sort by digit |
| Underscore-prefix nodes clustered | If workspace policy clusters infrastructure planes |

Sibling spacing: empty `│` line between every pair of siblings is
**required** (per §2.5).

### 4.3 Mixing folders and files in the same scope

Folders and files may appear as siblings. Default convention: sort
alphabetically with no folder/file precedence. State chosen convention
in a `rule:` note if it matters.

### 4.4 Plane vs. concrete-instance distinction

- **Plane** = a closed-world top-level role (e.g., `corpus/`, `_PARA/`). Always carries a `[ROLE | ...]` annotation.
- **Concrete instance** = a specific folder or file at a position (e.g., `pyproject.toml`, `1_projects/my-project/`). Carries an inline description if helpful, no plane annotation.
- **Placeholder** = a variable slot (`<project-slug>/`, `<slug>--<uuid>.yaml`). Wrapped in `<...>`. Inline description optional.

---

## 5. Anti-patterns (do NOT do these)

| Don't | Do |
|---|---|
| Mix Unicode and ASCII symbols (`│` and `\|` in same tree) | Pick one set per tree |
| Use indentation without `│` connecting lines | Every nested scope has a continuous vertical line |
| Put `►` arrowheads on T-/L-junctions | Containment uses plain `├──` and `└──`; `►` is reserved for the decision-tree spec |
| Render the tree as Mermaid, PlantUML, or an image | ASCII in a fenced code block, always |
| Put multiple nodes on one line | One node per line, always |
| Skip the empty `│` separator between siblings | Always include the blank `│` line between siblings |
| Use square brackets for placeholders | Square brackets = annotations; angle brackets = placeholders |
| Use angle brackets for plane annotations | Angle brackets = placeholders; square brackets = annotations |
| Omit the trailing `/` on folder names | Folders ALWAYS show trailing `/` |
| Use `─` characters to pad annotation gap | Use spaces; `─` is reserved for junction connectors |
| Write prose explanations inside scopes | Use constraint notes (`forbidden:`, `rule:`, etc.) only; prose goes outside the tree |
| Allow a tree to exceed ~110 columns | Break with shorter node names, compress annotations, or drop optional fields |
| Use plane annotations on every node | Annotations are for top-level planes and major subdirectories; concrete instances get descriptions, not annotations |

---

## 6. Modifiers (append to trigger phrase)

| Modifier | Effect |
|---|---|
| `annotations only` | Show plane annotations but suppress constraint / rule notes |
| `structure only` | Suppress all annotations, notes, and descriptions; pure folder/file topology |
| `with key` | Append a separate plane-summary key block below the tree |
| `with placeholders` | Show `<slug>` / `<uuid>` placeholder leaves explicitly |
| `concrete only` | Suppress all `<placeholder>` leaves; show only fixed nodes |
| `ASCII fallback` | Use `\|`, `+--`, `\--` instead of Unicode box characters |
| `posix-sort` | Use case-sensitive alphabetical sort instead of default case-insensitive |
| `compact` | Drop empty `│` separators between siblings (denser, less readable) |
| `with exceptions` | Highlight closed-world violations / carve-outs explicitly |

Combine modifiers with commas: `"AFT format, with key, concrete only"`.

---

## 7. Worked example (canonical reference)

A small project layout demonstrating folders, files, placeholders, plane
annotations, constraint notes, inline descriptions, and mixed sibling
types.

```
START example-project
│
└── my-project/                                    [PROJECT | mutable | path-based]
    │
    ├── _build/                                    [GENERATED | regenerable | gitignored]
    │   │
    │   └── <html-output>/
    │
    ├── docs/                                      Sphinx documentation source
    │   │   forbidden: build artifacts (use _build/)
    │   │
    │   └── index.md
    │
    ├── src/                                       source code
    │   │   subdirs allowed
    │   │
    │   ├── core/                                  business logic modules
    │   │   │
    │   │   ├── __init__.py
    │   │   │
    │   │   └── engine.py
    │   │
    │   └── utils/                                 helpers, no business logic
    │       │
    │       └── helpers.py
    │
    ├── tests/                                     pytest suite; mirrors src/ structure
    │   │
    │   └── test_engine.py
    │
    ├── pyproject.toml                             canonical project metadata
    │
    └── README.md
```

This example demonstrates: nested folders, leaf files, a placeholder
(`<html-output>/`), a plane annotation
(`[GENERATED | regenerable | gitignored]`), constraint notes
(`forbidden: build artifacts`, `subdirs allowed`), inline descriptions
(`pytest suite; mirrors src/ structure`), and mixed folder+file
siblings.

---

## 8. Quality gates (self-check before delivering)

A rendered tree passes if **all** of these are true:

- [ ] Every nested scope has a continuous `│` left edge.
- [ ] Every sibling pair is separated by an empty `│` line.
- [ ] Every folder name ends with `/`.
- [ ] Every file name has an extension (no extensionless files unless intentional and noted).
- [ ] No mixing of Unicode and ASCII symbols.
- [ ] No `►` arrowheads on junctions (those belong in the decision-tree spec).
- [ ] Square brackets `[...]` only used for plane annotations.
- [ ] Angle brackets `<...>` only used for placeholders.
- [ ] Annotation column reasonably aligned (within ~5 columns of consistent target).
- [ ] Tree width does not exceed ~110 columns.
- [ ] One node per line; no multi-node lines.
- [ ] Hierarchy reads top-to-bottom = sibling order, left-to-right = containment depth.
- [ ] Constraint / rule notes hang under `│` with 4-space indent (no junction).
- [ ] Plane annotations only on planes / major subdirectories, not on every node.

If any gate fails, fix before delivering.

---

## 9. Versioning

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-29 | Initial specification, derived from `ascii-decision-tree-spec.md` v1.0 with adaptations for containment-tree semantics. |
