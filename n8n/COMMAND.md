# n8n — unified reference (staging automation corpus)

**Corpus root:** `C:\code\_staging\Automation\n8n`  
**Unified output (this file):** `C:\Users\rtoth\.cursor\commands\n8n\n8n_unified_corpus.md`  
**Method:** `corpus-unify` (`c:\Users\rtoth\.cursor\skills-cursor\corpus-unify\SKILL.md`) — overlap folded once; unique facts retained per source; conflicts explicit. **Extended pass:** structured research procedure from `C:\code\_staging\ai_research_playbook.yaml` (steps 2–7: tier-1 first, repo search, gaps) plus repo-local enumeration; **tier-1 n8n URL registry** inlined by reference to `n8n_research_playbook.yaml` below rather than pasted here (~500 URLs).

**What this file is:** A single dispatcher + operator reference across **local Docker MSSQL backups**, **Access/GDrive sidecar automation**, **documentation / KT / gap-analysis lineage**, and a **parallel CFP-intake architecture spec** that was authored for cloud deployment — not merged silently with runtime facts.

**What this file is not:** Verbatim paste of large specs (`kn.spec.*`, full workflow JSON); not a substitute for SQL under `\_PARA\libraries\code\sqlt` or secrets in `.env`.

## Automation default (command context)

Aligned with **`corpus-unify`** *Automation default*: when you analyze **this** corpus, `C:\code\_staging\Automation\n8n`, or anything referenced from it, **assume every repeated, cross-boundary, or trigger-like activity can be automated.** The productive question is **not** whether it *might* be automated, but **why it cannot** or **why it should not**.

- **Cannot** — defensible hard blocks: no machine interface, physical reality, unknowable inputs, cryptographic human step, explicit policy prohibition, etc.
- **Should not** — defensible restraint: risk, loss of determinism, compliance, economics, lawful accountability. Tie to a **source** in this corpus when one exists; otherwise label **`operator preference`** or **`hypothesis:`**.

Treat **manual or semi-manual** practice as **gap or chosen exception**, not a neutral default, until a barrier is stated. Full merge rules and inventory checks: `c:\Users\rtoth\.cursor\skills-cursor\corpus-unify\SKILL.md`.

---

## Provenance

| Source | Class | Role in this merge |
| ------ | ----- | ------------------ |
| `compose.yaml` | Executable stack | **Authority** for local n8n: image pin `n8nio/n8n:2.18.5`, `n8n-local`, binds `/scripts`, `/watch`, TZ, file-access allowlist, healthcheck, `host.docker.internal`. |
| `.env.example` | Config template | States n8n 2.x UI auth via User Management; `.env` empty template; `.env` not duplicated here. |
| `.gitignore` | Config | Ignores `.env`, `.env.local`, `.env.*.local`. |
| `mssql-backup.workflow.json` | Executable workflow | **Authority** for backup graph: triggers (schedule **02:00**, webhook **`mssql-backup-static`**, file drop **`/watch/*.trigger`**, manual), MSSQL credential name, SQL read path, JSONL append path logic. |
| `watch-folder-to-gdrive.workflow.json` | Executable workflow | Local file trigger → conditional branches → GX copy vs Access dump execution. |
| `link-db-to-watch.ps1` | Script | Hard-link (same volume) or symlink file into `_watch`; warns symlink may break reliable watcher semantics on Windows. |
| `dump-access-db.ps1` | Script | Headless Access COM dump using `DumpAccessDB_AR.bas`; outputs to `G:\My Drive\Utilix` naming `GX.{db}_dump_{yyMMdd-HHmmss}.zip`. |
| `kn.docg.07.08.19_kt-n8n.md` | KT pack | Sess-03 narrative: KT continuity via Drive watcher, filter, merge/validation; node-notes standardization; evidence E49–E51; next = chat evaluation tree. |
| `kn.docg.07.08.19_kt-n8n.yaml` | Mirror | YAML mirror of KT pack; substance subsumed by `.md`. |
| `kn.docg.07.08.19_todo-n8n.md` | Todo | sess-03 task list T15–T20 (Drive watcher … chat grading wiring). |
| `kn.docg.07.08.19_todo-n8n.yaml` | Mirror | Subsumed by paired `.md`. |
| `kn.docg.07.08.19_kt-n8n-wkfl-gap.md` | KT | **Founding sess-01** gap-analysis pack: STARTUP PROMPT, doc-audit-first scope, `kn.pmpt` vs project-KT ambiguity (T13-class blocker), successor steps (inventory → remediation → workflow JSON skeleton). |
| `kn.docg.07.08.19_kt-n8n-wkfl-gap.yaml` | Mirror | Subsumed by `.md`. |
| `kn.docg.07.08.19_todo-n8n-wkfl-gap.md` | Todo |_sess-01_ baseline todos T01–T13 with full evidence excerpt index E01–E29. |
| `kn.docg.07.08.19_todo-n8n-wkfl-gap.yaml` | Mirror | Subsumed by `.md`. |
| `kn.wkfl.00.01.19_housekeep.md` | Workflow doc | Housekeeping orchestrator: delta-scan → pend-clnp → fldr-clnp; triggers webhook + scheduled + manual; pend retention default **14 days** (`ar\pend\`). |
| `kn.wkfl.00.01.19_file-mant.md` | Workflow doc | File maintenance: **newest-first** invariant; grading/routing; **approval_required** semantics in governance vs automation. |
| `housekeep__963f2ae2-….md` | Snapshot export | Same housekeeping body as `kn.wkfl…housekeep`; adds taxonomy YAML frontmatter + `ARCHIVED_FIELD` comments referencing UUID-named module stubs **not present** in this folder — treat as portability snapshot only. |
| `file-mant__f6bab374-….md` | Snapshot export | Same pattern as above for file-mant. |
| `kn.spec.00.01.19_n8n-auto.md` | Full specification | **CFP intake / validation / Postgres / Slack / email / multi-route triggers** architecture (Webhook + Drive + Gmail). Large; summarized here + pointer. |
| `kn.proc.00.01.19_n8n-deploy.md` | Procedure | Stepwise **n8n Cloud + Postgres + OAuth** deployment for that CFP stack; contrasts with today’s Compose-local pattern. |
| `_ar/_from_worktree/S01_0302/manifest.json` | Session manifest | Inception: isolated-doc count (**7**), coverage gaps (**4**), **`startup_prompt`** for cross-reference remediation; cites `kv/20_Areas/Automations/kn.flow.03.03.19_cfp-intk-vald.json`. |
| `_ar/_from_worktree/S01_0302/re.rcvm.07.08.19_n8n.md` | CFP | Formal CFP framing: founding session, gaps E001–E015, **`kn.flow.03.03.19_cfp-intk-vald.json`** as existing asset **out-of-tree**. |
| `_ar/_from_worktree/S01_0302/re.rcvm.07.08.19_n8n.yaml` | Mirror | Subsumed. |
| `_ar/_from_worktree/S01_0302/op.schd.07.06.19_todo-n8n.md` | Todo | Scheduling/todo artifact for sess-01 (mirrors remediation tasks). |
| `_ar/_from_worktree/S01_0302/op.schd.07.06.19_todo-n8n.yaml` | Mirror | Subsumed. |
| `_ar/_from_worktree/S02_0634/*` | Worktree archive | **`cfp-*-wkfl-gap`** naming (CFP rebranding of gap KT/todo content); manifests — **near-duplicate** of root `kn.docg…*_wkfl-gap*`. |
| `_ar/_from_worktree/S03_0654/*` | Logic-tree todo | sess-02 **logic tree** todo: branching policy (**E49**), startup tree (**T10**); blocked on as-is vs target alignment (**T15**) before JSON build. |
| `_ar/_from_worktree/S04_0852/*` | Worktree archive | Later `cfp-n8n` / `todo-n8n` copies + manifest — **subset/duplicate** of root docg lineage. |

**Provenance — research-pass additions (outside staging `Automation\n8n` root)**

| Source | Class | Role in this merge |
| ------ | ----- | ------------------ |
| `C:\code\_staging\ai_research_playbook.yaml` | Reusable procedure | Generic **tier-1 authority > blogs**, search templates (`site:docs…`, GitHub paths), determinism caveats; methodology for this sweep. |
| `C:\Users\rtoth\.cursor\commands\research\n8n\playbook\n8n_research_playbook.yaml` | **Primary URL registry** | n8n-specific **tier_1 docs.n8n.io / hosting / LangChain / community / MCP patterns**, tier_2 awesome lists **`n8n-mcp`** (AI assistant tooling), tier_3 zeitgeist; **canonical pointer** — do not stale-copy full lists into this MD. |
| `C:\code\_staging\governance-rewrite\vocab-gov\n8n_research_playbook.yaml` | **Symlink** → Commands playbook | Same registry; **edit canonical only** (`…\commands\research\…`). Prior file: `n8n_research_playbook.yaml.260430-125814.pre_symlink_bak` in same folder. |
| `C:\code\_PARA\1_[P]roject\internal.n8n-integration\03_outputs\n8n_research_playbook.yaml` | **Symlink** → Commands playbook | Same; prior copy: `…03_outputs\n8n_research_playbook.yaml.260430-125805.pre_symlink_bak`. |
| `C:\code\_PARA\1_[P]roject\internal.n8n-integration\02_working\chat-sessions\bootstrap\internal.n8n-integration_260429-1137.yaml` | **Project bootstrap SoT** | Live integration narrative: Lazarus `\SQLEXPRESS`, **`n8n_backup`**, 4-trigger pipeline, JSONL audit; tasks **T-001** backup path migration to **`C:\Backups\SQL\Lazarus\SQLEXPRESS\...`**, substrate-test corpus (T-002), webhook/file-drop smoke (T-003/004). Differs from **current** `@backup_root` in SQL unless T-001 finished. |
| `C:\code\_staging\governance-rewrite\vocab-gov\kn.spec.00.01.19_n8n-auto.md` (and sibling `kn.*`, `re.rcvm.*`) | Corpus mirrors | Governance-rewrite copies of staging `Automation\n8n` docs — treat as **non-authoritative** unless governance process says otherwise. |
| `C:\code\_staging\BootstrapProtocol\02_working\chat-sessions\bootstrap\BootstrapProtocol_260429-0732.yaml` | Protocol backlog | Held work: **`n8n_260428-2115`** session-zero path `…/internal.n8n-integration/…/bootstrap/` (target may have moved — verify disk). |
| `C:\code\_PARA\1_[P]roject\cenhud.utilix\02_working\…` | Utilix artefacts | Bootstrap YAMLs (**Utilix_260430-0545** et al.), **phase-0-completion**, **milestones** tying **canonical backup** to n8n **`run_id`**, schedule health **T-103** track. |
| `C:\Users\rtoth\.cursor\commands\housekeeping\housekeeping_unified_corpus.md` | Related unified corpus | **`proc-housekeep`** JSON (**janitor graph**); conflict notes vs `kn.wkfl…housekeep`; paths into `_staging\Automation\n8n`. |
| `c:\code\.cursor\skills\corpus-unify\SKILL.md` | Cursor skill | Pattern: merge **n8n JSON + markdown** into one Automation section (config beats prose where they clash). |

**Exclusions**

| Path | Reason |
| ---- | ------ |
| `C:\code\_staging\Automation\n8n\.env` | Local secrets — never inlined in corpus. |

**Operational log path (not under corpus unify inventory but downstream of backup workflow):** JSONL summaries are produced under `\_staging\Automation\n8n\_watch\_log\` when the MSSQL workflow runs (referenced from implementation behavior; folder may exist at runtime).

**SQL authority (outside corpus root):** `C:\code\_PARA\libraries\code\sqlt\mssql-backup-with-guardrails.sql` defines `@backup_root`, GFS tiers, **`n8n_backup`** login assumptions — full text stays there.

---

## 1. Disambiguation (“n8n” overload)

1. **Local ops stack (`compose.yaml`):** Docker **n8n-local**, bind mounts **`/scripts`** (read-only sqlt) and **`/watch`** (RW file-drop sentinel), MSSQL reachable via **`host.docker.internal`**, pinned **n8n 2.18.5**, **User Management** for UI login (not `N8N_BASIC_AUTH_*` on 2.x default path).
2. **MSSQL backup workflow (`mssql-backup.workflow.json`):** Four triggers converge → read script from mounted path → **`microsoftSql`** node with credential **`Lazarus SQLEXPRESS — n8n_backup`** → summarize → append **JSONL** run record; schedule node labeled **Daily 02:00 ET**.
3. **Watch → GDrive workflow (`watch-folder-to-gdrive.workflow.json`):** Folder watcher feeding **IF** nodes; branches call **`executeCommand`** for GX vs Access paths — pairs with **`dump-access-db.ps1`** / links.
4. **CFP-intake automation (`kn.spec` + `kn.proc`):** Alternate **design plane** — webhook `/webhook/cfp-intake`, **Postgres** `cfp_log`, Slack+email notifications, **n8n Cloud** deployment story; **not** the Lazarus backup graph unless explicitly implemented.
5. **Documentation remediation / KT-CFP lineage (`kn.docg` + `_ar/_from_worktree`):** AI-to-AI handoff, taxonomy/frontmatter governance, isolated-doc remediation — **documentation process**, not executable backup behavior.
6. **Orchestration pattern docs (`kn.wkfl` housekeeping / file-mant):** Describe **human + n8n** cleanup and file-triage narratives used elsewhere (`proc-housekeep` in housekeeping corpus) — overlapping **word** housekeeping with Cursor command housekeeping; distinct systems.

---

## 2. Local runtime facts (Compose + MSSQL workflow)

**Compose highlights**

- Preserve existing **`n8n_data`** volume (**`external: true`**); migrate from ad-hoc `docker run` per header comments.
- **File access:** `N8N_RESTRICT_FILE_ACCESS_TO` must explicitly include **`/home/node/.n8n-files;/scripts;/watch`** (replacement semantics, not append).
- **Binary/workload:** `N8N_DEFAULT_BINARY_DATA_MODE: filesystem`; `N8N_PAYLOAD_SIZE_MAX: "64"` (MB-scale HTTP bodies).
- **Nodes:** `NODES_EXCLUDE: "[]"` to allow Execute Command / Read Write File where required.
- **PARA caveat:** Compose comments advise **avoiding bracket-heavy bind sources** for *future* extra mounts (e.g. Utilix archives); MSSQL writes `.bak` on **Windows host**, not via n8n file node.

**Backup workflow structure (deduped)**

- **Triggers merged into one funnel:** cron **hour 2 minute 0** (timezone follows n8n/Compose `America/New_York`), **Webhook** static id **`mssql-backup-static`**, **Local file** watch **`*.trigger`** under `/watch`, **Manual**.
- **Metadata:** `Set Run Metadata` sets `trigger_source` (`schedule` | `webhook` | `file_drop` | `manual`), `run_id`, `started_at`.
- **Execution chain:** Read SQL script file → extract text → MSSQL execute → Code node summarizes rows (`backup_ok`, `backup_failed`, retention actions) → append JSON lines to log via Read/Write Files.
- **Operational implication:** Verification = **JSONL line** + new **`Utilix_<stamp>.bak`** under **`C:\code\_PARA\1_[P]roject\cenhud.utilix\04_archive\<yyMMdd>\`** per SQL (`@backup_root` in authoritative script).

---

## 3. Watch folder → GDrive + Access tooling

- **Workflow:** **`Watch Folder → Sync to Google Drive`** — **`localFileTrigger`** → **`Filter GX Files`** (`if`) → **`Copy GX to Drive`** (`executeCommand`) vs **`Filter Access DBs`** → **`Execute Dump Script`**.
- **`link-db-to-watch.ps1`:** Parameters **`SourcePath` (mandatory)** and **`WatchDir`** default `…\n8n\_watch`; same-volume → **hard link**; cross-volume → **symlink** with explicit reliability warning for watcher semantics.
- **`dump-access-db.ps1`:** Copies DB to `%TEMP%`, strips `MsgBox` continuation from VBA, imports **`DumpAccessDB_Auto`**, runs `DumpAccessDatabase`, ships zip to **`G:\My Drive\Utilix`**with prefix **`GX.`** — ties to GX filter branch naming in workflow.

---

## 4. CFP-intake specification lane (distinct from MSSQL backups)

Summarized from `kn.spec.00.01.19_n8n-auto.md` (full ASCII architecture diagram and payload schemas remain in that file):

- **Goals:** Multi-route intake (Webhook, Drive upload, Gmail), merge/normalize → parse → validate against CFP schema → branch → Postgres audit + Slack + email; evidence IDs E001–E013 referenced in header.
- **Webhook contract (spec):** `POST` JSON with `filename`, markdown `content`, nested `metadata` (26-field style frontmatter analogue) — **endpoint name in spec** is `cfp-intake`; **different** from live backup webhook slug.
- **Validation / notification:** Dedicated validation engine section + failure branches (see spec §4 onward).
- **Deployment procedure (`kn.proc.00.01.19_n8n-deploy.md`):** **n8n Cloud** login (`app.n8n.cloud`), import workflow JSON from session output, configure Postgres **least-privilege** user **`n8n_cfp_user`**, Slack webhooks OAuth, Gmail vs IMAP (**IMAP blocked** narrative E012 inside spec excerpt), OAuth redirect **`https://oauth.n8n.cloud/oauth2/callback`**.

---

## 5. Documentation, gap-analysis, and session lineage

### 5.1 Founding sess-01 (gap remediation)

- **Objective:** Exhaustive Procedures + Specifications **audit** before building modular node-per-decision workflows ; emphasis on completeness over implementation in that phase.
- **Quantified ChatGPT-era findings carried into CFP:** **7** conceptually isolated documents; **4** coverage/integration gaps referenced in manifest/key findings narrative.
- **Concrete gap themes (CFP snapshot):**
  - Validation logic in specs not operationally threaded through procedures (**isolated validation** symptom).
  - Session lifecycle lacked deployment linkage (**session → deploy bridge** gap).
  - Procedure **`quench-name`** called out as isolated from archive/project flow (**example** — verify against current corpus if revived).
- **Blocked / unresolved meta-task (still relevant):** whether **`kn.pmpt…` governance prompts** ship in parallel vs **`kn.docg…` project KT** — flagged as KT/CFP template confusion (**T13-class** blocker in todo gap doc).

### 5.2 Successor directives (repeatable STARTUP PROMPT pattern)

Canonical phrasing variants appear in KT gap + manifest; converge to:

> Continue **n8n workflow gap analysis** / doc remediation from **sess-01** lineage: reload **non-truncated** Procedures+Specifications corpus, rerun interconnection coverage, prioritize link remediation for isolated docs, then emit **workflow JSON skeleton** mapping procedures/specs ↔ nodes (**T08–T12** backlog in gap todo).

Mirror YAML pairs carry identical payload for machine ingest.

### 5.3 sess-02 logic tree strand (`S03` archive)

Todos **T08–T14**: consolidated gaps with template xref (**E47**), branching policy (**E49**), full startup conditional tree (**E49-A**), remaining phase trees (**T11–T12**), future JSON bundles for unrelated workflow classes (**CRM→Notion**, **AI Email** — **may be aspirational** vs deployed). **Blocked:** **as-is vs target** behavior confirmation before generating production JSON (**T15**).

### 5.4 sess-03 KT operational narrative (`kn.docg…_kt-n8n.md`)

- Implemented **Drive-based KT watcher** → **filter** → **merge/validation**.
- Formalized **Node Notes** skeleton: Purpose, behavior, Inputs, Outputs, Evidence ref (**E50-A**).
- **Forward work:** behavioral / message grading tree (**E51** onward) — aligns with `kn.docg…_todo-n8n.md` incomplete **T18–T20**.

### 5.5 Workflow pattern docs rooted in staging (`kn.wkfl`)

- **Housekeeping:** module chain **delta-scan**, **pending-cleanup**, **folder-cleanup** — maps to **`proc-housekeep`** class automation described in housekeeping unified corpus (**webhook**, **scheduled**).
- **File maintenance:** **newest-first** processing discipline; graded routing; **`approval_required: true`** in governance metadata for manual lane.

Duplicate UUID-prefixed exports (`housekeep__…`, `file-mant__…`) add taxonomy-style headers — **same narrative body** — unique delta is archival metadata + phantom module filenames.

### 5.6 `_from_worktree` duplicates

**S02** `cfp-n8n-wkfl-gap` files = **semantic duplicate** of root `*_kt-n8n-wkfl-gap` during CFP rebranding.**S04** similar packing.**S01** retains original **manifest + re.rcvm CFP naming**. Use **root `kn.docg…`** unless reproducing forensic session history.

---

## 6. Conflicts / reconciliation (explicit)

| Topic | Source A | Source B | Guidance |
| ----- | --------- | --------- | --------- |
| **Hosting model** | `kn.proc` / `kn.spec` (**n8n Cloud**, managed OAuth domains) | `compose.yaml` (**local Docker**, `WEBHOOK_URL` localhost) | Local stack wins for **Utilix MSSQL backups** today; Cloud procedure is **valid only** if migrating CFP-intake design. |
| **UI authentication** | Legacy basic-auth wording in historic mental models | Compose comments: User Management stores creds in volume; **`n8n user-management:reset`** | Follow **Compose + n8n 2.x** behavior. |
| **Webhook paths** | Spec: `/webhook/cfp-intake` | Backup workflow: static **`webhookId` `mssql-backup-static`** + node label **`POST /mssql-backup`** | **Separate workflows** — no PATH merge. |
| **Reference workflow asset** | CFP cites `kv/20_Areas/Automations/kn.flow.03.03.19_cfp-intk-vald.json` | May not exist at that path inside `C:\code` | Treat as **pointer** — resolve before importing. |
| **KT vs CFP lexical drift** | `kn.docg…_kt-*` vs `_ar/S02*` `*_cfp-*` | Parallel filenames | Same gap-analysis content generation; **`kt-n8n*` root** canonical for sess-03+ unless reproducing **`cfp`** experiment. |
| **Backup archive root (`@backup_root`)** | `mssql-backup-with-guardrails.sql` (**PARA `04_archive` tree** — as deployed for Phase 0) | `internal.n8n-integration_260429-1137.yaml` **T-001** (**`C:\Backups\SQL\Lazarus\SQLEXPRESS\…`** nested layout, retention walk) | **As-built vs planned:** reconcile on disk (`FORMAT` paths + JSONL timestamps) before treating bootstrap task as done. |

---

## 7. Gaps and excerpts

- **Truncation risk:** KT gap pack states ChatGPT archive ellipses → **inventory incomplete** unless raw Knowledge.zip / full tree re-loaded (**T08**-class).
- **Out-of-tree workflows:** **`kn.flow…cfp-intk-vald.json`** referenced but **not** in corpus root → integration **unverified** from workspace alone.
- **Module files for UUID housekeeping export:** Composition lists (`delta-scan__….md`) **not bundled** — workflows reference **conceptual modules**.
- **`kn.spec` checksum frontmatter:** `checksum_sha256: pending` — do not rely on declarative completeness field for verification.
- **Python runner:** prior `docker logs` on local n8n showed optional internal Python runner missing — **noise for JS workflows** unless Code node relies on Python (not evidenced in MSSQL workflow grep).
- **Multiple `n8n_research_playbook.yaml` mirrors:** PARA `03_outputs` and `_staging\governance-rewrite\vocab-gov` are **symlinks** to **`C:\Users\rtoth\.cursor\commands\research\n8n\playbook\n8n_research_playbook.yaml`**; pre-symlink snapshots kept as `*.pre_symlink_bak` beside each link.

---

## 8. Extended reference registry (playbook methodology + workspace abilities)

### 8.1 Scoped question (research output contract)

Produce and maintain verifiable pointers for **n8n automation on this workstation**: self-hosted Docker (**`n8n-local`**), **MSSQL** backup lane, adjunct **GDrive/GX–Access** lane, **Cursor** housekeeping/janitor JSON, PARA governance/bootstrap continuity, plus **official n8n** documentation whenever behavior or licensing must be defended.

### 8.2 Procedure sources (follow in order)

1. **Fill variables:** `TOPIC=n8n` (add `PRIMARY_PRODUCT=mixed`, `PRIMARY_SURFACE` from `n8n_core`/`n8n_hosting`/… enums in specialized playbook below).
2. **Open tier-1:** Prefer **`n8n_research_playbook.yaml` § `tier_1_official`** over random blogs (`C:\Users\rtoth\.cursor\commands\research\n8n\playbook\n8n_research_playbook.yaml`).
3. **Repo search templates** (adapted from `ai_research_playbook.yaml` `search_templates.github_code` — substitute `TOPIC=n8n`):
	- `path:.cursor/commands language:yaml n8n`
	- `path:_staging/Automation/n8n n8n`
	- `path:_PARA/1_[P]roject/internal.n8n-integration n8n`
	- `filename:*n8n* path:c:/code`
4. **Triangulate** community items only via **`tier_3_community_zeitgeist`** in `n8n_research_playbook.yaml` — label **Zeitgeist**, not canon.
5. **Conflicts:** vendor/docs.n8n.io wins over Reddit/YouTube; **Compose + exported JSON on disk** wins over ivory-tower **`kn.proc` cloud** prose for **this host**.

### 8.3 Official n8n — condensed tier-1 (pin exact pages from registry file)

Authority order matches `n8n_research_playbook.yaml` **`identity.authority_model`**. High-yield entries (HTTPS; expand via registry):

| Use case | URL |
| -------- | ----- |
| Docs home / quickstarts | https://docs.n8n.io/ |
| Hosting (self-host baseline) | https://docs.n8n.io/hosting/ |
| Docker install narrative | https://docs.n8n.io/hosting/installation/docker/ |
| Env var reference (**`N8N_*`** truth) | https://docs.n8n.io/hosting/configuration/environment-variables/ |
| Release notes (**pin compat with `compose` image**) | https://docs.n8n.io/release-notes/ |
| Webhooks (production vs test URL, signing) | https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/ |
| Built-in integrations / Microsoft SQL node | https://docs.n8n.io/integrations/ |
| Expressions + Code node | https://docs.n8n.io/code/expressions/, https://docs.n8n.io/code/builtin/code-node/ |
| Securing n8n (**SSRF, auth**) | https://docs.n8n.io/hosting/securing/overview/ |
| Public REST API + CLI (`@n8n/cli`) | https://docs.n8n.io/api/, https://docs.n8n.io/hosting/cli-commands/ |
| Fair-code / Sustainable Use license | https://docs.n8n.io/faircode-license/, https://blog.n8n.io/announcing-new-sustainable-use-license |
| Source releases (diff against **2.18.5** pin) | https://github.com/n8n-io/n8n/releases |

**Community LLM aides (not behavioral spec):** `https://cdn.n8n.community/llms.txt`, expression/code rule mirrors on same CDN — per playbook `url_redirect_notes`.

### 8.4 Tier-2 “abilities” (Curated repos — verify before reliance)

Listed in `n8n_research_playbook.yaml` **`tier_2_curated_repos`**; highlights for **this** workspace:

| Asset | Why it matters here |
| ----- | -------------------- |
| https://github.com/n8n-io/n8n | Issue search, release parity with Docker tag. |
| https://github.com/n8n-io/n8n-docs | Source for docs.n8n.io (MkDocs). |
| https://github.com/n8n-io/n8n-hosting | Alternate Compose / reverse-proxy recipes vs hand-rolled **`compose.yaml`**. |
| https://github.com/czlonkowski/n8n-mcp | MCP exposure of nodes/templates for **assistant-driven workflow authoring** (Cursor ecosystem fit). |

### 8.5 Cross-stack: Cursor / MCP tier-1 (from generic playbook)

Use `C:\code\_staging\ai_research_playbook.yaml` **`source_registry.tier_1_official`** when wiring **skills, rules, or MCP**:

- Cursor rules/skills/agents/hooks — https://cursor.com/docs/rules , https://cursor.com/docs/skills  
- MCP specification — https://modelcontextprotocol.io/specification/latest  

### 8.6 Copy-paste web search strings (`TOPIC=n8n`, `YEAR_HINT=2026`)

From `ai_research_playbook.yaml` templates (fill `{}` omitted — already literal):

- `site:docs.n8n.io n8n (webhook OR schedule OR credential OR Docker OR "environment variables")`
- `site:github.com/n8n-io n8n (issue OR release OR microsoftSql OR "readWriteFile")`
- `site:cursor.com OR site:docs.cursor.com n8n (skills OR MCP OR workflows)`
- `site:reddit.com/r/n8n (self-hosted OR Docker OR webhook)`
- `site:stackoverflow.com n8n (docker OR webhook OR mssql)`

### 8.7 Zeitgeist (non-canon reminder)

Forum threads, influencer templates, Skool/courses — `n8n_research_playbook.yaml` **`tier_3_community_zeitgeist`** — triage failures only after tier-1.

---

## Quick lookup

| I need to … | Open |
| ----------- | ------ |
| Start / upgrade **local** n8n (`n8n-local`, volumes, mounts) | `C:\code\_staging\Automation\n8n\compose.yaml` |
| See **pinned image** and **`N8N_*` knobs** | same |
| Inspect **backup trigger wiring + webhook id + log append** | `C:\code\_staging\Automation\n8n\mssql-backup.workflow.json` |
| Inspect **folder → GX / Access** automation | `C:\code\_staging\Automation\n8n\watch-folder-to-gdrive.workflow.json` |
| Link a file into the **watch** drop area | `C:\code\_staging\Automation\n8n\link-db-to-watch.ps1` |
| Run **Access** dump to **GDrive local folder** | `C:\code\_staging\Automation\n8n\dump-access-db.ps1` |
| Read **canonical SQL** backing MSSQL backups | `C:\code\_PARA\libraries\code\sqlt\mssql-backup-with-guardrails.sql` |
| Recover **sess-01** startup + gap counts | `C:\code\_staging\Automation\n8n\_ar\_from_worktree\S01_0302\manifest.json` + `re.rcvm.07.08.19_n8n.md` |
| Full **CFP-intake architecture + payloads** | `C:\code\_staging\Automation\n8n\kn.spec.00.01.19_n8n-auto.md` |
| **Deploy CFP-intake to cloud + credentials** narrative | `C:\code\_staging\Automation\n8n\kn.proc.00.01.19_n8n-deploy.md` |
| Track **sess-03** KT continuity build | `C:\code\_staging\Automation\n8n\kn.docg.07.08.19_kt-n8n.md` |
| Recover **baseline gap todos + evidence IDs** | `C:\code\_staging\Automation\n8n\kn.docg.07.08.19_todo-n8n-wkfl-gap.md` |
| Recover **sess-02 logic-tree todos** only | `C:\code\_staging\Automation\n8n\_ar\_from_worktree\S03_0654\kn.docg.07.08.19_todo-n8n_workflow_logic_tree.md` |
| Dispatcher for **automated housekeeping** semantics (related system) | `C:\Users\rtoth\.cursor\commands\housekeeping\housekeeping_unified_corpus.md` |
| **Automation default** stance (why can’t / shouldn’t) | This file — **§ Automation default (command context)** |
| Full **merge + inventory rules** (corpus-unify skill) | `c:\Users\rtoth\.cursor\skills-cursor\corpus-unify\SKILL.md` |
| **Full n8n vendor / community tier registry** (~500 lines, all surfaces) | `C:\Users\rtoth\.cursor\commands\research\n8n\playbook\n8n_research_playbook.yaml` |
| Generic **AI research playbook** (Cursor, MCP, OpenAI tiers + search templates) | `C:\code\_staging\ai_research_playbook.yaml` |
| **`internal.n8n-integration`** bootstrap (tasks T-001…, infra path intent) | `C:\code\_PARA\1_[P]roject\internal.n8n-integration\02_working\chat-sessions\bootstrap\internal.n8n-integration_260429-1137.yaml` |
| Utilix milestone + Phase 0 + schedule risk carryover | `C:\code\_PARA\1_[P]roject\cenhud.utilix\02_working\plans\utilix-typedb-migration-milestone-plan.md`, `…\phase-0-baseline\phase-0-completion.260430-0618.md`, bootstrap `Utilix_260430-0545.yaml` |
| Governance-rewrite **mirrors** of n8n kn.* packs | `C:\code\_staging\governance-rewrite\vocab-gov\` (search `n8n`) |

---

## Self-check (corpus-unify Step 5)

- [x] Every inventoried path (except `.env`) appears in provenance or conflicts.
- [x] YAML mirrors flagged as subsumed without dropping traceability rows.
- [x] Repeated operational facts (**02:00 schedule**, binds, webhook id) stated once in §2 / §6.
- [x] Local vs Cloud / CFP vs Backup conflicts explicit.
- [x] Quick lookup answers **which file for X**.
- [x] `ai_research_playbook`-style tiering applied: tier-1 n8n docs + registry pointer; Zeitgeist separated; playbook copy-paste searches recorded.
- [x] **Automation default** (command context §) present for hand-triggered use of this path.
