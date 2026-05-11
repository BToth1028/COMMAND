# Housekeeping `prev_doc` corpus — multi-session blueprint (reduced)

**Handshake:** `{"ack":"ready","agent":"mult-sess-blueprint","schema_mode":"reduced","metric_story":false,"version":1}`

**Step 0 governance:** Operator asked to apply distillation to this folder in one turn — **APPROVE** assumed for depth/length.

---

## ESTIMATED_SCOPE_AND_BUDGET (actualized)

| Item | Type | Size | Pre-tier |
|------|------|------|----------|
| D0 `00_INDEX_AND_SOURCES.md` | Corpus map | Short | Tier 2 |
| D1 `housekeeping.yaml` | Executable command spec | Large | Tier 1 |
| D2 `rtoth-code__specstory__..._EXCERPT.md` | Chat-derived 7-step summary | Short | Tier 2 |
| D3 `cursor_plans__housekeeping_batch_p5_...` | DB/Utilix batch plan | Medium | Tier 3 *for this theme* |
| D4 `cursor_plans__housekeeping_system_completion_...` | Cross-ref / workflow completion plan | Medium | Tier 2 |
| D5 `..._housekeep.md` | Workflow doc | Medium | Tier 1 |
| D6 `..._file-mant.md` | Workflow doc | Long | Tier 1 |
| D7 `..._snip-harv.md` | Workflow doc | Long | Tier 1 |
| D8 `..._snip-stor.md` | Workflow doc | Long | Tier 1 |
| D9 `proc-housekeep.json` | n8n orchestrator | Short | Tier 1 |

- **Dominant risk:** Homonym “housekeeping” (Cursor session hygiene vs. SQLite/audit “housekeeping batch” vs. automated repo cleanup); legacy **7-step** procedure vs current **3-module** n8n chain; **snippet filename** scheme drift between harvest vs storage docs.
- **Work shape:** Reduced mode — no metric/H/W/CE/VC enforcement layer; focus on scope, authority, traceability, tests.
- **Budget:** Block 1 medium; Block 2 medium (merge + U#); Block 3 compact; tests 8–12.

---

## BLOCK 1 — Per-document analysis

### A) Corpus index

| Id | File | Role |
|----|------|------|
| D0 | `00_INDEX_AND_SOURCES.md` | Provenance + theme map for harvest |
| D1 | `housekeeping.yaml` | Cursor `housekeeping` command — session-touched files |
| D2 | SpecStory excerpt | Historical summary of `kn.proc.00.01.19_housekeep` (7 steps) |
| D3 | `housekeeping_batch_p5` plan | Form-Builder DB maintenance (not file hygiene) |
| D4 | `housekeeping_system_completion` plan | Planned xref + `housekeep` formalization |
| D5 | `kn.wkfl.00.01.19_housekeep.md` | Workflow: delt-scan → pend-clnp → fldr-clnp |
| D6 | `kn.wkfl.00.01.19_file-mant.md` | Workflow: inventory → concept review → 4-axis grade → route |
| D7 | `kn.wkfl.00.01.19_snip-harv.md` | Harvest snippets via script + triage |
| D8 | `kn.wkfl.00.01.19_snip-stor.md` | Store snippets under `li/code/snippets/` |
| D9 | `proc-housekeep.json` | n8n: HTTP chain to mod endpoints |

### B) Claim tables (atomic, local to source)

**D0**

| Anchor | Claim |
|--------|--------|
| D0.C1 | This folder copies primary sources from `c:\code` / Cursor paths about file housekeeping and snippet flows. |
| D0.C2 | Theme map splits: automated `housekeep` + n8n; human `file-mant`; Cursor `housekeeping`; `snip-harv`/`snip-stor`. |
| D0.C3 | `kn.proc.00.01.19_housekeep.md` was not found under `c:\code` at index time; full SpecStory path cited. |
| D0.C4 | `housekeeping_batch_p5` is explicitly **DB/Utilix batch**, not general file cleanup. |

**D1**

| Anchor | Claim |
|--------|--------|
| D1.C1 | Command mission: review session-touched files; propose retain/relocate/rename/remove with **user approval**. |
| D1.C2 | Destructive or modifying actions require approval; PARA classification delegated to `para-ontology`; no guessing if unavailable. |
| D1.C3 | Check pipeline order: stub → duplicate overlap → inbound references → PARA → naming → location. |
| D1.C4 | Proposals: REMOVE (stub / near-duplicate), MERGE_OR_REMOVE, RELOCATE, RENAME, RELOCATE_AND_RENAME, KEEP_AS_IS. |
| D1.C5 | Soft delete default to `{workspace_root}/_trash/{session_id_or_timestamp}/`; hard delete requires explicit user election. |
| D1.C6 | REMOVE with inbound references requires explicit acknowledgment after presenting list. |
| D1.C7 | Integrated mode writes decisions via `bootstrap-checkpoint` and mutates `context_file_audit`; failure is HARD_FAILURE. |
| D1.C8 | Decision records must pass “zero context test” per skill rules. |

**D2**

| Anchor | Claim |
|--------|--------|
| D2.C1 | Legacy procedure purpose: periodic compliance + cleanup of pending deletions. |
| D2.C2 | Seven steps: delta compliance → project registry audit → spec/procedure validation → taxonomy validation → pending deletion cleanup (>14d in `ar\pend\`) → archive continuity → timestamp update. |
| D2.C3 | Schedules: daily quick (steps 1+5), weekly full (all 7), on-demand. |
| D2.C4 | Archives are not restructured; orphans/moves reported, archive paths preserved. |

**D3**

| Anchor | Claim |
|--------|--------|
| D3.C1 | Batch scope: link `tblAuditLog` in Access, fix `tblEdgeType.Cardinality` truncation, axioms doc frontmatter/trigger install, TODO/bootstrap updates, `phase3_audit` pre/post. |
| D3.C2 | Cardinality fix: `UPDATE` SQLite where value truncated; schema/reference table. |
| D3.C3 | Naming “housekeeping” here denotes **maintenance batch**, not Cursor command or n8n housekeep. |

**D4**

| Anchor | Claim |
|--------|--------|
| D4.C1 | Planned: `term-xref` reference sheet, `refs-updt` module, `file-comp` steps 0.5/1.5/4.5, formal `housekeep` workflow doc, module relation updates. |
| D4.C2 | Architecture: automated subgraph `housekeep → delt-scan → pend-clnp → fldr-clnp`; manual subgraph `file-mant` / `file-comp` with xref. |
| D4.C3 | Several deliverables still **pending** in plan frontmatter (snapshot at copy time). |

**D5**

| Anchor | Claim |
|--------|--------|
| D5.C1 | `housekeep` orchestrates: mod-delt-scan, mod-pend-clnp, mod-fldr-clnp, then aggregate results. |
| D5.C2 | Pend-clnp targets `ar\pend\{YYMMDD}\` with default retention 14 days. |
| D5.C3 | Fldr-clnp removes empty folders recursively under repo root. |
| D5.C4 | n8n path: webhook → three HTTP steps → aggregate JSON → respond. |
| D5.C5 | Related workflows: `file-mant`, `file-comp` (delta may feed compliance). |

**D6**

| Anchor | Claim |
|--------|--------|
| D6.C1 | **Newest-first** ordering for inventory, concept review, grading, and routing. |
| D6.C2 | Concept review filters invalid concepts before 4-axis grading. |
| D6.C3 | Axes: Quality, Effort, Relevance, Direction (1–5 each); matrix maps total to PROMOTE / REFINE / HOLD / ARCHIVE / DELETE. |
| D6.C4 | PROMOTE → `file-comp`; DELETE → archive then `tp/stag/`; ARCHIVE → archive workflow. |
| D6.C5 | Step 5 runs `mod-fldr-clnp`; final user approval via `mod-user-conf`. |

**D7**

| Anchor | Claim |
|--------|--------|
| D7.C1 | Phases: SCAN (harvester script) → TRIAGE → ENRICH (v3.1 frontmatter) → STORE. |
| D7.C2 | Noise filter: line bounds, test/private names, import-only, dup hash, etc. |
| D7.C3 | Store path pattern in Phase 4: `li/code/snippets/snip-{lang}-{slug}.md` plus language/pattern/master indexes. |

**D8**

| Anchor | Claim |
|--------|--------|
| D8.C1 | Library root `li/code/snippets/` with `index.md`, `by-language/`, `by-pattern/`. |
| D8.C2 | Dedup: normalize code, **MD5** first 12 hex, filename `snip-{hash}.md`. |
| D8.C3 | If hash exists, extend `related_sessions` rather than duplicate file. |
| D8.C4 | Six steps: dedup → classify → title → create file → update indexes → verify. |

**D9**

| Anchor | Claim |
|--------|--------|
| D9.C1 | Webhook POST `proc-housekeep` triggers sequential HTTP POSTs to `host.docker.internal:5070`. |
| D9.C2 | Bodies: delt-scan `hours:24`, pend-clnp `days:14, dry_run:false`, fldr-clnp `dry_run:false`. |
| D9.C3 | Code node aggregates prior three JSON outputs into `results`. |

### C) Irreducible cores (per document)

| Id | S0 (authority) | CWA (closed world) | Collapse intent | K0 (kernel) | Recursive notes | U# |
|----|----------------|--------------------|-----------------|-------------|-----------------|-----|
| D0 | Index author | Files listed are the corpus; external SpecStory paths are pointers | Maps four housekeeping themes | D0.C2–C4 | N/A | — |
| D1 | User + workspace FS + PARA skill | Session scope or explicit list; no bootstrap finalize here | One proposal per file; enum actions | D1.C1–C8 | Integrated vs standalone branches | — |
| D2 | `kn.proc` doc (not in repo) | Seven steps + schedules + archive rule | Compress chat to procedure table | D2.C1–C4 | Triggers/schedules imply automation not fully in D5/D9 | **U#1** vs D5/D9 |
| D3 | Form-Builder SQLite + Access + audit scripts | tbl/schema names as cited | Batch is orthogonal to file workflows | D3.C1–C3 | — | **U#2** naming collision with “housekeeping” |
| D4 | Plan author | Deliverables set pending/partial | Merge xref into `file-comp` | D4.C1–D4.C2 | Depends on files not all present in corpus | — |
| D5 | Workflow doc + module contracts | Three modules only | Same as D9 order | D5.C1–C5 | “Optional pass to file-comp” is conditional | — |
| D6 | Workflow doc + grading module | Newest-first invariant | Score → discrete route | D6.C1–C5 | Archive before delete staging | — |
| D7 | Harvester + v3.1 spec ref | Languages/extensions in table | Candidate → approved snippet | D7.C1–C3 | Feeds D8 | — |
| D8 | Library layout + template | Hash-based identity for stored files | Dedup before new file | D8.C1–D8.C4 | Consumes D7 output | **U#3** filename scheme vs D7 |
| D9 | n8n export | Three endpoints, fixed JSON | Same chain as D5 | D9.C1–C3 | Docker host wiring | — |

**U#1 Active uncertainty — legacy 7-step vs current 3-step automated housekeeping**

- **Conflict:** D2 describes a broad compliance/registry/taxonomy/archive audit procedure; D5/D9 describe delta scan + pending cleanup + empty folders only.
- **Candidates:** “Full kn.proc housekeeping” [D2.C1–C2] vs “Minimal mod-chain housekeeping” [D5.C1, D9.C1].
- **Status:** Active — corpus states D2’s source file missing under `c:\code`; D0 marks D2 as historical/SpecStory.
- **Resolution test:** If `kn.proc.00.01.19_housekeep.md` is absent, treat D2 as **historical reference**; operational default for “automated housekeeping” in this repo is D5/D9 unless operator restores/imports kn.proc.

**U#2 Active uncertainty — word “housekeeping”**

- **Conflict:** D1 (Cursor command), D3 (DB batch), D5/D9 (repo janitor) share a natural-language label.
- **Candidates:** Session file hygiene [D1.C1], database maintenance batch [D3.C3], n8n cleanup procedure [D5.C1].
- **Resolution test:** Disambiguate by **artifact**: `housekeeping.yaml` vs `proc-housekeep.json` / `kn.wkfl..._housekeep` vs Access/SQLite work items.

**U#3 Active uncertainty — snippet file naming**

- **Conflict:** D7 Phase 4 uses `snip-{lang}-{slug}.md` [D7.C3]; D8 uses `snip-{hash}.md` [D8.C2].
- **Candidates:** Slug naming [D7] vs hash naming [D8].
- **Resolution test:** Pick one canonical pattern per library version; until then, automation must not assume both names collide with the same snippet identity.

### D) Tier scoring (/20, dimension 5 N/A)

| Doc | Det | Collapse | Root | Kernel | Total | Tier |
|-----|-----|----------|------|--------|-------|------|
| D0 | 4 | 4 | 4 | 3 | 15 | T2 |
| D1 | 5 | 5 | 5 | 5 | 20 | T1 |
| D2 | 3 | 3 | 3 | 3 | 12 | T2 |
| D3 | 4 | 2 | 2 | 2 | 10 | T3 |
| D4 | 4 | 4 | 4 | 4 | 16 | T2 |
| D5 | 5 | 5 | 5 | 5 | 20 | T1 |
| D6 | 5 | 5 | 5 | 5 | 20 | T1 |
| D7 | 5 | 4 | 5 | 5 | 19 | T1 |
| D8 | 5 | 4 | 4 | 5 | 18 | T1 |
| D9 | 5 | 5 | 5 | 5 | 20 | T1 |

---

## BLOCK 2 — Cross-document canonicalization

### A) Registry (canonical name → definition → anchors)

| Name | One-line definition | Anchors |
|------|---------------------|---------|
| R1 Session file hygiene | Enumerate session-touched files; PARA placement; approve before move/remove | D1.C1–C8 |
| R2 Automated repo housekeeping | delt-scan → pend-clnp → fldr-clnp; aggregate report | D5.C1, D9.C1–C3 |
| R3 Pending deletion retention | Delete staged pending folders older than threshold days | D5.C2, D2.C2 (step 5 subset), D9.C2 |
| R4 Empty folder cleanup | Recursive removal of empty directories | D5.C3, D9.C2 |
| R5 Human file maintenance | Newest-first inventory; concept review; 4-axis grade; route | D6.C1–C5 |
| R6 Grading routing | Score bands map to PROMOTE/REFINE/HOLD/ARCHIVE/DELETE | D6.C3–C4 |
| R7 Snippet harvest | Script scan + filters + user triage + v3.1 enrich | D7.C1–C3 |
| R8 Snippet storage | Dedup by normalized hash; indexes; template file | D8.C1–C4 |
| R9 Legacy full housekeeping audit | Seven-step compliance/registry/taxonomy/archive procedure | D2.C1–C4 |
| R10 Cross-ref maintenance batch | DB/Access/axioms/trigger work under “housekeeping batch” label | D3.C1–C3, D0.C4 |
| R11 Xref system (planned) | term-xref + refs-updt + file-comp steps | D4.C1–C3 |

### B) Alias map

- **R2** aliases: “proc-housekeep”, “kn.wkfl.00.01.19_housekeep”, n8n chain [D5, D9].
- **R1** aliases: Cursor command `housekeeping` [D1].
- **R10** aliases: “Housekeeping batch P5”, Utilix/Form-Builder cleanup [D3, D0.C4].

### C) Equivalence classes

- **EC1** Automated chain identity: D5 module sequence ≡ D9 HTTP sequence (representative: R2).
- **EC2** Pending cleanup policy: D5 default 14 days; D2 step 5 cites `ar\pend\` >14d — align as same policy intent (representative: R3) pending path parity check (representative path D5 `ar\pend\{YYMMDD}\` vs D2 `ar\pend\`).

### D) U# (from Block 1, consolidated)

| Id | Conflict | Test / gate |
|----|----------|-------------|
| U#1 | R9 vs R2 breadth | Presence of `kn.proc...` in workspace; if absent, R9 non-operational |
| U#2 | “Housekeeping” label | Disambiguate by artifact id (yaml/json/wkfl/plan) |
| U#3 | R7 slug filenames vs R8 hash filenames | Single library naming standard + migration rule |

### E) Hidden assumptions (A#)

| Id | Assumption | Depends on |
|----|------------|------------|
| A#1 | `para-ontology` available for Cursor housekeeping | D1.C2 |
| A#2 | HTTP services at `host.docker.internal:5070` implement modules | D9.C1 |
| A#3 | v3.1 snippet spec is authoritative for harvest enrich | D7.C1 |
| A#4 | Legacy SpecStory procedure matches lost `kn.proc` file | D2, D0.C3 |

---

## BLOCK 3 — Enforcement blueprint (reduced)

### 1) Scope + CWA

**In scope:** Four distinct capabilities — (R1) Cursor session housekeeping, (R2–R4) automated janitor, (R5–R6) human triage maintenance, (R7–R8) snippet lifecycle. **R10** is explicitly a different domain (DB batch). **R9** is historical unless source procedure file returns.

**CWA:** No single “housekeeping” predicate covers all documents; closed world is **{R1..R11}** with R9/R10/R11 marked conditional on external artifacts.

### 2) Authority topology

- **R1:** User approval > PARA skill > workspace FS (D1 authority block).
- **R2–R4:** Workflow doc + n8n export + module HTTP contracts (D5, D9).
- **R5–R6:** Workflow doc + grading module; user approval at routing (D6).
- **R7–R8:** Workflow docs + on-disk library layout; user triage (D7–D8).

### 3) Collapse

- Treat **EC1** as one operational story for automation.
- Do not merge **R1** with **R2** (different triggers, approval models).
- Keep **R10** isolated from file-hygiene registry.

### 4) K0

- **No destructive filesystem change without explicit human approval** (R1, D6 routes).
- **Newest-first** is invariant for R5 inventory/review (D6.C1).
- **Soft delete default** for R1 unless hard explicitly chosen (D1.C5).

### 5) Recursive safety

- R1 REMOVE with inbound refs: block until acknowledgment (D1.C6).
- R6 DELETE: archive before `tp/stag/` (D6.C4).
- R8: dedup prevents silent duplicate files (D8.C2–C3).

### 6) Quantitative

OOS — `metric_story: false`.

### 7) Failure modes

| Mode | Detection | Mitigation |
|------|-----------|------------|
| Wrong playbook | User says “housekeeping” without context | Apply U#2 disambiguation |
| Silent hard delete | Missing user election | Revert to soft; re-prompt (D1) |
| PARA unavailable | Skill error | Halt classification; no guessing (D1) |
| Broken n8n chain | HTTP non-200 | Abort run; do not assume cleanup done (D9) |
| Snippet identity drift | Mixed slug/hash files | Halt bulk import until U#3 resolved |

### 8) Acceptance tests (minimal)

1. **T1:** Given stub file `<threshold` chars, R1 proposes REMOVE with factual justification [D1.C3–C4].
2. **T2:** Given duplicate overlap ≥0.95, R1 proposes REMOVE (near-identical) [D1.C4].
3. **T3:** Given REMOVE with inbound refs, R1 blocks until user acknowledges list [D1.C6].
4. **T4:** Integrated mode: decision emitted ⇒ checkpoint invoked OR HARD_FAILURE [D1.C7].
5. **T5:** R2 order: delt-scan before pend-clnp before fldr-clnp [D5.C1, D9 connections].
6. **T6:** Pend-clnp JSON includes `days: 14` and `dry_run: false` in recorded export [D9.C2].
7. **T7:** R5 listing sort = LastWriteTime descending [D6.C1].
8. **T8:** Score 16–20 ⇒ route PROMOTE to file-comp [D6.C3–C4].
9. **T9:** R7 noise filter excludes `<5` lines and `test_*` names [D7.C2].
10. **T10:** R8 normalize+hash matches D8 algorithm before create [D8.C2].
11. **T11:** Corpus index D0 correctly labels P5 plan as DB batch not file cleanup [D0.C4, D3.C3].
12. **T12:** When `kn.proc` missing, operator docs default automated story to D5/D9 not D2 [U#1 test].

### Appendix A — U#

See Block 2 section D.

### Appendix B — A#

See Block 2 section E.

### Appendix C — Traceability map

| Registry | Primary docs |
|----------|--------------|
| R1 | D1 |
| R2–R4 | D5, D9 |
| R5–R6 | D6 |
| R7–R8 | D7, D8 |
| R9 | D2 |
| R10 | D3 |
| R11 | D4 |

---

`BUDGET_ACTUALS:{"est":"medium pipeline","actual":"single file; tests=12; sections=full reduced blueprint","drift_reason":"operator single-turn approve; U# surfaced for legacy and naming"}`
