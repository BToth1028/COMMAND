---
name: create-document
description: >-
  Master-router DOCUMENT execution child. Materializes one new document file
  from a frozen handoff JSON (native UTF-8 write). Pair with master-router
  dispatch terminus SUCCESS_ATOMIC after gates pass. Never silently overwrite.
---

# Create-document

## Mission

Execute **`DOCUMENT`** creation emitted by **`@master-router`**: accept **`handoff_envelope`** JSON, validate **`target_path_absolute`** + subtype, resolve document bytes from frozen fields or stdin, write atomically (mkdir parents), return structured stdout JSON.

## Scope / Non-scope

**In scope:** JSON handoffs aligned with **`handoff_envelope_schema`** subset (**`request_type`**, **`target_path_absolute`**, **`subtype_or_operation_or_language_label`**, frozen optional/required body fields).

**Out of scope:** router classification, CODE artifacts, RULE/SKILL/COMMAND authoring, content correctness beyond faithfully writing supplied bytes.

## Authority

- **`C:\Users\rtoth\.cursor\commands\master-router\COMMAND.md`**
- **`C:\Users\rtoth\.cursor\commands\create-document\create-document.yaml`** (declarative twin)

## Inputs

| Input | Required |
|-------|----------|
| `--handoff-json <absolute-path>` | Yes |
| `--overwrite` | No (explicit opt-in) |
| `--stdin-body` | No |

Body resolution order:

1. **`optional_inputs_frozen.body_or_content_brief`**
2. **`required_inputs_frozen.body`**
3. stdin when **`--stdin-body`**

## Algorithm (deterministic)

1. Parse JSON strictly UTF-8.
2. Require **`request_type == DOCUMENT`** else HALT.
3. Require absolute **`target_path_absolute`** else HALT.
4. Require non-empty subtype string else HALT.
5. If target exists and **`--overwrite`** absent → HALT.
6. Resolve body per precedence above else HALT.
7. **`mkdir -p`** parents; write file UTF-8 LF.
8. Emit single stdout JSON line **`{"status":"written","path":...,"subtype":...}`**.

## Output contract

- Success: one JSON object on stdout.
- Failure: **`HALT: ...`** messages on stderr, non-zero exit code.
- Forbidden: silent overwrite, guessing subtype from extension alone.

## Validation gates

Document gates **`VDOC01–VDOC04`** live in **`create-document.yaml`**.

## Error keys

| Key | Meaning |
|-----|---------|
| MISSING_HANDOFF | JSON missing / unreadable |
| TARGET_EXISTS_NO_OVERWRITE | Path collision |
| BODY_UNRESOLVED | No body fields and no stdin |

## Anti-drift

- Never default **`--overwrite`** true.
- Never treat extension as authoritative substitute for subtype field.
- Never branch on undocumented **`request_type`** values.

## Invocation

```powershell
python "C:\Users\rtoth\.cursor\commands\create-document\create-document_run.py" `
  --handoff-json "C:\path\to\handoff.json"
```

Optional stdin body:

```powershell
Get-Content .\body.yaml -Raw | python ... --handoff-json .\handoff.json --stdin-body
```
