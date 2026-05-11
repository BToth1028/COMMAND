# Housekeeping — unified operational corpus

**Corpus root:** `C:\Users\rtoth\.cursor\commands\housekeeping`  
**Fresh systematic pass:** 2026-04-29  
**Method:** `corpus-unify` skill, with every file in the folder re-read in this pass. Executable/config sources are treated as authorities; older specs, plans, excerpts, and distilled analyses contribute only unique facts, context deltas, conflicts, tests, and audit controls.  
**Exclusions:** none. No source is copied wholesale. The two `DISTILLED_*` files are not treated as replacement registries; their useful risk, assumption, quantitative, uncertainty, metric, and test deltas are folded into the control sections.

This file is the working reference for the housekeeping corpus. It is not a paste-concat and it is not a replacement for long executable specs; where a source is the verbatim authority, this file points to it.

**How to use this file:** first identify which “housekeeping” lane you mean, then open the full authority file named in that lane before executing anything destructive, automated, or batch-oriented. Treat this document as the dispatcher, conflict ledger, and compressed operator reference. When this file and an authority source disagree, the authority source wins unless the disagreement is already called out as a conflict below.

---

## Provenance

| Source | Class | Role in this merge |
| ------ | ----- | ------------------ |
| `command.housekeeping.yaml` | Executable command spec | **Primary authority** for Cursor command behavior, stale sweep, approval gates, and Recycle Bin-only removal. |
| `rtoth-code__va__ar__Automations__Workflows__proc-housekeep.json` | Executable n8n config | **Primary authority** for deployed janitor graph: node order, endpoint path, POST bodies, timeouts, aggregate shape. |
| `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_housekeep.md` | Workflow doc | Human-readable automated janitor workflow; adds module intent, trigger scenarios, related workflow notes. |
| `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_file-mant.md` | Workflow doc | Human file triage and grading workflow; provides newest-first invariant, concept gate, routing matrix, approval points. |
| `c-code__staging__snip-harv__kn.wkfl.00.01.19_snip-harv.md` | Workflow doc | Snippet harvest lane; provides scanner inputs, noise filters, triage syntax, v3.1 enrichment, slug filename conflict. |
| `c-code__staging__snip-stor__kn.wkfl.00.01.19_snip-stor.md` | Workflow doc | Snippet storage lane; provides hash identity, normalization algorithm, template, index update/verify pattern. |
| `housekeeping.yaml` | Older command spec | Historical command variant; retained for overlap and conflict evidence only. Loses to `command.housekeeping.yaml` on removal policy. |
| `00_INDEX_AND_SOURCES.md` | Index / map | Adds original paths, four-theme map, missing `kn.proc` note, duplicate staging pointers, related chat pointers. |
| `housekeeping_unified_corpus.md` | Prior unified file / current target | Superseded in place by this fresh pass. Its useful structure is retained, stale assumptions are corrected, and this row remains as provenance for the previous merge state. |
| `DISTILLED_mult-sess-blueprint_full.md` | Meta-analysis / audit blueprint | Folded for unique registry names R1-R11, quantitative primitives Q1-Q20, assumptions A#1-A#8, metric bundles, failure modes, and 16 test ideas compressed into consolidated rows. |
| `DISTILLED_mult-sess-blueprint_reduced.md` | Meta-analysis / reduced blueprint | Folded for tier framing, uncertainty IDs U#1-U#3, reduced acceptance tests, and “wrong playbook” failure mode. Fully subsumed where it duplicates the full blueprint. |
| `personal-snippet.command.housekeeping.md` | Raw operator prompt | Fully subsumed by `command.housekeeping.yaml`; preserved here as origin of the two-stage Recycle Bin approval flow. |
| `rtoth-code__specstory__housekeeping-procedure-summary_EXCERPT.md` | Historical excerpt | Adds legacy seven-step `kn.proc` procedure, old path evidence, schedules, and archive continuity rule. |
| `cursor_plans__housekeeping_batch_p5_9f85cc6d.plan.md` | Out-of-domain homonym plan | Kept as DB / Access / SQLite maintenance island; not folded into file hygiene. |
| `cursor_plans__housekeeping_system_completion_6c3bfff8.plan.md` | Roadmap / backlog plan | Kept as planned cross-reference and workflow-completion island; not treated as current behavior. |

---

## Merge Guardrails

- **No source is dropped silently.** Every file in the folder is listed in provenance; source-specific deltas are either retained below or explicitly marked as superseded / historical / out-of-domain.
- **Executable artifacts win for runtime facts.** `command.housekeeping.yaml` wins for Cursor command behavior; `proc-housekeep.json` wins for deployed n8n path, POST bodies, node order, timeout values, response shape, and absent/present auth fields.
- **Human workflow docs win for operator intent.** Markdown workflows supply when-to-use guidance, approval points, review mindset, and workflow relationships unless they conflict with executable config.
- **Historical and blueprint files do not override current command authority.** Both `DISTILLED_*` files analyze the older `housekeeping.yaml`; their old soft/hard-delete facts remain only as conflict evidence after `command.housekeeping.yaml` introduced Recycle Bin-only removal.
- **Plans are backlog unless verified elsewhere.** A Cursor plan with pending frontmatter is a roadmap, not proof that the referenced deliverables exist or are wired.
- **User approval remains an execution authority.** Inside the Cursor command, the operator’s explicit approval or rejection controls modification and removal actions even when this merge identifies a preferred source.
- **Freshness rule.** `command.housekeeping.yaml` and this unified corpus are newer than the distilled blueprints; any D1 / `housekeeping.yaml` claim in the blueprints must be translated through the current command spec before use.
- **Do not import destructive vocabulary across lanes.** `DELETE` in file maintenance, pending cleanup in n8n, and `REMOVE` in the Cursor command are separate operations with different approvals and destinations.

---

## 1. Disambiguation

The word **housekeeping** names multiple systems. Treat the artifact type as the dispatch key.

1. **Cursor command / session file hygiene (`command.housekeeping.yaml`):** session-touched files plus optional stale sweep; approval-gated keep / relocate / rename / remove proposals; removal only through the desktop Recycle Bin.
2. **Automated janitor (`proc-housekeep.json` + `kn.wkfl..._housekeep.md`):** delt-scan → pend-clnp → fldr-clnp; webhook/manual/scheduled; no per-file PARA classification.
3. **Human file maintenance (`kn.wkfl..._file-mant.md`):** newest-first inventory, concept review, 4-axis grading, route to file-comp / refine / hold / archive / delete staging.
4. **Snippet lifecycle (`snip-harv` + `snip-stor`):** extract reusable code and store it in `li/code/snippets/`; contains an unresolved filename scheme conflict.
5. **Legacy vault housekeeping (`kn.proc` excerpt):** seven-step compliance / registry / taxonomy / archive review; historical unless the missing procedure file is restored.
6. **P5 “Housekeeping batch”:** Access / SQLite / axioms maintenance; same word, different domain.
7. **System-completion roadmap:** future xref and module wiring; plan snapshot, not deployed fact.

---

## 2. Authority and tier order

**Conflict rule:** higher-quality / higher-tier data wins. The operational order for this corpus is:

1. `command.housekeeping.yaml` for Cursor command semantics.
2. `proc-housekeep.json` for n8n runtime facts.
3. Tier A workflow docs (`housekeep`, `file-mant`, `snip-harv`, `snip-stor`) for operator narrative and local context.
4. `housekeeping.yaml`, index, excerpt, plans, and blueprint files only where they add non-duplicative context or expose conflicts.

**Config vs prose:** If `proc-housekeep.json` and markdown disagree, JSON wins for deployed path, payload, timeout, and graph order.

**Current removal policy:** `command.housekeeping.yaml` wins over `housekeeping.yaml`; no permanent deletion, no `Remove-Item`, no `_trash` soft-delete flow as command authority.

**Distillation caveat:** rows labeled D1 in the blueprint files refer to the older `housekeeping.yaml`, not the newer `command.housekeeping.yaml`. In this merged corpus, D1-derived quantitative thresholds remain useful, but D1-derived deletion semantics are superseded.

### Operational dispatch matrix

| If the operator means... | Use this lane | Authority | Guardrail |
| --- | --- | --- | --- |
| Session-created or session-modified files, stale-looking workspace files, rename / relocate / Recycle Bin proposals | Cursor command | `command.housekeeping.yaml` | Approval first; in-depth review before removal; Recycle Bin only. |
| Scheduled or manual repository janitor run | Automated janitor | `proc-housekeep.json` plus `kn.wkfl..._housekeep.md` | JSON wins for deployed endpoint, bodies, timeouts, and node order. |
| Reviewing legacy/imported files for value and routing | Human file maintenance | `kn.wkfl..._file-mant.md` | Newest-first; concept review before grading; approval before routing. |
| Extracting reusable code from source files | Snippet harvest | `kn.wkfl..._snip-harv.md` | User triage and v3.1 enrichment before storage. |
| Storing a reusable snippet in the library | Snippet storage | `kn.wkfl..._snip-stor.md` | Deduplicate by normalized 12-char hash before creating a file. |
| Seven-step compliance / registry / archive audit | Legacy procedure | SpecStory excerpt only | Historical unless the missing `kn.proc` file is restored. |
| Access / SQLite / axiom cleanup batch | P5 DB batch | `cursor_plans__housekeeping_batch_p5_9f85cc6d.plan.md` | Out-of-domain homonym; do not apply file-cleanup rules. |
| Term/path cross-reference wiring | System-completion roadmap | `cursor_plans__housekeeping_system_completion_6c3bfff8.plan.md` | Pending roadmap unless separately verified. |

---

## 3. Cursor command — session file hygiene

**Full text:** `command.housekeeping.yaml`

**Mission:** Review session-touched files and stale candidates; propose retain / relocate / rename / Recycle Bin removal per file; execute only after explicit approvals; emit decision and audit records; optionally integrate with an active bootstrap checkpoint.

**Scope and non-scope:**

- In scope: session-touched file enumeration, optional stale-folder sweep when `cross_session_sweep` is enabled, multi-check pipeline, per-file proposals, approvals, execution, records, git hints.
- Out of scope: bootstrap finalization, PARA logic itself, reorganization outside session scope unless sweep enabled, file body rewrites, permanent deletion.

**Inputs and defaults:**

- Required: `workspace_root`, `project_name`.
- Optional: `in_memory_bootstrap`, `cross_session_sweep=false`, `approval_mode=per_file`, `removal_destination=desktop_recycle_bin`, `git_integration=true`, `explicit_file_list`, `stub_threshold_chars=50`, `duplicate_overlap_threshold=0.85`.
- Mode: `integrated` if bootstrap exists and session is unended; otherwise `standalone`.
- Ignored: files outside workspace root, bootstrap files themselves, hidden files unless explicitly targeted, and `.git` internals.

**Candidate order:**

1. `explicit_file_list` if provided, exclusively.
2. Workspace files modified after session start.
3. Files referenced in completed tasks when integrated.
4. If `cross_session_sweep`: stale-looking files discovered by folder search, non-canonical locations, and prior `STALE` audit flags.

**Per-file check order:** stub size → duplicate overlap → inbound reference scan → PARA classification → naming compliance → location compliance → cursory relevance review.

**Proposal enum:** `REMOVE`, `MERGE_OR_REMOVE`, `RELOCATE_AND_RENAME`, `RELOCATE`, `RENAME`, `KEEP_AS_IS`.

**Removal flow, condensed from the raw prompt and YAML:**

1. Search for old/stale-looking files.
2. Cursory review only to identify obvious relevance.
3. Present list and location to the operator.
4. If the operator declines (`no`, `nevermind`, or equivalent), stop removal and resume normal work.
5. If the operator approves (`Approved`, `proceed`, or equivalent), perform a deeper review before removal.
6. If deeper review confirms no use, send to the desktop Recycle Bin.
7. If deeper review finds reconsideration information, surface it and require a second explicit approval before Recycle Bin removal.
8. If the operator holds after seeing reconsideration information, leave the file untouched.

**Allowed removal techniques:** Shell.Application `InvokeVerb('delete')`; VisualBasic `FileSystem.DeleteFile(..., 'SendToRecycleBin')`.

**Forbidden:** `Remove-Item`, Shift+Delete, `delete_permanently`, fallback to permanent delete if Recycle Bin fails.

**Validation gates:** approval required; factual justification required; PARA present for kept/relocated files; reference scans populated; inbound-reference removals acknowledged; Recycle Bin destination enforced; in-depth review before every removal; second approval when reconsideration info appears; zero-context decision rationale; integrated checkpoint write-back or HARD_FAILURE; decision-id collision check.

**Error policies:** `PARA_SKILL_UNAVAILABLE`, `AMBIGUOUS_DUPLICATE`, `REFERENCE_BREAKAGE_RISK`, `NAMING_CONVENTION_UNDEFINED`, `SESSION_FILES_UNDETECTABLE`, `GIT_NOT_PRESENT`, `USER_REJECTS_ALL`, `RECYCLE_BIN_UNAVAILABLE`, `CHECKPOINT_INTEGRATION_FAILED`.

**Output contract:** structured summary with mode, session id, counts, user decisions, applied / failed actions, decision records, audit updates, bootstrap integration status, git suggestions, decision trace, and handoff.

### Conflict: `command.housekeeping.yaml` vs `housekeeping.yaml`

| Topic | Historical `housekeeping.yaml` | Current authority `command.housekeeping.yaml` |
| ----- | -------------------------------- | -------------------------------------------- |
| Removal destination | `_trash` soft-delete dir by default; hard delete possible if explicitly chosen | Desktop Recycle Bin only |
| Deletion vocabulary | `delete_mode: soft\|hard` | `removal_destination: desktop_recycle_bin` |
| Safety before removal | reference acknowledgment and soft/hard checks | reference acknowledgment + in-depth review + possible second approval |
| Failure mode | `SOFT_DELETE_DIR_UNCREATABLE` | `RECYCLE_BIN_UNAVAILABLE`, leave file untouched |
| Anti-drift | never default to hard delete | never permanently delete; never use `Remove-Item` |

**Resolution:** `housekeeping.yaml` is superseded for removal semantics. It remains useful only as history for the older command shape and shared pipeline facts.

---

## 4. Automated janitor

**Full runtime config:** `rtoth-code__va__ar__Automations__Workflows__proc-housekeep.json`  
**Human workflow doc:** `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_housekeep.md`

**Purpose:** repository hygiene automation, not Cursor session review.

**Operational chain:**

| Step | Conceptual module | JSON node | Inputs / policy | Output intent |
| ---- | ----------------- | --------- | --------------- | ------------- |
| 1 | `kn.modl.00.01.19_delt-scan` | `Step 1: Delta Scan` | `POST http://host.docker.internal:5070/mod-delt-scan`, body `{"hours": 24}`, timeout `60000` ms | modified files / count |
| 2 | `kn.modl.00.01.19_pend-clnp` | `Step 2: Pending Cleanup` | `POST .../mod-pend-clnp`, body `{"days": 14, "dry_run": false}`, timeout `30000` ms | deleted and kept pending folders |
| 3 | `kn.modl.00.01.19_fldr-clnp` | `Step 3: Folder Cleanup` | `POST .../mod-fldr-clnp`, body `{"dry_run": false}`, timeout `30000` ms | removed empty folders |
| 4 | aggregate | `Aggregate Results` | reads prior three node outputs | `status`, `procedure`, `completed`, `results` |

**Deployed webhook fact:** JSON path is `proc-housekeep`; node response mode is `lastNode`, response data is `allEntries`.

**Markdown-only context retained:** use after sessions, on schedule, manually, or after bulk file moves/deletes. The doc states a daily 02:00 ET option and records related workflows: `file-mant` may call cleanup after maintenance; `file-comp` may consume delta output.

**Conflict:** markdown shows `POST /webhook/housekeep` with Bearer auth and fixed module base paths such as `C:\Users\rtoth\code`. JSON shows path `proc-housekeep`, no encoded auth, no base path parameter, and HTTP calls to `host.docker.internal:5070`. **Resolution:** trust JSON for runtime, prose for operator intent only; verify auth and base path in the deployed n8n environment before invoking externally.

---

## 5. Human file maintenance

**Full text:** `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_file-mant.md`

**Purpose:** cleanup, reorganization, import processing, and legacy review. **Not for new files**; new files go directly to File Compliance.

**Invariant:** every pass is newest-first by modified time. Newer files establish current direction; older files are judged against that direction.

**Workflow:**

1. **Inventory (`mod-file-invt`):** target path + recursive flag; output files sorted by `LastWriteTime` descending and grouped by extension.
2. **Concept review (`mod-file-grad`, phase 1):** concept value, content quality, integration potential, directional alignment. Results: valid → grade; good but misaligned → archive notes; redundant → delete or merge; obsolete → delete.
3. **4-axis grading (`mod-file-grad`, phase 2):** Quality, Effort, Relevance, Direction, each 1-5.
4. **Route by score:** 16-20 PROMOTE → `file-comp`; 12-15 REFINE then `file-comp`; 8-11 HOLD in quarantine; 4-7 ARCHIVE with path mirroring; 1-3 DELETE after archive, then stage under `tp/stag/{YYMMDD}/`.
5. **Cleanup:** `mod-fldr-clnp`.
6. **Final approval:** `mod-user-conf`.

**Strategic context retained:** n8n over manual counters; Standard + Vault Taxonomy; path-mirrored archive with `YYMMDD/HHMM`; human-readable workflow docs under `30_Knowledge/`.

**Operator mindset:** do not grade polish alone. Concept value and directional alignment can override implementation quality.

**Approval posture:** frontmatter marks this workflow `approval_required: true`; concept review and grading both require showing results to the user before proceeding. DELETE in this lane means archive first, then stage under `tp/stag/{YYMMDD}/`; it is not the Cursor command’s Recycle Bin removal flow.

---

## 6. Snippet lifecycle

### Harvest lane

**Full text:** `c-code__staging__snip-harv__kn.wkfl.00.01.19_snip-harv.md`

- Purpose: scan source code, filter noise, let the operator triage, enrich selected candidates, and store approved snippets.
- Preconditions: source identified; harvester script available at `to\genr\03.07\21\py\to.genr.03.07.21_snip-harv.py`; `li\code\snippets\` exists; v3.1 spec understood.
- Inputs: `source_path`, `recursive` default true, language filter default all, `min_lines=5`, `max_lines=300`.
- Applies to `.py`, `.js`, `.ts`, `.css`, `.sql`, `.ps1`, `.sh`.
- Excludes binaries, `test_*`, private/internal candidates, import-only blocks, one-line assignments, config constants, duplicates.
- Extraction method deltas: Python AST; JS/TS regex; CSS regex selector blocks; SQL regex for CREATE/SELECT; PowerShell/Shell regex functions.
- Triage syntax: comma list (`1,3,5`), ranges (`1-5`), `all`, or `none`.
- Enrichment auto-fills v3.1 fields and prompts operator for description, config keys, HTML elements, and init order.
- Auto-fill deltas worth preserving: `$schema=snippet-v3.1`, `origin=extracted`, `status=active`, `has_example=true`, `has_tests=false`, source file / source lines, inferred packages, side effects, contexts, and provides.
- Store step in this doc writes `snip-{lang}-{slug}.md` and updates language, pattern, and master indexes.

### Storage lane

**Full text:** `c-code__staging__snip-stor__kn.wkfl.00.01.19_snip-stor.md`

- Purpose: add reusable code snippets with deduplication and indexing.
- Library tree: `li/code/snippets/index.md`, `by-language/`, `by-pattern/`, and individual snippets.
- Dedup identity: normalize code, then `md5(normalized)[:12]`; filename `snip-{hash}.md`.
- Normalization removes leading/trailing whitespace, empty lines, and comment-only lines beginning `#`, `//`, or `--`.
- If hash exists: add a `related_sessions` entry instead of creating a duplicate.
- Classification fields: language, type (`function`, `class`, `pattern`, `utility`, `config`), pattern tags, complexity, dependencies.
- Pattern hints include file I/O, API calls, data transforms, database, async, error handling, CLI, testing, config, and logging.
- Title generation extracts function / class names where possible, converts camelCase / PascalCase to words, and makes names descriptive and searchable.
- Dependency extraction examples are regex-based for Python imports and JavaScript import / require statements.
- Complexity: simple <=10 lines; moderate 11-50; complex >50 or deep nesting.
- Template includes title, id, type, language, tags, dependencies, complexity, timestamps, related sessions, description, code, usage example.
- Verification: file exists; language index updated; pattern index updated; master index updated; links work.
- Optional automation: `to/genr/03.07/21/py/to.genr.03.07.21_snip-extr.py` can periodically extract snippets from session logs.

### Conflict: snippet identity

| Source | Filename pattern |
| ------ | ---------------- |
| Harvest workflow | `snip-{lang}-{slug}.md` |
| Storage workflow | `snip-{hash}.md` |

**Resolution:** unresolved. Do not bulk import until one convention or a mapping rule is selected. If script implementation is used, the script’s actual output must be checked before assuming either doc is authoritative.

---

## 7. Legacy seven-step vault housekeeping

**Source:** `rtoth-code__specstory__housekeeping-procedure-summary_EXCERPT.md`

This is historical evidence from a SpecStory excerpt. The excerpt found `c:\Users\rtoth\code\kv\30_Knowledge\Procedures\kn.proc.00.01.19_housekeep.md`, but the index says the corresponding `c:\code\kv\30_Knowledge\Procedures\kn.proc.00.01.19_housekeep.md` was not found under the current repo root.

**Procedure summarized in the excerpt:**

| Step | Purpose |
| ---- | ------- |
| 1 | Delta compliance: changed files, taxonomy validation, violations |
| 2 | Project registry audit: registered vs missing vs unregistered projects |
| 3 | Spec/procedure validation under `30_Knowledge\Specifications\` and `30_Knowledge\Procedures\` |
| 4 | Taxonomy validation for `pr\*` and `kv\20_Areas\Cenhud\*`; Opus metadata gaps |
| 5 | Pending deletion cleanup: folders in `ar\pend\` older than 14 days |
| 6 | Archive continuity: compare `50_Archive` to current taxonomy, flag orphaned or moved archives |
| 7 | Update timestamp for next delta run |

**Schedules:** daily quick 6:00 AM ET for steps 1 and 5; weekly full Sunday 2:00 AM ET for all seven; on-demand configurable.

**Archive rule:** archives are never restructured; historical paths are preserved. If the source folder moved or vanished, report ORPHAN/MOVED but keep the archive intact.

**Resolution:** absent the canonical `kn.proc` file in the active tree, this lane is historical and should not override the automated janitor (`proc-housekeep.json` + workflow doc).

---

## 8. Roadmap island: system completion

**Source:** `cursor_plans__housekeeping_system_completion_6c3bfff8.plan.md`

This is a pending plan, not deployed behavior.

**Planned deliverables:**

- `kn.refd.00.01.19_term-xref.md`: mappings for terminology, filename patterns, path mappings, usage notes.
- Initial term/path examples: CFP → T1, PID → T2, GKM → T3, Carry-Forward Pack → T1_Session, `30_Knowledge` → `Areas/kn`, `20_Areas` → `Areas`.
- `kn.modl.00.01.19_refs-updt.md`: contract `file_path`, `xref_path`, `dry_run`, `sections` → `changes_made`, `updated_content`, `change_count`, `success`.
- `refs-updt` intended logic: parse the xref sheet into term, pattern, and path maps; replace long forms before short forms to avoid partial matches; replace paths last; return a change log.
- `kn.wkfl.00.01.19_file-comp.md` updates:
  - step 0.5 load xref sheet,
  - step 1.5 cross-reference lookup,
  - step 4.5 update internal references.
- Formal `kn.wkfl.00.01.19_housekeep.md` document mirroring the n8n janitor structure.
- Module relation updates for `delt-scan`, `pend-clnp`, `fldr-clnp`, and file-comp composition.

**Architecture intent:** automated subgraph `housekeep → delt-scan → pend-clnp → fldr-clnp`; manual subgraph `file-mant → file-invt/file-grad → file-comp → refs-updt → term-xref`; grading outcomes route to file-comp, update, quarantine, archive, or staging.

**Status rule:** frontmatter todos were pending at export. Treat as backlog unless separately verified.

---

## 9. Homonym island: P5 DB housekeeping batch

**Source:** `cursor_plans__housekeeping_batch_p5_9f85cc6d.plan.md`

This is not file cleanup.

**Scope:**

- Link `tblAuditLog` in Access using `LinkAuditLog` in `modNodeManager.bas`; uses existing ODBC connection string from `tblNode`; idempotently drops/relinks the table; operator action required in Access Immediate window.
- Verify/fix `tblEdgeType.Cardinality`: all seven rows may be truncated to `many-to-ma`; intended fix is `UPDATE tblEdgeType SET Cardinality = 'many-to-many' WHERE Cardinality = 'many-to-ma';`.
- Cardinality table is schema/reference; triggers do not block the update; VBA pattern matching still behaves correctly.
- Resolve axioms doc issues: `trg_attrschema_vocabulary_update` referenced/expected but not created by install scripts; update frontmatter timestamp; remove `version: "V02"`; mark prior TODO items resolved.
- Update TODO, bootstrap, and session docs; run `phase3_audit.py` pre/post.

**Execution order retained:** baseline audit → verify cardinality → update if needed → install missing trigger if needed → update axioms frontmatter → add Access link routine → update TODO/bootstrap → create session doc → final audit.

---

## 10. Cross-document controls from blueprint files

The `DISTILLED_*` files are not operational authorities, but they add useful audit scaffolding.

### Canonical registry names

| Registry | Meaning | Primary sources |
| -------- | ------- | --------------- |
| R1 | Session file hygiene | `command.housekeeping.yaml` / historical `housekeeping.yaml` |
| R2 | Automated repo housekeeping | janitor workflow + n8n JSON |
| R3 | Pending deletion retention | janitor workflow, JSON, legacy step 5 |
| R4 | Empty folder cleanup | janitor workflow + JSON |
| R5 | Human file maintenance | file-mant workflow |
| R6 | Grading routing | file-mant workflow |
| R7 | Snippet harvest | snip-harv workflow |
| R8 | Snippet storage | snip-stor workflow |
| R9 | Legacy full housekeeping audit | SpecStory excerpt |
| R10 | DB maintenance batch homonym | P5 plan |
| R11 | Planned xref system | system completion plan |

### Quantitative primitives

| Id | Value | Meaning |
| -- | ----- | ------- |
| Q1 | 50 chars | Cursor stub threshold |
| Q2 | 0.85 | Duplicate overlap threshold |
| Q3 | 0.95 | Near-identical duplicate threshold |
| Q4 | 14 days | Pending cleanup retention |
| Q5 | 24 hours | n8n delta scan body |
| Q6 | 60000 ms | delta scan timeout |
| Q7 | 30000 ms | pending cleanup timeout |
| Q8 | 30000 ms | folder cleanup timeout |
| Q9-Q10 | 1-5 | grading axis min/max |
| Q11-Q15 | 16, 12, 8, 4, 3 | promote/refine/hold/archive/delete route boundaries |
| Q16-Q17 | 5, 300 lines | snippet harvest min/max |
| Q18 | 12 hex chars | snippet hash length |
| Q19-Q20 | 10, 50 lines | simple/moderate snippet complexity boundaries |

**Tier update for Q1-Q3 and removal:** `command.housekeeping.yaml` preserves Q1-Q3 but replaces old `delete_mode` semantics with Recycle Bin-only removal.

### Uncertainties / conflicts

| Id | Conflict | Current resolution |
| -- | -------- | ------------------ |
| U#1 | Legacy seven-step breadth vs current three-step janitor | If `kn.proc` is absent, use R2 for automated behavior and keep R9 historical. |
| U#2 | “Housekeeping” label collision | Dispatch by artifact type: command YAML, n8n JSON/workflow, DB plan, snippet docs, roadmap. |
| U#3 | Snippet slug filename vs hash filename | Unresolved; block bulk import until naming rule is chosen. |
| U#4 | Old soft/hard command vs Recycle Bin command | `command.housekeeping.yaml` wins. |

### Consolidated conflict ledger

| Conflict | Sources | Resolution / operator action |
| --- | --- | --- |
| Cursor removal model changed from `_trash` / hard-delete option to Recycle Bin-only | `housekeeping.yaml`, `command.housekeeping.yaml`, both `DISTILLED_*` files | Treat `_trash`, `delete_mode`, and hard-delete language as historical. Current command removal means desktop Recycle Bin only after approvals and in-depth review. |
| n8n endpoint/auth/base-path prose differs from runtime JSON | `kn.wkfl..._housekeep.md`, `proc-housekeep.json` | JSON wins for deployed path `proc-housekeep`, POST bodies, timeouts, node chain, and absence of encoded auth. Verify actual n8n auth externally before invoking. |
| Legacy seven-step procedure is broader than current automated janitor | SpecStory excerpt, `00_INDEX_AND_SOURCES.md`, `kn.wkfl..._housekeep.md`, `proc-housekeep.json` | Historical unless `kn.proc.00.01.19_housekeep.md` is restored into the active tree. |
| Snippet identity has slug and hash variants | `snip-harv`, `snip-stor` | Do not bulk import until a canonical filename or mapping rule is chosen. Use actual script output as evidence if automation is run. |
| P5 “housekeeping batch” uses the same label for DB work | P5 plan, index, distilled blueprints | Keep isolated as Access / SQLite / axiom maintenance. Never route it through file hygiene or n8n janitor procedures. |
| System-completion plan lists deliverables that may now partially exist elsewhere | system-completion plan, current folder contents | Treat the plan frontmatter as a snapshot; verify target files before claiming completion or wiring. |

### Hidden assumptions worth preserving

- `para-ontology` is available when the Cursor command needs classification; if unavailable, do not guess.
- HTTP services at `host.docker.internal:5070` implement the module contracts shown in JSON.
- The v3.1 snippet spec is stable enough for harvest enrichment.
- The SpecStory excerpt accurately reflects the missing `kn.proc` file.
- `dry_run:false` in the n8n JSON means the pending and folder cleanup modules can mutate state.
- n8n timeouts are meaningful runtime bounds, not just UI decoration.
- Duplicate overlap thresholds correctly separate ambiguous vs near-identical files.
- 4-axis score sums map cleanly to routing bands without off-by-one errors.
- The newer `command.housekeeping.yaml` intentionally supersedes the older soft/hard delete model captured by the blueprint files.

### Compact metric/control bundles from full blueprint

The full blueprint's H/W/CE/VC layer is retained here as operator controls, not as invented KPIs.

| Bundle | Meaning in this corpus | Concrete checks retained |
| --- | --- | --- |
| H - hygiene throughput | Janitor result shape and pending-folder policy | Modified-file count, pending deleted/kept counts, empty-folder removed count, age compliance against 14 days. |
| W - workflow load / latency | Runtime bounds and command review volume | Cursor `files_reviewed` / `proposals_total`; n8n HTTP completion against 60000 / 30000 / 30000 ms. |
| CE - control thresholds | Numeric gates that alter behavior | Stub `<50` chars; duplicate ambiguity `0.85-0.95`; near-identical `>=0.95`; snippet line bounds `5-300`; delta window `24` hours. |
| VC - value coverage | Human review and snippet library quality | Four grading axes each scored 1-5; route-band correctness; normalized-code hash identity; complexity tiers <=10 / 11-50 / >50. |

### Failure modes retained from the blueprints

- **Wrong playbook:** user says “housekeeping” without an artifact. Use the disambiguation and dispatch matrix first.
- **Threshold drift:** JSON, command YAML, and workflow prose diverge on thresholds. Update related authority docs together or record a conflict.
- **Timeout silent pass:** an HTTP node returns success with a partial or malformed body. Schema-validate module responses before trusting cleanup completion.
- **Band mis-route:** a score sum routes to the wrong file-maintenance outcome. Test exact boundary values.
- **Snippet identity drift:** slug and hash naming coexist without mapping. Block bulk import.
- **R9 accidental activation:** the seven-step legacy procedure is treated as current without the missing `kn.proc` source file. Gate on file presence.

### Acceptance tests retained from the blueprints

1. A file under 50 chars reaches the stub proposal path.
2. Duplicate overlap 0.96 reaches near-identical removal proposal logic.
3. Duplicate overlap 0.90 reaches ambiguous merge/remove handling.
4. A REMOVE candidate with inbound references blocks until explicit acknowledgment.
5. Integrated mode without checkpoint write-back hard-fails.
6. n8n order is delta scan → pending cleanup → folder cleanup → aggregate.
7. JSON bodies include `hours:24`, `days:14`, and `dry_run:false`.
8. HTTP nodes preserve the 60000/30000/30000 ms timeouts.
9. File maintenance inventory is sorted newest-first.
10. A score of 17 routes PROMOTE; a score of 10 routes HOLD.
11. 3-line and 400-line snippet candidates are filtered.
12. Same normalized code yields same 12-character hash.
13. P5 plan remains classified as DB batch, not file cleanup.
14. If `kn.proc` is absent, default automated behavior is R2, not R9.

---

## 11. Gaps and pointers

- Full SpecStory log: `C:\Users\rtoth\code\.specstory\history\2026-01-22_10-35Z-housekeeping-procedure-summary.md`; the in-folder excerpt is only lines 1-113.
- Related governance merge chat: `C:\Users\rtoth\code\.specstory\history\2026-02-11_19-05Z-bootstrap-and-todo-list-summary.md`; referenced by index but not copied.
- Duplicate staging copies may exist under `_staging\Utilix\...Automation\n8n\` and FormBuilder staging; index says these duplicate the canonical `_staging\Automation\n8n` copy.
- Utilix bootstraps may reference Cursor housekeeping decision records: `c:\code\_staging\Utilix\bootstrap\Utilix_260416-*.yaml`.
- Missing current-tree procedure: `c:\code\kv\30_Knowledge\Procedures\kn.proc.00.01.19_housekeep.md`.

---

## Source Retention Ledger

| Source | Non-redundant retention / status |
| ------ | -------------------------------- |
| `command.housekeeping.yaml` | Current Cursor command authority, Recycle Bin-only removal, second approval on reconsideration, full output/error/validation contract. |
| `personal-snippet.command.housekeeping.md` | Origin of the stale-search, cursory-review, first approval, deep-review, possible second-approval removal process; otherwise fully subsumed by `command.housekeeping.yaml`. |
| `housekeeping.yaml` | Superseded command model retained for thresholds, older action pipeline, and explicit conflict evidence around `_trash` / hard delete. |
| `proc-housekeep.json` | Runtime n8n endpoint, POST bodies, order, response shape, timeouts, and no encoded auth. |
| `kn.wkfl..._housekeep.md` | Operator scenarios, related workflows, retention / recursive cleanup narrative, and schedule context. |
| `kn.wkfl..._file-mant.md` | Newest-first invariant, concept gate, score bands, strategic directions, approval points, and route semantics. |
| `kn.wkfl..._snip-harv.md` | Harvest filters, language extraction methods, triage syntax, v3.1 auto-fill details, and slug naming side of the conflict. |
| `kn.wkfl..._snip-stor.md` | Hash identity, normalization algorithm, classification hints, template, index updates, and hash naming side of the conflict. |
| `00_INDEX_AND_SOURCES.md` | Corpus path map, missing `kn.proc` note, duplicate source pointers, and four-theme dispatch map. |
| `rtoth-code__specstory__housekeeping-procedure-summary_EXCERPT.md` | Historical seven-step procedure, schedules, old source path, and archive immutability rule. |
| `cursor_plans__housekeeping_system_completion_6c3bfff8.plan.md` | Pending xref / refs-updt / file-comp / module-relation roadmap; not current behavior. |
| `cursor_plans__housekeeping_batch_p5_9f85cc6d.plan.md` | DB / Access / SQLite homonym island and its completed batch procedure; not file cleanup. |
| `DISTILLED_mult-sess-blueprint_full.md` | R/Q/A/U registry names, metric bundles, failure modes, and acceptance-test ideas; deletion semantics corrected by current command authority. |
| `DISTILLED_mult-sess-blueprint_reduced.md` | Reduced tier framing, “wrong playbook” failure mode, compact uncertainty map, and 12-test subset; otherwise subsumed by the full blueprint. |
| `housekeeping_unified_corpus.md` | This merged dispatcher and conflict ledger; supersedes earlier content at this same path. |

---

## Quick lookup

| Need | Open |
| ---- | ---- |
| Cursor command authority, especially removal | `command.housekeeping.yaml` |
| Older command shape / superseded soft-delete history | `housekeeping.yaml` |
| n8n runtime path, bodies, timeouts, node order | `rtoth-code__va__ar__Automations__Workflows__proc-housekeep.json` |
| Human-readable janitor workflow | `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_housekeep.md` |
| Legacy / stale file triage | `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_file-mant.md` |
| Harvest code snippets | `c-code__staging__snip-harv__kn.wkfl.00.01.19_snip-harv.md` |
| Store and dedupe snippets | `c-code__staging__snip-stor__kn.wkfl.00.01.19_snip-stor.md` |
| Original source path map | `00_INDEX_AND_SOURCES.md` |
| Raw removal-flow prompt origin | `personal-snippet.command.housekeeping.md` |
| Legacy seven-step audit | `rtoth-code__specstory__housekeeping-procedure-summary_EXCERPT.md` |
| DB / Access / SQLite batch | `cursor_plans__housekeeping_batch_p5_9f85cc6d.plan.md` |
| Cross-reference roadmap | `cursor_plans__housekeeping_system_completion_6c3bfff8.plan.md` |
| Audit registry / Q primitives | `DISTILLED_mult-sess-blueprint_full.md` |
| Reduced uncertainty map | `DISTILLED_mult-sess-blueprint_reduced.md` |

---

## Self-check

- Every file in the folder is represented in provenance.
- Every source has a retained delta or explicit status in the Source Retention Ledger.
- No file is excluded.
- Duplicate facts are stated once in the strongest section.
- Lower-tier files add only deltas, conflicts, assumptions, tests, or historical context.
- Conflicts are explicit: removal semantics, n8n endpoint / auth / base-path prose vs JSON, legacy breadth vs janitor chain, snippet naming, DB homonym, and plan-vs-current status.
- The dispatch matrix gives one concrete authority path for each operational need.
- The full blueprint's metric/failure-mode deltas are retained without allowing it to override the newer command spec.
- Tier A wins wherever directions conflict.
