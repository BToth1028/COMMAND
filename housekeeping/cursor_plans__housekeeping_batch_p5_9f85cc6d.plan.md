---
name: Housekeeping batch P5
overview: Knock out 3 housekeeping items (link tblAuditLog, fix Cardinality truncation, resolve axioms doc gaps) as a batch, then update session documentation.
todos:
  - id: preflight
    content: Run phase3_audit.py to capture baseline state and check trg_attrschema_vocabulary_update existence
    status: completed
  - id: cardinality-verify
    content: Verify tblEdgeType.Cardinality values in live SQLite DB
    status: completed
  - id: cardinality-fix
    content: Fix Cardinality truncation if confirmed (UPDATE tblEdgeType)
    status: completed
  - id: trigger-vocab-update
    content: Install trg_attrschema_vocabulary_update if missing from DB, add to phase2_install_triggers.py
    status: completed
  - id: axioms-frontmatter
    content: Update axioms doc frontmatter (timestamp, remove version)
    status: completed
  - id: link-auditlog-vba
    content: Add LinkAuditLog utility sub to modNodeManager.bas
    status: completed
  - id: update-todo-bootstrap
    content: "Update TODO (mark items complete, fix rule #12) + Bootstrap"
    status: completed
  - id: session-doc
    content: Create new T1 session doc for this batch
    status: completed
  - id: postflight
    content: Run phase3_audit.py final verification
    status: completed
isProject: false
---

# P5 -- Housekeeping Batch (tblAuditLog Link + Cardinality Fix + Axioms Doc)

## Pre-flight

Run `python tp/phase3_audit.py` to capture baseline state. This will also reveal whether `trg_attrschema_vocabulary_update` exists in the live DB (the audit expects it but no install script creates it).

---

## Item 1: Link tblAuditLog as ODBC Table in Access

**Problem**: `tblAuditLog` exists in SQLite but is not linked in the `.accdb` front-end.

**Approach**: Add a `LinkAuditLog` utility sub to [modNodeManager.bas](pr/Form-Builder_Access/da/uire/03.07/08/accdb/migration/modNodeManager.bas) (which already hosts `LogAudit` and `GetAuditSessionId`). The function will:

- Read the existing ODBC connection string from any already-linked table (e.g., `tblNode`)
- Use `DAO.TableDef` to create and append the linked table
- Idempotent: drops existing link if present before re-linking

```vb
Public Sub LinkAuditLog()
    Dim db As DAO.Database
    Dim tdf As DAO.TableDef
    Dim connStr As String

    Set db = CurrentDb
    connStr = db.TableDefs("tblNode").Connect

    On Error Resume Next
    db.TableDefs.Delete "tblAuditLog"
    On Error GoTo 0

    Set tdf = db.CreateTableDef("tblAuditLog")
    tdf.Connect = connStr
    tdf.SourceTableName = "tblAuditLog"
    db.TableDefs.Append tdf
    db.TableDefs.Refresh

    Set tdf = Nothing
    Set db = Nothing
End Sub
```

**User action required**: After importing the updated module into Access, run `Call LinkAuditLog` once in the Immediate window.

---

## Item 2: Fix tblEdgeType.Cardinality Truncation

**Problem**: All 7 `tblEdgeType` rows show `many-to-ma` in AccessDump CSVs. Expected: `many-to-many`.

**Step 1 -- Verify live SQLite values**:

```python
import sqlite3
DB = r'C:\dev\pr\Form-Builder_Access\da\uire\03.07\08\accdb\FormBuilder_Def.sqlite'
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT EdgeType_KEY, DisplayName, Cardinality FROM tblEdgeType")
for row in cur.fetchall():
    print(row)
conn.close()
```

**Step 2 -- Fix if truncated**:

```sql
UPDATE tblEdgeType SET Cardinality = 'many-to-many' WHERE Cardinality = 'many-to-ma';
```

`tblEdgeType` is a Schema/Reference table, not an authority table -- no triggers block UPDATE.

**VBA impact**: None. The VBA cardinality enforcement in [modEdgeManager.bas](pr/Form-Builder_Access/da/uire/03.07/08/accdb/migration/modEdgeManager.bas) lines 77-100 uses `Left(cardinality, ...)` pattern matching. `many-to-many` falls through (no constraint = correct), same behavior as `many-to-ma`.

**Note on seed_layer0.py**: The seed script uses short notation (`1:N`, `N:N`). This is a separate mismatch from the `many-to-many` long form the VBA expects. Since `seed_layer0.py` is legacy (NOT to be re-run per non-negotiable rule #6), no change needed there.

---

## Item 3: Axioms Doc Resolution

**File**: [kn.prml.07.08.19_axioms.md](va/gv/RKM/pr/prod/Form-Builder/T2_Project/Access/Primals/kn.prml.07.08.19_axioms.md)

### Original 3 issues -- assessment

All 3 issues listed in the TODO appear **already resolved**:

1. **Trigger name mismatch** -- File uses correct names (`trg_nodeattr_schema_binding`, etc.)
2. **Enforcement map incomplete** -- EM.6 includes `trg_attrschema_vocabulary` + `trg_attrschema_vocabulary_update`; EM.7 includes `trg_nodeattr_boolean_rule`
3. **IV.2 wording** -- Says "Only Nodes may own attributes" which matches enforcement

### NEW issues found during exploration

- **trg_attrschema_vocabulary_update**: Referenced in axioms doc (EM.6, trigger inventory line 140) and expected by `phase3_audit.py` (line 156), but **not created by any install script**. `phase2_install_triggers.py` only installs the INSERT variant. Must verify if it exists in the live DB. If missing: install it (BEFORE UPDATE on tblAttrSchema with same vocabulary check). If present (from manual install): create a script to reproduce it.
- **Frontmatter `updated` timestamp**: Says `260210-1600` but file content reflects 260212 changes (20 triggers). Update to current session timestamp.
- **Frontmatter `version: "V02"**`: Violates axiom D4 (no version suffixes). Remove field.

### Action

1. Run audit to check if trigger exists
2. If missing: install via Python script, add to `phase2_install_triggers.py`
3. Update frontmatter (timestamp, remove version)
4. Mark original 3 TODO items as resolved with annotation

---

## Item 4: Update TODO and Session Docs

- **TODO** ([rkm.pr.prod.form-bld-accs.ToDo_07.08.19.md](va/gv/RKM/pr/prod/Form-Builder/T1_Session/Access/rkm.pr.prod.form-bld-accs.ToDo_07.08.19.md)):
  - Mark items 1-3 complete
  - Fix non-negotiable rule #12: "15 triggers" -> "20 triggers"
  - Update timestamp
- **Bootstrap** ([rkm.pr.prod.form-bld-accs.T1_07.08.19.md](va/gv/RKM/pr/prod/Form-Builder/T1_Session/Access/rkm.pr.prod.form-bld-accs.T1_07.08.19.md)):
  - Update "What the Next Agent Must Know" with tblAuditLog linked, Cardinality fixed, doc issues resolved
  - Update trigger count documentation references
- **New session doc**: `rkm.pr.prod.form-bld-accs.T1_07.08.19_{timestamp}.md` capturing this batch

---

## Execution Order

```
1. phase3_audit.py          (baseline + trigger existence check)
2. Verify SQLite Cardinality (inline python)
3. Fix Cardinality if needed (UPDATE)
4. Install trg_attrschema_vocabulary_update if missing
5. Update axioms doc frontmatter
6. Add LinkAuditLog to modNodeManager.bas
7. Update TODO + Bootstrap
8. Create session doc
9. phase3_audit.py          (final verification)
```
