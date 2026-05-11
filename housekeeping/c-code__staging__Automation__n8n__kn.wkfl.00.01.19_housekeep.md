---
id: kn.wkfl.00.01.19_housekeep
title: 'Workflow: Housekeeping'
description: Orchestrate automated cleanup tasks - delta scanning, pending deletion, empty folder removal
type: documentation
category: architecture
status: working
created: 260205-0930
updated: 260205-0930
author: Claude-Opus-4.5
owner: operator
tags:
- workflow
- housekeeping
- cleanup
- automation
- n8n
relations:
- kn.wkfl.00.01.19_file-mant.md
- kn.wkfl.00.01.19_file-comp.md
- proc-housekeep.json
source: Formalized from housekeep procedure and n8n automation
dependencies: []
automation_hooks:
- n8n webhook trigger
- scheduled daily run
evidence_id_range: ''
coverage_window_start: ''
coverage_window_end: ''
completeness: 100%
project_name: ''
uuid: housekeep-wkfl-260205
checksum_sha256: pending
mirror_yaml: ''
platform: Cursor
make: Anthropic
model: claude-opus-4.5
session_id: ''
governance_node:
  node_id: kn.wkfl.00.01.19_housekeep
  node_type: workflow
  authority_level: session
  governed_by: kn.life.00.01.19_session.md
  executable: false
  invocable_by:
  - lifecycle
  - automation
  - n8n
  approval_required: false
  observable: true
children:
- id: modl-delt-scan
  relation_type: calls
- id: modl-pend-clnp
  relation_type: calls
- id: modl-fldr-clnp
  relation_type: calls
composition:
- type: module
  id: modl-delt-scan
  file: kn.modl.00.01.19_delt-scan.md
  purpose: Scan for files modified since last run
- type: module
  id: modl-pend-clnp
  file: kn.modl.00.01.19_pend-clnp.md
  purpose: Delete expired folders from pending staging
- type: module
  id: modl-fldr-clnp
  file: kn.modl.00.01.19_fldr-clnp.md
  purpose: Remove empty folders after file operations
---

# Housekeeping Workflow

**Purpose:** Orchestrate automated cleanup tasks for code repository hygiene
**Type:** Orchestrator - calls modules for execution
**Trigger:** n8n webhook, scheduled daily, or manual invocation

---

## When To Use

| Scenario | How You Get Here |
|----------|------------------|
| Scheduled cleanup | n8n scheduled trigger (daily) |
| Post-session cleanup | After session ends |
| Manual cleanup | Direct invocation |
| After file operations | After bulk file moves/deletes |

---

## Todo List

```
[ ] STEP 1: DELTA SCAN → mod-delt-scan
    - Scan for files modified since last housekeeping run
    - Return list of modified files for compliance check
[ ] STEP 2: PENDING CLEANUP → mod-pend-clnp
    - Delete folders older than retention period from ar\pend\
    - Default retention: 14 days
[ ] STEP 3: FOLDER CLEANUP → mod-fldr-clnp
    - Remove empty folders after file operations
    - Recursive pass until no empty folders remain
[ ] FINAL: AGGREGATE RESULTS
    - Combine results from all modules
    - Report summary
```

---

## Module Sequence

### STEP 1: Delta Scan

**Module:** `kn.modl.00.01.19_delt-scan.md`

**Purpose:** Find all files modified since last housekeeping run

**Input:**
- `base_path` = `C:\dev`
- `since_timestamp` = last housekeeping run timestamp (YYMMDD-HHMM)

**Output:**
- `modified_files` = list of modified file paths
- `count` = number of modified files

**Next Step:** Optionally pass to file-comp for compliance checking

---

### STEP 2: Pending Cleanup

**Module:** `kn.modl.00.01.19_pend-clnp.md`

**Purpose:** Delete expired folders from pending deletion staging

**Input:**
- `retention_days` = 14 (default)

**Output:**
- `deleted_count` = number of folders deleted
- `deleted_paths` = list of deleted folder paths
- `kept_count` = number of folders kept

**Location:** `ar\pend\{YYMMDD}\`

---

### STEP 3: Empty Folder Cleanup

**Module:** `kn.modl.00.01.19_fldr-clnp.md`

**Purpose:** Remove empty folders after file operations

**Input:**
- `target_path` = `C:\dev`
- `recursive` = true

**Output:**
- `removed_count` = number of folders removed
- `removed_paths` = list of removed folder paths

**Note:** Runs in loop until no empty folders remain (handles nested empties)

---

### FINAL: Aggregate Results

**Purpose:** Combine results from all modules for reporting

**Output:**
```json
{
  "delta_scan": {
    "modified_files_count": 42,
    "since_timestamp": "260204-1800"
  },
  "pending_cleanup": {
    "deleted_count": 3,
    "kept_count": 5
  },
  "folder_cleanup": {
    "removed_count": 12
  },
  "run_timestamp": "260205-0930",
  "success": true
}
```

---

## n8n Integration

This workflow is automated via `proc-housekeep.json`:

```
Webhook Trigger
    ↓
step-1-delt-scan → calls mod-delt-scan
    ↓
step-2-pend-clnp → calls mod-pend-clnp
    ↓
step-3-fldr-clnp → calls mod-fldr-clnp
    ↓
aggregate-results → combine outputs
    ↓
respond-webhook → return summary
```

### Webhook Endpoint

```
POST /webhook/housekeep
Authorization: Bearer {token}
```

### Trigger Options

| Trigger | Schedule |
|---------|----------|
| Daily | 02:00 ET (off-hours) |
| Post-session | After session cleanup |
| Manual | On-demand via webhook |

---

## Quick Reference

```
HOUSEKEEPING ORCHESTRATION:

STEP 1: mod-delt-scan   → Find modified files
STEP 2: mod-pend-clnp   → Delete expired pending folders
STEP 3: mod-fldr-clnp   → Remove empty folders
FINAL:  aggregate       → Report summary
```

---

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| file-mant | Calls housekeep for cleanup after maintenance |
| file-comp | Delta scan feeds into compliance checking |

---

## Next Workflow Options

```
1. Check compliance → kn.wkfl.00.01.19_file-comp.md
2. File maintenance → kn.wkfl.00.01.19_file-mant.md
3. End session → mod-sess-doc
```
