# Housekeeping documentation harvest — index

Generated: 2026-04-24. This folder contains copies of primary sources found by searching `c:\code` and `C:\dev` (and related Cursor paths) for file housekeeping: automated cleanup, old-file triage, merge/delete/archive routing, and snippet library flows.

## Files copied into this folder (verbatim)

| Local copy | Original path |
|------------|---------------|
| `housekeeping.yaml` | `C:\Users\rtoth\.cursor\commands\housekeeping\housekeeping.yaml` — **Cursor command spec**: session file review, PARA placement, stub/duplicate detection, soft delete, merge proposals, git hints. |
| `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_housekeep.md` | `C:\dev\50-59-infrastructure-and-devops\56-scripts-and-automation\56.04-n8n-workflows\kn.wkfl.00.01.19_housekeep.md` — **workflow doc**: delt-scan → pend-clnp → fldr-clnp; n8n integration. |
| `c-code__staging__Automation__n8n__kn.wkfl.00.01.19_file-mant.md` | `C:\dev\50-59-infrastructure-and-devops\56-scripts-and-automation\56.04-n8n-workflows\kn.wkfl.00.01.19_file-mant.md` — **file maintenance**: newest-first inventory, concept review, 4-axis grading, route PROMOTE/REFINE/HOLD/ARCHIVE/DELETE, then fldr-clnp. |
| `rtoth-code__va__ar__Automations__Workflows__proc-housekeep.json` | **n8n orchestrator** JSON (exported janitor graph: mod-delt-scan, mod-pend-clnp, mod-fldr-clnp) — correlate with **`56.04-n8n-workflows`** + **`kn.wkfl.00.01.19_housekeep.md`** on **`C:\dev`**. |
| `c-code__staging__snip-stor__kn.wkfl.00.01.19_snip-stor.md` | `C:\dev\_staging\0.U_Inbox\KT\~~~CURRENT~~~\02_most\kn.wkfl.00.01.19_snip-stor.md` — **snippet storage** to `li/code/snippets/`. |
| `c-code__staging__snip-harv__kn.wkfl.00.01.19_snip-harv.md` | `C:\dev\_staging\0.U_Inbox\GOVERNANCE\z9-trash\Workflows\kn.wkfl.00.01.19_snip-harv.md` — **snippet harvest** from source files. |
| `cursor_plans__housekeeping_system_completion_6c3bfff8.plan.md` | `%USERPROFILE%\.cursor\plans\housekeeping_system_completion_6c3bfff8.plan.md` — plan tying file-mant, modules, n8n, cross-ref work. |
| `cursor_plans__housekeeping_batch_p5_9f85cc6d.plan.md` | `%USERPROFILE%\.cursor\plans\housekeeping_batch_p5_9f85cc6d.plan.md` — **note:** “housekeeping” here is a **DB/Utilix batch** (tblAuditLog, cardinality, axioms doc), not general file cleanup. |
| `rtoth-code__specstory__housekeeping-procedure-summary_EXCERPT.md` | Excerpt from SpecStory (see below). |

## Additional locations (not duplicated — duplicates or chat logs)

- **SpecStory (full, large):** `%USERPROFILE%\.specstory\history\2026-01-22_10-35Z-housekeeping-procedure-summary.md` — includes an agent summary of a **7-step** `kn.proc.00.01.19_housekeep` procedure (historical host path; not under **`C:\dev`** JDex).
- **Governance merge chat:** `%USERPROFILE%\.specstory\history\2026-02-11_19-05Z-bootstrap-and-todo-list-summary.md` — `housekeep` vs `file-mant` redundancy, merge n8n into file-mant, archive workflows.
- **Duplicate staging copies:** treat **`56.04-n8n-workflows`** on **`C:\dev`** as canonical for the n8n automation tree; older host-only staging trees are retired under clean-break policy.
- **Utilix bootstraps:** see **`46.01-bootstrap-yamls`** and Utilix domain YAMLs on **`C:\dev`** (domain: housekeeping).

## Theme map (what handles “old files”)

1. **Automated / scheduled (repo hygiene):** `kn.wkfl` housekeep + `proc-housekeep.json` (delta scan, pending deletion folders, empty folders).
2. **Human-in-the-loop triage of legacy files:** `kn.wkfl` file-mant (grading matrix, archive/delete, promote to file-comp).
3. **Cursor command “housekeeping”:** `housekeeping.yaml` — session-touched files, merge/remove/relocate with approval.
4. **Preserving code as reusable assets:** `snip-harv` + `snip-stor` (snippet library at `li/code/snippets/`).

## Missing from this repo root

- `kn.proc.00.01.19_housekeep.md` may appear only in SpecStory / archived exports — verify under **`C:\dev`** JDex if resurrected as a governed doc.
