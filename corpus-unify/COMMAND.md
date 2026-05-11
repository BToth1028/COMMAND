---
name: corpus-unify
description: Merges multiple related documents in a folder into one reference file with conservative deduplication—only TRUE duplicates are removed; nuance, framing, examples, and decision-relevant context are retained even when sources overlap. Surfacing conflicts and homonyms stays mandatory. Inventory assumes processes are automatable until a defensible cannot/should-not is recorded. Use when the user wants a single coherent corpus, unified reference, “dedupe without losing nuance,” folder merge, or consolidation of overlapping docs (not aggressive summarization, not formal scoring registries like R*/Q* unless requested).
---

# Corpus unify (maximal context + true-dedup only)

## Purpose

Build **one** markdown file that a human can use as the **operational reference** for a **multi-file corpus**: the default is to **keep as much context as possible**—including overlapping material—unless it is a **true duplicate** (defined below). Information that appears in only one source is **kept**; **contradictions and homonyms** are made explicit, not hidden.

**Bias:** many real corpora are **nuanced** (constraints, exceptions, audience-specific wording, “when this applies” detail). Prefer **retention and explicit bridging** over aggressive folding. If two passages are *similar* but not *identical in information and framing*, they are **not** duplicates—keep both or merge into one section with **per-source sub-bullets** so nothing is flattened away.

This is **not** the same as:

- **Structural reconstruction** (heavy deletion, claim atomization, short output) — use that skill when the goal is a compressed cognitive skeleton, not a merged manual.
- **Multi-session / blueprint distillation** (R*, Q*, tier scoring, test matrices) — use only when the user explicitly wants that audit-style artifact.
- **Copy-paste concatenation** — forbidden as the default outcome.

## True duplicate vs. overlap (dedup boundary)

Use this litmus test before removing or collapsing anything:

- **True duplicate (safe to fold to one instance):** same informational payload **and** no additional decision-relevant detail in either copy—substantively identical claims, lists, numbers, and constraints; wording may differ trivially (typos, spacing). You may state once and note `(same in A, B)` if traceability helps.
- **Not a duplicate (keep both or keep explicit deltas):** different examples, edge cases, rationale, warnings, scope qualifiers (“usually,” “unless,” “for operators”), ordering that implies priority, different thresholds or filenames, or **different phrasing that could change how someone acts**. Treat overlapping *themes* with different *texture* as **context worth preserving**, not noise.

**When uncertain:** do **not** collapse. Keep both passages, or one block with **Source A / Source B** sub-bullets capturing what each adds.

## Automation default (inventory attitude)

When scanning the **corpus root** and everything it implies across the folder structure—files **and** what they describe or drive (scripts, schedules, containers, MCP, webhooks, operator checklists, services, queues):

- **Base assumption:** any repeated, cross-boundary, or trigger-like activity **can** be automated until a **defensible** barrier is written down.
- **Forbidden default:** asking only whether something *might* be automated (“if we could…”) leaves manual work falsely neutral.
- **Required default:** ask **why it cannot** be automated, or **why it should not** be—hard **cannot** (no machine interface, unknowable inputs, cryptographic human step, physical reality, immutable policy prohibition) versus **should not** (risk, loss of determinism, compliance, economics, lawful human accountability—tie to **sources** where the corpus supplies them; label **operator preference** explicitly when inferred).
- Treat **currently manual or semi-manual** practice in the corpus as **automation gap or deliberate exception**, not an inherent category, unless barriers are stated above.

Fold this into the merge: do not ship a sermon—surface it in **Gaps**, **Merged narrative**, and/or **Conflicts**, and in the **Self-check**.

## Triggers

Use this skill when the user (or task) mentions any of: unified document, single reference, merge folder, deduplicate documentation (without losing nuance), combine sources, one file from many, unique content per file, conservative dedup, true duplicates only, maximal context, overlap handled without flattening, consolidated corpus, “like `housekeeping_unified_corpus`,” or disambiguation of overloaded terms.

## Required inputs

- **Corpus root**: path to a directory **or** explicit list of file paths.
- **Output path** (or name): where to write the unified file; default is `{corpus_root}/{topic}_unified_corpus.md` if unspecified.
- **Exclusions** (optional): glob patterns or names to skip (e.g. prior bad distillations, chat logs, `node_modules`).

If the corpus root is missing, ask before writing.

## Non-negotiable output contract

1. **Provenance first**: a table or list mapping **each** ingested file to one row (name + one-line role). Excluded files named under “Exclusions.”
2. **Conservative dedup (true duplicates only):** remove **only** material that meets the **true duplicate** definition above. If multiple sources state the “same” point with different nuance, **retain the nuance**—either as separate paragraphs, merged prose with explicit “A emphasizes … / B adds …,” or consecutive bullets. Do **not** reduce the corpus to the shortest common formulation.
3. **Context-first retention:** treat rationale, constraints, examples, edge cases, operator guidance, failure modes, and scope qualifiers as **first-class** even when a “core fact” repeats. **Pure** verbatim repetition (copy-paste identical blocks) may drop to one instance; anything else, preserve deltas—or the full richer passage if splitting loses meaning.
4. **Per-source unique facts**: for every file, at least one **non-redundant** fact, procedure, or context delta must appear in the merged doc **unless** the file is empty or fully duplicated (then state “fully subsumed by X”).
5. **Conflicts visible**: if two sources disagree (numbers, names, order, or filenames), do **not** pick silently — use a **Conflicts / resolution** or **per-source note** (e.g. “Workflow says `snip-{slug}`; storage doc says `snip-{hash}` — reconcile before import”).
6. **Disambiguation section** when the same word labels different systems (e.g. “housekeeping” = Cursor command vs n8n vs DB batch). Short numbered list, each item **what it is / what it is not**.
7. **Pointer to authority**: where the full verbatim spec is huge (e.g. long YAML), **extract the operationally decision-relevant parts in full** (thresholds, guards, enums, env vars, idempotency notes)—do **not** summarize away nuance just to save length. Then point to the file: “full verbatim: `[path]`.” If the prose around the config matters for interpretation, keep that prose in the unified doc.
8. **Quick lookup** table at the end: “If you need to … → open …” with concrete paths.
9. **Automation frontier:** across **everything the inventory reveals** about how work is done or executed (including latent paths in prose or config), briefly map **candidate automation surfaces** and, for anything that remains manual or partial **in authoritative sources**, attach a **cannot** or **should not** rationale. Unresolved claims need the **hypothesis:** label—never silent resignation to “mostly manual.”

## Forbidden

- Silently favoring the newest file when sources conflict.
- Replacing the merge with a registry-only artifact (R*, Q*, scoring dimensions) **unless the user asked for that**.
- Dropping a source file from the folder without mentioning it in provenance (either merged or listed as skipped with reason).
- Inventing procedures not present in any source (hypotheses must be labeled as such or omitted).
- Treating “human step” as the default destiny for any described flow **without** a written **cannot / should not** barrier.
- **Aggressive “semantic dedup”** that merges similar-but-not-identical explanations, flattens two warnings into one generic line, or drops examples because “the idea was already stated.”
- **Preferring brevity over fidelity** when trimming overlapping sections—if shortening removes a constraint, example, or hedge present in any source, keep the longer or split presentation instead.

## Execution workflow

### Step 1 — Inventory

- List all files in scope (respect exclusions).
- Classify each file: **index/map**, **full spec**, **plan/roadmap**, **executable config** (JSON/YAML), **historical/excerpt**, **out-of-domain homonym** (same word, different project).
- Trace **executable reality**: triggers, binaries, pipelines, cron, credentials, approvals, MCP or API calls, queues, watcher folders—anything implied as **actually running**, not prose-only ideals.
- For each surfaced process, assume **automatable**: record only **blocking** or **rightful-non-automation** reasons (see Automation default)—not “might automate someday.”

### Step 2 — Build a private overlap map (no need to show unless useful)

- For each pair of files, note where they **touch the same topic**—then tag each case **true duplicate** vs **overlapping but nuanced** (different examples, qualifiers, ordering, or emphasis).
- Mark **unique** bullets per file: only one file says it → must survive in the unified doc.
- Mark **context deltas** liberally: if both say “the same thing” but not as true duplicates, plan to **retain both voices** (merged with labels or adjacent blocks), not to keep “only the delta” at the cost of hiding fuller context from either source.

### Step 3 — Write sections (suggested order)

1. **Title + scope** (what the merged file is and is not).
2. **Provenance table** (and exclusions).
3. **Disambiguation** (if overload exists).
4. **Merged narrative by concern** (e.g. “operator command,” “automation,” “human workflow,” “roadmap — not current behavior”), not by source filename — *except* when two sources are truly different “lanes” and stacking them under one heading would hide boundaries.
5. **Source-specific islands** only when needed: e.g. “DB batch (only in `…plan.md`)” so unique content is not smeared into wrong lane.
6. **Gaps** (index notes missing files, missing paths, excerpt-only content)—include **manual or partial-automation deltas** paired with **why can’t / why shouldn’t**, per Automation default where material exists.
7. **Quick lookup** table.

### Step 4 — Deduplication rules (true duplicates only)

- **Byte-for-byte or trivially identical blocks** (same table, same code fence, same list pasted twice) → one canonical instance; note sources if helpful.
- **Same fact, materially identical detail everywhere** (true duplicate) → one statement; optional “(aligned in A, B).”
- **Same fact, extra context in one source** → keep the **full richer treatment** as the primary block, then add anything still unique from the thinner source; avoid stripping the “redundant” sentence if it adds a hedge or example.
- **Same theme, different phrasing or emphasis** → **not** a duplicate: keep both or use labeled sub-bullets (`From A: …` / `From B: …`).
- **Pure data duplication** (identical paths, IDs, enum rows) → one instance; if *any* cell or comment differs, treat as conflict or merged superset, not a dup.
- **Same fact, different numbers** → conflict list.
- **Subset relationship** → keep the **superset** in body; still surface **non-redundant** lines from the smaller file in place or in a short “Only in [file]” note—do not assume subset without scanning for extra qualifiers.
- **Config vs prose** (e.g. n8n JSON + markdown): merge into one **Automation** section; **concrete** timeouts, JSON keys, and URLs from the **config**; keep **all** narrative, caveats, and “when to use” from **markdown** even if the config partially repeats the steps.

### Step 5 — Self-check before handoff

- [ ] Every file in the inventory (except explicit exclusions) is either reflected in the body or called out as fully subsumed.
- [ ] Only **true duplicates** were removed; overlapping sections with different nuance are still visible (merged with labels or kept in parallel).
- [ ] No example, warning, or scope qualifier present in any source was dropped solely because another source “already covered the main idea.”
- [ ] No contradiction left implicit.
- [ ] One place answers “which document do I open for X?”
- [ ] Automation default honored: observable execution paths inventoried under **assume automatable**, and lingering manual/semi-manual posture has stated **cannot** or **should not** (or **`hypothesis:`** where unknowable)—not tacit assumptions.

## File placement

- **Cursor command**: `C:\Users\rtoth\.cursor\commands\corpus-unify\COMMAND.md` — canonical command file.
- **Companion skill-style trigger file**: `C:\Users\rtoth\.cursor\commands\corpus-unify\SKILL.md` — mirrors command behavior for skill-style discovery only; it is not the canonical command contract.

## Example section skeleton (template)

```markdown
# {Topic} — unified reference (from `{corpus_root}`)

**Sources merged:** [table]
**Exclusions:** [list or “none”]

## 1. What “{overloaded term}” means (if applicable)
- Lane A: …
- Lane B: …

## 2. {First concern} (merged; true-dupes only)
…

## N. Gaps and excerpts
…

## Quick lookup
| I need to … | Open |
|-------------|------|
| … | `path` |
```

## Relation to other skills

- **structural-reconstruction**: compress and classify claims; use when the deliverable is **short** and **insight-dense**. **Corpus-unify** is the opposite default: **retain context** and remove only **true duplicates**—do not route a nuanced merge through reconstruction unless the user asks for compression.
- **prompt-builder**: if the user wants a **reusable machine prompt** for future corpus merges, translate this workflow into YAML-first prompt blocks there.
- **writing-plans**: if the corpus is huge or high-risk, write a one-page plan and get approval before generating the unified file.
