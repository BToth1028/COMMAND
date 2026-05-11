---
id: kn.wkfl.00.01.19_file-mant
title: 'Workflow: File Maintenance'
description: Analysis workflow - orchestrates modules for inventory, concept review, grading, routing
type: documentation
category: architecture
status: working
created: 260111-0545
updated: 260202-1230
author: Claude-Opus-4.5
owner: operator
tags:
- workflow
- maintenance
- analysis
- orchestrator
- grading
relations:
- Session Lifecycle
- Master Workflow Index v2.0
- File Compliance Workflow
- Import/Quarantine Workflow
- kn.modl.00.01.19_file-grad.md
source: File maintenance best practices
dependencies: []
automation_hooks: []
evidence_id_range: ''
coverage_window_start: ''
coverage_window_end: ''
completeness: 100%
project_name: ''
uuid: file-mant-proc-260111
checksum_sha256: pending
mirror_yaml: ''
platform: Cursor
make: Anthropic
model: claude-opus-4.5
session_id: ''
governance_node:
  node_id: kn.wkfl.00.01.19_file-mant
  node_type: workflow
  authority_level: session
  governed_by: kn.life.00.01.19_session.md
  executable: false
  invocable_by:
  - lifecycle
  - automation
  approval_required: true
  observable: true
children: []
composition: []
---
# File Maintenance Workflow

**Purpose:** Analyze existing files - inventory, concept review, grading, route to File Compliance
**Type:** Orchestrator - calls modules for execution
**Scope:** Cleanup, reorganization, import processing

---

## Core Principle: Newest First

**CRITICAL:** All steps in this workflow process files from **newest to oldest** by last modified date.

**Why:**
- Newest files show current direction and active work
- Recently modified files are most relevant
- Older files are more likely stale or obsolete
- Establishes context before reviewing historical content

**Apply to:**
- File inventory listing
- Concept review order
- Grading order
- All file operations

---

## When To Use

- Cleaning up existing files
- Reorganizing files
- Processing imported files (after quarantine)
- Reviewing legacy/historical content
- **NOT for new files** - use File Compliance directly

---

## Todo List

```
[ ] STEP 1: INVENTORY → mod-file-invt
    [ ] 1.1 List all files in scope (SORTED BY LAST MODIFIED, NEWEST FIRST)
    [ ] 1.2 Categorize by type/extension
    [ ] 1.3 Note modification dates to establish direction

[ ] STEP 2: CONCEPT REVIEW → mod-file-grad (Phase 1)
    [ ] 2.1 Start with NEWEST files to establish current direction
    [ ] 2.2 Evaluate concept value (is the idea useful?)
    [ ] 2.3 Check content quality (salvageable?)
    [ ] 2.4 Assess integration potential (merge opportunity?)
    [ ] 2.5 Verify directional alignment (fits current strategy?)
    [ ] 2.6 Route invalid concepts to ARCHIVE/DELETE

[ ] STEP 3: 4-AXIS GRADING → mod-file-grad (Phase 2)
    [ ] 3.1 Grade files in order (newest first)
    [ ] 3.2 Grade Quality (1-5)
    [ ] 3.3 Grade Effort (1-5)
    [ ] 3.4 Grade Relevance (1-5)
    [ ] 3.5 Grade Direction (1-5)
    [ ] 3.6 Apply decision matrix

[ ] STEP 4: ROUTE
    [ ] 4.1 PROMOTE (16-20) → File Compliance
    [ ] 4.2 REFINE (12-15) → Update, then File Compliance
    [ ] 4.3 HOLD (8-11) → Keep in quarantine
    [ ] 4.4 ARCHIVE (4-7) → Archive with path-mirroring
    [ ] 4.5 DELETE (1-3) → Archive then stage to tp/stag/

[ ] STEP 5: CLEANUP → mod-fldr-clnp
    [ ] 5.1 Remove empty folders

[ ] FINAL: APPROVAL → mod-user-conf
```

---

## Module Sequence

### STEP 1: File Inventory

**Module:** `kn.modl.00.01.19_file-invt.md`

**Input:** Target path, recursive flag
**Output:** Files sorted by last modified (newest first), grouped by extension

<!-- ATOMIC: file-inventory -->
<!-- INPUTS: target_path, recursive_flag -->
<!-- OUTPUTS: file_list, sorted_by_modified, grouped_by_extension -->
**CRITICAL:** Sort by LastWriteTime descending. This establishes:
- What's being actively worked on
- Current direction and priorities
- Context for reviewing older files

**Example Output:**
```
Last Modified    | File
-----------------|----------------------------------
260112-1300      | to.genr.03.02.21_wbs-full.py
260111-0900      | da.wbs.00.00.08_hierarchy.csv
260105-1400      | check_foundation.py  ← older = less relevant
251215-0800      | legacy_import.py     ← oldest = likely obsolete
```

---

### STEP 2: Concept Review

**Module:** `kn.modl.00.01.19_file-grad.md` (Phase 1)

**Start with newest files** - they define current direction. Then review older files against that context.

**Concept Review Questions:**

| Question | Evaluation |
|----------|------------|
| **Concept Value** | Is the underlying idea worth having? |
| **Content Quality** | Is there salvageable content to integrate? |
| **Integration Potential** | Could this improve something we already have? |
| **Directional Alignment** | Does it fit current strategy/tooling? |

**Current Strategic Directions:**

| Area | Direction |
|------|-----------|
| Automation/Scheduling | n8n workflows |
| Workflow orchestration | n8n (not manual counters) |
| File storage | Standard Taxonomy + Vault Taxonomy |
| Archiving | Path-mirrored with YYMMDD/HHMM |
| Workflows/Modules | Human-readable docs in `30_Knowledge/` |

**Concept Review Outcomes:**

| Result | Action |
|--------|--------|
| CONCEPT VALID | → Proceed to 4-Axis Grading |
| CONCEPT GOOD, MISALIGNED | → Archive with notes |
| CONCEPT REDUNDANT | → Delete or merge |
| CONCEPT OBSOLETE | → Delete |

**User Approval:** Show concept review, get approval before proceeding

---

### STEP 3: 4-Axis Grading

**Module:** `kn.modl.00.01.19_file-grad.md` (Phase 2)

**Process files newest to oldest.** Newest files set the bar for relevance.

**4-Axis Grading:**

| Axis | What It Measures |
|------|------------------|
| Quality (1-5) | Code/content condition |
| Effort (1-5) | Work needed to update |
| Relevance (1-5) | Usefulness/priority |
| Direction (1-5) | Strategic alignment |

**Decision Matrix:**

| Score | Category | Action |
|-------|----------|--------|
| 16-20 | PROMOTE | → File Compliance (final location) |
| 12-15 | REFINE | Update first, then → File Compliance |
| 8-11 | HOLD | Keep in quarantine for later |
| 4-7 | ARCHIVE | → Archive with path-mirroring |
| 1-3 | DELETE | Archive then stage to `tp/stag/` |

**User Approval:** Show grades, get approval

---

### STEP 4: Route Files

| Decision | Route To |
|----------|----------|
| PROMOTE | → `kn.wkfl.00.01.19_file-comp.md` |
| REFINE | Update first, then → File Compliance |
| HOLD | Keep in quarantine |
| ARCHIVE | → `kn.wkfl.00.01.19_archive.md` |
| DELETE | → Archive first, then `tp/stag/{YYMMDD}/` |

---

### STEP 5: Cleanup Empty Folders

**Module:** `kn.modl.00.01.19_fldr-clnp.md`

**Input:** Source path
**Output:** Removed empty folders

---

### FINAL: User Approval

**Module:** `kn.modl.00.01.19_user-conf.md`

Show summary, get approval

---

## Quick Reference

```
FILE MAINTENANCE ORCHESTRATION:

*** ALWAYS PROCESS NEWEST TO OLDEST ***

STEP 1: mod-file-invt   → List & categorize (sorted by last modified DESC)
STEP 2: mod-file-grad   → Concept Review (Phase 1) - newest first
        - Concept value?
        - Content quality?
        - Integration potential?
        - Directional alignment?
STEP 3: mod-file-grad   → 4-Axis Grading (Phase 2) - newest first
        - Quality + Effort + Relevance + Direction
STEP 4: Route           → Based on score
STEP 5: mod-fldr-clnp   → Remove empty folders
FINAL:  mod-user-conf   → Approval

DECISION MATRIX:
- 16-20 → PROMOTE
- 12-15 → REFINE
- 8-11  → HOLD
- 4-7   → ARCHIVE
- 1-3   → DELETE (archive first, then tp/stag/)
```

---

## Review Mindset

**Critical:** Don't just evaluate implementation quality. Consider:

1. **The Concept** - Is the underlying idea valuable?
2. **The Content** - Can anything be salvaged or integrated?
3. **The Direction** - Does it align with where we're going?
4. **The Recency** - Newer files define direction, older files are judged against it

A well-implemented feature that conflicts with our direction should be archived.
A poorly-implemented concept that aligns with our direction should be rebuilt.

---

## Next Workflow Options

```
1. Continue to File Compliance → kn.wkfl.00.01.19_file-comp.md
2. Analyze another location → Restart this workflow
3. Import more files → kn.wkfl.00.01.19_impt-quar.md
4. Archive files → kn.wkfl.00.01.19_archive.md
5. End session → mod-sess-doc
```
