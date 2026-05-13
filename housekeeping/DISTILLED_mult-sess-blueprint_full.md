# Housekeeping `prev_doc` corpus — multi-session blueprint (full)

**Handshake:** `{"ack":"ready","agent":"mult-sess-blueprint","schema_mode":"full","metric_story":true,"version":1}`

**Step 0 governance:** Operator requested **full** mode in-thread — **APPROVE** for Blocks 1–3 in one delivery; budget expanded for metric registry and section 6.

---

## ESTIMATED_SCOPE_AND_BUDGET (actualized)

| Item | Type | Size | Pre-tier |
|------|------|------|----------|
| D0 `00_INDEX_AND_SOURCES.md` | Corpus map | Short | T2 |
| D1 `housekeeping.yaml` | Command spec | Large | T1 |
| D2 `..._EXCERPT.md` | Legacy 7-step summary | Short | T2 |
| D3 `housekeeping_batch_p5` | DB batch plan | Medium | T3 *theme* |
| D4 `housekeeping_system_completion` | Xref / completion plan | Medium | T2 |
| D5 `..._housekeep.md` | Workflow | Medium | T1 |
| D6 `..._file-mant.md` | Workflow | Long | T1 |
| D7 `..._snip-harv.md` | Workflow | Long | T1 |
| D8 `..._snip-stor.md` | Workflow | Long | T1 |
| D9 `proc-housekeep.json` | n8n JSON | Short | T1 |

- **Dominant risk:** Homonym “housekeeping”; legacy **R9** vs **R2** automation breadth; **U#3** snippet identity (slug vs hash).
- **Quantitative surface:** Rich in D1, D5–D9 (thresholds, timeouts, score bands, line bounds); thin in D0/D4; D3 DB-numeric; D2 schedule/step counts.
- **Work shape:** Full pipeline — Block 1 `/25`, Block 2 quantitative candidates + H/W/CE/VC-relevant A#, Block 3 section 6 populated from corpus (not invented physics).
- **Budget:** Block 1 large tables; Block 2 registry + **Q*** metric rows; Block 3 full sections; tests **16** (within 8–20 default).

---

## BLOCK 1 — Per-document analysis

### A) Corpus index

| Id | File | Role |
|----|------|------|
| D0 | `00_INDEX_AND_SOURCES.md` | Provenance + theme map |
| D1 | `housekeeping.yaml` | Cursor `housekeeping` command |
| D2 | SpecStory excerpt | Historical `kn.proc` 7-step |
| D3 | `housekeeping_batch_p5` | Form-Builder / SQLite batch |
| D4 | `housekeeping_system_completion` | Planned xref + housekeep doc |
| D5 | `kn.wkfl.00.01.19_housekeep.md` | Automated janitor workflow |
| D6 | `kn.wkfl.00.01.19_file-mant.md` | Human maintenance workflow |
| D7 | `kn.wkfl.00.01.19_snip-harv.md` | Snippet harvest |
| D8 | `kn.wkfl.00.01.19_snip-stor.md` | Snippet storage |
| D9 | `proc-housekeep.json` | n8n orchestration |

### B) Claim tables (atomic)

**D0** — D0.C1 corpus copy scope; D0.C2 four themes; D0.C3 `kn.proc` not under `c:\code`; D0.C4 P5 is DB batch not file cleanup.

**D1** — D1.C1 session-touched review + approval; D1.C2 JDex delegation, no guess; D1.C3 pipeline stub→dup→refs→JDex→name→loc; D1.C4 proposal enum; D1.C5 soft `_trash` default; D1.C6 REMOVE+refs ack; D1.C7 integrated checkpoint HARD_FAILURE; D1.C8 zero-context rationale; D1.C9 numeric: stub_threshold 50, duplicate 0.85/0.95, gates.

**D2** — D2.C1 periodic compliance + pending cleanup; D2.C2 seven named steps; D2.C3 daily vs weekly schedules; D2.C4 archive immutability rule; D2.C5 numeric: `>14` days pending.

**D3** — D3.C1 Access/SQLite/audit/trigger scope; D3.C2 cardinality UPDATE; D3.C3 naming disambiguation “housekeeping batch”.

**D4** — D4.C1 deliverables list; D4.C2 architecture subgraphs; D4.C3 pending todos in snapshot.

**D5** — D5.C1 three modules + aggregate; D5.C2 `ar\pend\{YYMMDD}\`, retention **14** days; D5.C3 recursive empty-folder pass; D5.C4 n8n webhook; D5.C5 optional file-comp feed.

**D6** — D6.C1 newest-first invariant; D6.C2 concept review gate; D6.C3 four axes **1–5**; D6.C4 bands **16–20 / 12–15 / 8–11 / 4–7 / 1–3**; D6.C5 routes; D6.C6 fldr-clnp + user-conf.

**D7** — D7.C1 scan→triage→enrich→store; D7.C2 noise: **<5** lines, **>300** lines, test_*, etc.; D7.C3 store `snip-{lang}-{slug}.md`.

**D8** — D8.C1 library tree; D8.C2 MD5(normalized)[:**12**]; D8.C3 related_sessions merge; D8.C4 complexity **≤10 / 11–50 / >50** lines.

**D9** — D9.C1 webhook `proc-housekeep`; D9.C2 `hours:24`, `days:14`, timeouts **60000** / **30000**; D9.C3 aggregate JSON.

### C) Irreducible cores

| Id | S0 | CWA | Collapse | K0 | Recursive | Quant (dim 5 feed) | U# |
|----|-----|-----|----------|----|-----------|---------------------|-----|
| D0 | Index | Listed files only | Theme map | D0.C2 | External pointers | Low — meta inventory | — |
| D1 | User+FS+JDex | Session/explicit list | One action/file | Approval+refs+soft default | Integrated bootstrap | **High** — thresholds, enums | — |
| D2 | Lost kn.proc | 7 steps + schedules | Table vs narrative | Archive rule | Automation implied | **Med** — 14d, step IDs | U#1 |
| D3 | DB artifacts | Schema names | Batch ≠ file hygiene | Audit triggers | phase scripts | **Med** — SQL row fixes | U#2 |
| D4 | Plan author | Pending set | Xref injection | Modular graph | file-comp deps | Low–Med | — |
| D5 | Wkfl+n8n | 3 modules | = D9 chain | Retention+recursion | Optional file-comp | **High** — counts JSON | — |
| D6 | Wkfl+grad | Newest-first | Score→route | User approvals | Archive before delete | **High** — 4×5 matrix | — |
| D7 | Script+v3.1 | Lang table | Phase gates | User triage | Indexes | **High** — bounds | — |
| D8 | Library+hash | snip-{hash} | Dedup | Indexes | Session context | **High** — MD5, tiers | U#3 |
| D9 | n8n export | 3 POST bodies | = D5 | Timeouts+dry_run | Docker host | **High** — ms, hours | — |

### D) Signal scoring (dimensions 1–5, total /25)

Dimensions: (1) Determinism (2) Collapse Value (3) Root Integrity (4) Kernel Relevance (5) **Quantitative Control**

| Doc | 1 | 2 | 3 | 4 | 5 | Σ | Tier |
|-----|---|---|---|---|---|-----|------|
| D0 | 4 | 4 | 4 | 3 | 3 | 18 | T1 |
| D1 | 5 | 5 | 5 | 5 | 5 | 25 | T1 |
| D2 | 4 | 4 | 4 | 4 | 4 | 20 | T1 |
| D3 | 4 | 3 | 4 | 4 | 4 | 19 | T1 |
| D4 | 4 | 4 | 4 | 4 | 2 | 18 | T1 |
| D5 | 5 | 5 | 5 | 5 | 5 | 25 | T1 |
| D6 | 5 | 5 | 5 | 5 | 5 | 25 | T1 |
| D7 | 5 | 4 | 5 | 5 | 5 | 24 | T1 |
| D8 | 5 | 4 | 4 | 5 | 5 | 23 | T1 |
| D9 | 5 | 5 | 5 | 5 | 5 | 25 | T1 |

**Tier cuts (metric_story true):** Tier1 ≥18, Tier2 12–17, Tier3 ≤11 — all documents **Tier1** in this harvest.

### E) Required Block 1 outputs — C) condensed claim anchors for traceability

Irreducible quantitative atoms (for Block 2 **Q** registry):

- [D1.C9] `stub_threshold_chars=50`, `duplicate_overlap_threshold=0.85`, near-identical REMOVE at `≥0.95`, MERGE_OR_REMOVE between 0.85–0.95 (ambiguous band in error_policy).
- [D5.C2,D9.C2] `retention_days=14`, `hours=24` (delt window in n8n).
- [D9.C2] HTTP timeouts 60000 ms (scan), 30000 ms (pend, fldr).
- [D6.C3,C4] axis range 1–5; band thresholds 16, 15, 11, 7, 3 boundaries.
- [D7.C2] `min_lines=5`, `max_lines=300` (defaults stated).
- [D8.C2,C4] MD5 hex length 12; complexity line bands.

---

## BLOCK 2 — Cross-document canonicalization

### A) Registry — structural (R*) — unchanged semantics from reduced run

| Name | Definition | Anchors |
|------|------------|---------|
| R1 | Session file hygiene (Cursor command) | D1 |
| R2 | Automated repo housekeeping (3 modules) | D5,D9 |
| R3 | Pending deletion retention | D5,D2,D9 |
| R4 | Empty folder cleanup | D5,D9 |
| R5 | Human file maintenance | D6 |
| R6 | Grading routing | D6 |
| R7 | Snippet harvest | D7 |
| R8 | Snippet storage | D8 |
| R9 | Legacy full housekeeping audit | D2 |
| R10 | DB maintenance batch (homonym) | D3,D0 |
| R11 | Planned xref system | D4 |

### B) Registry — quantitative primitives (**Q***)

| Id | Name | Type | Value / formula | Unit | Source |
|----|------|------|-----------------|------|--------|
| Q1 | stub_threshold_chars | threshold | 50 | chars | D1 |
| Q2 | duplicate_overlap_lo | threshold | 0.85 | unit interval | D1 |
| Q3 | duplicate_overlap_merge | threshold | 0.95 | unit interval | D1 |
| Q4 | retention_days_pend | policy | 14 | days | D5,D9,D2 |
| Q5 | delt_scan_hours | policy | 24 | hours | D9 |
| Q6 | timeout_delt_scan_ms | SLO | 60000 | ms | D9 |
| Q7 | timeout_pend_clnp_ms | SLO | 30000 | ms | D9 |
| Q8 | timeout_fldr_clnp_ms | SLO | 30000 | ms | D9 |
| Q9 | axis_min_score | domain | 1 | dimensionless | D6 |
| Q10 | axis_max_score | domain | 5 | dimensionless | D6 |
| Q11 | promote_floor | band | 16 | sum of 4 axes | D6 |
| Q12 | refine_floor | band | 12 | sum | D6 |
| Q13 | hold_floor | band | 8 | sum | D6 |
| Q14 | archive_floor | band | 4 | sum | D6 |
| Q15 | delete_ceiling | band | 3 | sum | D6 |
| Q16 | snip_min_lines | threshold | 5 | lines | D7 |
| Q17 | snip_max_lines | threshold | 300 | lines | D7 |
| Q18 | snippet_hash_len | format | 12 | hex chars | D8 |
| Q19 | complexity_simple_max_lines | band | 10 | lines | D8 |
| Q20 | complexity_moderate_max_lines | band | 50 | lines | D8 |

### C) Alias map

- R2 ≡ `proc-housekeep` ≡ `kn.wkfl.00.01.19_housekeep` [D5,D9].
- R10 ≡ “Housekeeping batch P5” [D3,D0.C4].
- Q4 ties **EC2** (pend policy) across D2 step 5, D5, D9.

### D) Equivalence classes

- **EC1:** R2 operational identity: D5 todo list ≡ D9 node graph (representative **R2**).
- **EC2:** Pending retention **14 days** [Q4]: D5 prose, D9 JSON, D2 step 5 — representative **Q4**.

### E) U#

| Id | Conflict | Anchors | Resolution test |
|----|----------|---------|-----------------|
| U#1 | R9 breadth vs R2 | D2 vs D5/D9 | `kn.proc` file presence in workspace |
| U#2 | “Housekeeping” label | D1,D3,D5 | Artifact-id routing (yaml/json/wkfl/sql) |
| U#3 | Snippet filename schemes | D7.C3 vs D8.C2 | Single canonical pattern in library spec |

### F) A# (including H/W/CE/VC-relevant)

| Id | Assumption | Depends |
|----|------------|---------|
| A#1 | JDex skill callable | D1 |
| A#2 | Module HTTP API matches JSON bodies | D9 |
| A#3 | v3.1 snippet schema stable | D7 |
| A#4 | SpecStory matches missing kn.proc | D2,D0 |
| A#5 | **H:** Pend folders older than Q4 are safe to delete when `dry_run:false` | D9,D5 |
| A#6 | **W:** n8n timeouts bound worst-case module runtime | D9 |
| A#7 | **CE:** Q2–Q3 faithfully separate ambiguous vs merge duplicates | D1 |
| A#8 | **VC:** Axis sums map to correct routes without off-by-one | D6 |

---

## BLOCK 3 — Closed-ended enforcement blueprint (full)

### (1) Scope + CWA

**Scope:** Governed objects are workflows and command specs for **R1–R8**, plus explicit exclusion/classification of **R9** (conditional), **R10** (orthogonal batch), **R11** (planned).

**CWA:** Predicate `Housekeeping(x)` is **not** a single sort; `x` must be one of `{cursor_session_hygiene, repo_janitor, file_maint, snip_harv, snip_stor, legacy_kn_proc, db_batch, xref_plan}`.

### (2) Authority topology

- **R1:** User > JDex > FS; validators in D1 `validation_gates` and `error_policy`.
- **R2/R3/R4:** Module contracts implied by D5; transport authority D9.
- **R5/R6:** User approval nodes; grading module authority for scores.
- **R7/R8:** User triage + library layout; script authority for scan only.

### (3) Collapse

- **EC1:** Single automation story under R2; D9 is executable projection of D5.
- **EC2:** Single retention constant **Q4** unless operator ADJUSTs D9 JSON and D5 doc together.
- No merge of R1 with R2 (approval topology differs).

### (4) K0

- No mutation without approval (R1, R5).
- Soft delete default (R1).
- Newest-first for R5 listing.
- Dedup-by-hash before new snippet file (R8).

### (5) Recursive safety

- REMOVE: reference scan + ack (R1).
- DELETE route: archive then staging (R6).
- Integrated mode: checkpoint or HARD_FAILURE (R1).

### (6) Quantitative — H / W / CE / VC

*Note: The distillation prompt kit names **H/W/CE/VC** without expanding the acronym in-repo. Below, each letter names a **metric bundle** whose indicators are **only** what the corpus states; monitoring hooks tie to existing artifacts.*

#### H — Hygiene throughput (automated janitor)

| Metric | Definition | Measurement | Threshold / SLO | Monitor |
|--------|------------|-------------|-------------------|--------|
| H1 Modified file signal | Count of files changed in delt window | `delta_scan.modified_files_count` (D5 example JSON) | Report-only unless paired with compliance job | Each R2 run |
| H2 Pending volume | Folders deleted vs retained | `deleted_count`, `kept_count` (D5) | Policy: age governed by **Q4** | R2 step 2 |
| H3 Empty-folder debt | Directories removed | `removed_count` (D5) | Non-negative integer | R2 step 3 |
| H4 Pend age compliance | Staging older than Q4 | Filesystem age vs **Q4** | Violation if `age_days > Q4` when cleanup enabled | R3 |

#### W — Workflow load & latency

| Metric | Definition | Measurement | Threshold / SLO | Monitor |
|--------|------------|-------------|-------------------|--------|
| W1 R1 throughput | Files reviewed | `files_reviewed`, `proposals_total` (D1 output_contract) | Session budget operator-defined | Each R1 close |
| W2 Scan latency bound | HTTP completion | Wall clock vs **Q6** | Fail if exceeds Q6 | n8n / client |
| W3 Pend latency bound | HTTP completion | vs **Q7** | Fail if exceeds Q7 | n8n |
| W4 Fldr latency bound | HTTP completion | vs **Q8** | Fail if exceeds Q8 | n8n |

#### CE — Control thresholds (rules-as-numbers)

| Metric | Definition | Measurement | Threshold | Monitor |
|--------|------------|-------------|-----------|--------|
| CE1 Stub gate | Char count vs Q1 | `measure_content_size` (D1) | `< Q1` ⇒ stub path | R1 check a |
| CE2 Duplicate ambiguity | Overlap ∈ (Q2,Q3) | `overlap_score` (D1) | Escalate AMBIGUOUS_DUPLICATE | R1 check b |
| CE3 Duplicate merge | Overlap ≥ Q3 | same | REMOVE near-identical proposal | R1 |
| CE4 Snip size gate | Line count | Harvester filter (D7) | Outside [Q16,Q17] ⇒ skip | R7 |
| CE5 Delt window | Lookback | POST body (D9) | Must match deployed policy (**Q5**) | Config audit |

#### VC — Value coverage (human grading & library quality)

| Metric | Definition | Measurement | Scale | Monitor |
|--------|------------|-------------|-------|--------|
| VC1 Axis coverage | Each file receives 4 scores | Grading record | Q9–Q10 per axis | R6 |
| VC2 Route correctness | Sum maps to band | `Σ axes` vs Q11–Q15 | Discrete 5 outcomes | R6 QA |
| VC3 Snippet dedup integrity | Hash collision handling | MD5[:Q18] (D8) | Exists ⇒ update context | R8 |
| VC4 Complexity class | Line count tier | Q19–Q20 rules (D8) | 3 bins | R8 metadata |

**Enforcement posture:** H/W/CE/VC rows are **operational SLOs and gates** where the corpus already defines numbers; they are **not** extended with unstated business KPIs.

### (7) Failure modes

| Mode | Detection | Mitigation |
|------|-----------|------------|
| Threshold drift | D9 JSON changed without D5/D1 doc update | Version Q* triples together |
| Timeout silent pass | HTTP 200 with partial body | Schema-validate module responses |
| Band mis-route | Σ axes 16 routed to HOLD | Automated matrix test VC2 |
| U#3 violation | Two filename patterns in one library | Block bulk import; normalize spec |
| R9 activated without kn.proc | User expects 7-step | U#1 gate |

### (8) Acceptance tests (16)

1. **T1:** CE1 — file 40 chars ⇒ stub proposal path [D1, Q1].
2. **T2:** CE3 — overlap 0.96 ⇒ REMOVE near-identical [D1, Q3].
3. **T3:** CE2 — overlap 0.90 ⇒ MERGE_OR_REMOVE or ambiguous policy [D1, Q2–Q3].
4. **T4:** R1 REMOVE + inbound refs ⇒ blocked without ack [D1.C6].
5. **T5:** Integrated mode missing checkpoint ⇒ HARD_FAILURE [D1.C7].
6. **T6:** R2 order delt → pend → fldr [D5,D9, EC1].
7. **T7:** D9 body `days:14`, `hours:24`, `dry_run:false` [Q4,Q5].
8. **T8:** Q6–Q8 present on HTTP nodes [D9].
9. **T9:** Newest-first sort invariant on inventory [D6.C1].
10. **T10:** Σ=17 ⇒ PROMOTE [Q11, D6].
11. **T11:** Σ=10 ⇒ HOLD [Q13–Q14].
12. **T12:** CE4 — 3-line candidate filtered [Q16, D7].
13. **T13:** CE4 — 400-line candidate filtered [Q17, D7].
14. **T14:** VC3 — same normalized code ⇒ same hash[:Q18] [D8].
15. **T15:** D0 labels P5 as DB batch [D0.C4, R10].
16. **T16:** U#1 — if kn.proc absent, default ops doc is R2 not R9 [D0.C3].

### Appendix A — U#

Block 2 section E.

### Appendix B — A#

Block 2 section F.

### Appendix C — Traceability map

| Artifact | Primary |
|----------|---------|
| R1 | D1 |
| R2–R4 | D5,D9 |
| R5–R6 | D6 |
| R7 | D7 |
| R8 | D8 |
| R9 | D2 |
| R10 | D3 |
| R11 | D4 |
| Q1–Q20 | D1,D5,D6,D7,D8,D9,D2 |

### Appendix D — Sections A–G mapping (full schema_mode)

For automation that expects **A–G** labels: **A** Scope/CWA §1; **B** Authority §2; **C** Collapse §3; **D** K0 §4; **E** Recursive safety §5; **F** Quantitative/HWCEVC §6; **G** U# consolidated §Appendix A + Block 2 E.

---

`BUDGET_ACTUALS:{"est":"expanded full+metrics","actual":"1 file; Q-rows=20; tests=16; HWCEVC=4 tables","drift_reason":"corpus is playbook-heavy; H/W/CE/VC expanded as metric bundles tied to Q* only"}`
