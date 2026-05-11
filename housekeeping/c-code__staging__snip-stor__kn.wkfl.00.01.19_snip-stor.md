---
id: kn.wkfl.00.01.19_snip-stor
title: 'Workflow: Snippet Storage'
description: Workflow for adding new code snippets to li/code/snippets/ library
type: documentation
category: architecture
status: working
created: 260112-1545
updated: 260202-1630
author: Claude-Opus-4.5
owner: operator
tags:
- workflow
- snippets
- library
- storage
- deduplication
relations:
- Session Lifecycle
- Master Workflow Index v2.0
- kn.wkfl.00.01.19_code-crea.md
- kn.wkfl.00.01.19_quar-proc.md
source: Snippet library design session 260112
dependencies: []
automation_hooks: []
evidence_id_range: ''
coverage_window_start: ''
coverage_window_end: ''
completeness: 100%
project_name: ''
uuid: snip-stor-260112
checksum_sha256: pending
mirror_yaml: ''
platform: Cursor
make: Anthropic
model: claude-opus-4.5
session_id: ''
governance_node:
  node_id: kn.wkfl.00.01.19_snip-stor
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
# Workflow: Snippet Storage

**Purpose:** Add new code snippets to the library with proper deduplication and indexing
**Type:** Workflow - steps for storing reusable code
**Scope:** Any reusable code pattern, function, or utility

---

## Library Location

```
li/code/snippets/
├── index.md                <- Master index
├── by-language/            <- Language indexes
├── by-pattern/             <- Pattern indexes
└── snip-{hash}.md          <- Individual snippets
```

---

## When To Use

- After creating new reusable code
- During quarantine processing (snippet extraction)
- When refactoring code into reusable patterns
- When documenting existing code patterns

---

## Todo List

```
[ ] STEP 1: DEDUPLICATION CHECK
    [ ] 1.1 Normalize the code (strip whitespace, comments)
    [ ] 1.2 Generate hash: md5(normalized)[:12]
    [ ] 1.3 Check if snip-{hash}.md already exists
    [ ] 1.4 If exists → Update existing (add context)
    [ ] 1.5 If NOT exists → Proceed to Step 2

[ ] STEP 2: CLASSIFY SNIPPET
    [ ] 2.1 Determine language
    [ ] 2.2 Determine type (function/class/pattern/utility/config)
    [ ] 2.3 Identify patterns (file-io, api-calls, etc.)
    [ ] 2.4 Estimate complexity (simple/moderate/complex)
    [ ] 2.5 Extract dependencies

[ ] STEP 3: GENERATE TITLE
    [ ] 3.1 Extract function/class name if applicable
    [ ] 3.2 Create descriptive title
    [ ] 3.3 Ensure uniqueness

[ ] STEP 4: CREATE SNIPPET FILE
    [ ] 4.1 Use template format
    [ ] 4.2 Fill all frontmatter fields
    [ ] 4.3 Add code block
    [ ] 4.4 Add usage example
    [ ] 4.5 Link to related sessions

[ ] STEP 5: UPDATE INDEXES
    [ ] 5.1 Add to by-language/{language}.md
    [ ] 5.2 Add to by-pattern/{pattern}.md (for each pattern)
    [ ] 5.3 Add to index.md (master index)

[ ] STEP 6: VERIFY
    [ ] 6.1 Confirm file created
    [ ] 6.2 Confirm indexes updated
    [ ] 6.3 Test links work
```

---

## Step 1: Deduplication Check

### 1.1-1.2 Normalize and Hash

<!-- ATOMIC: code-normalize -->
<!-- INPUTS: code_string -->
<!-- OUTPUTS: normalized_code -->
<!-- ATOMIC: code-hash -->
<!-- INPUTS: normalized_code -->
<!-- OUTPUTS: hash_string -->
Normalization removes:
- Leading/trailing whitespace per line
- Empty lines
- Comment-only lines (# // -- etc.)

```python
def normalize_code(code: str) -> str:
    lines = code.split('\n')
    normalized = []
    for line in lines:
        line = line.strip()
        if line.startswith('#') or line.startswith('//') or line.startswith('--'):
            continue
        if not line:
            continue
        normalized.append(line)
    return '\n'.join(normalized)

def hash_code(code: str) -> str:
    import hashlib
    normalized = normalize_code(code)
    return hashlib.md5(normalized.encode()).hexdigest()[:12]
```

### 1.3 Check Existence

<!-- ATOMIC: file-exists-check -->
<!-- INPUTS: filepath -->
<!-- OUTPUTS: exists_boolean -->
```powershell
$hash = "{computed-hash}"
Test-Path "C:\dev\li\code\snippets\snip-$hash.md"
```

### 1.4 If Exists: Update

If snippet already exists, ADD a new related session:

```yaml
related_sessions:
  - session_id: "existing1"
    context: "Original use case"
  - session_id: "new-session"    # ADD THIS
    context: "New context/use case"
```

This preserves deduplication while capturing new contextual uses.

### 1.5 If NOT Exists: Create New

Proceed to Step 2.

---

## Step 2: Classify Snippet

### 2.1 Language Detection

| Extension/Syntax | Language |
|------------------|----------|
| `def function():` | python |
| `function name()` | javascript |
| `CREATE TABLE` | sql |
| `param()` | powershell |
| `#!/bin/bash` | shell |

### 2.2 Type Classification

| Type | Indicators |
|------|------------|
| **function** | `def`, `function`, standalone callable |
| **class** | `class ClassName` |
| **pattern** | Algorithm, approach, template |
| **utility** | One-liner, helper, short snippet |
| **config** | Configuration, settings, constants |

### 2.3 Pattern Detection

| Pattern | Keywords |
|---------|----------|
| file-io | open, read, write, Path, pathlib |
| api-calls | requests, fetch, httpx, axios |
| data-transform | json, pandas, map, filter, parse |
| database | SELECT, INSERT, cursor, execute |
| async | async def, await, asyncio |
| error-handling | try, except, raise, catch |
| cli | argparse, click, typer, sys.argv |
| testing | pytest, assert, mock, test_ |
| config | load_config, yaml, dotenv, environ |
| logging | logging, logger, print, console.log |

### 2.4 Complexity Estimation

| Complexity | Criteria |
|------------|----------|
| simple | <= 10 lines, shallow nesting |
| moderate | 11-50 lines, some nesting |
| complex | > 50 lines, deep nesting |

### 2.5 Dependency Extraction

For Python:
```python
import re
imports = re.findall(r'^(?:from|import)\s+([\w.]+)', code, re.MULTILINE)
```

For JavaScript:
```javascript
const imports = code.match(/(?:import|require)\s*\(?['"]([^'"]+)/g)
```

---

## Step 3: Generate Title

### Naming Rules

1. Extract function/class name if present
2. Convert camelCase/PascalCase to words
3. Make descriptive and searchable

**Examples:**
- `parse_json_file` → "Parse JSON File"
- `AsyncApiClient` → "Async Api Client"
- Generic SQL → "Query {TableName}"

---

## Step 4: Create Snippet File

### Template

```markdown
---
title: "{title}"
id: "snip-{hash}"
type: "{function|class|pattern|utility|config}"
language: "{language}"
tags: [{pattern1}, {pattern2}]
dependencies: [{dep1}, {dep2}]
complexity: "{simple|moderate|complex}"
created: "{YYMMDD}"
updated: "{YYMMDD}"
related_sessions:
  - session_id: "{id}"
    context: "{brief description of use}"
---

# {Title}

## Description

{One-line description of what this does.}

## Code

```{language}
{code block - copy-paste ready}
```

## Usage Example

```{language}
{minimal example showing how to use it}
```

## Related Sessions

- [{session_id}](../sessions/{filename}.md) - {context}
```

### File Location

<!-- ATOMIC: file-write -->
<!-- INPUTS: filepath, content -->
<!-- OUTPUTS: written_path, status -->
```
li/code/snippets/snip-{hash}.md
```

---

## Step 5: Update Indexes

### 5.1 Language Index

<!-- ATOMIC: index-update -->
<!-- INPUTS: index_file, entry_data -->
<!-- OUTPUTS: updated_status -->
Add to `li/code/snippets/by-language/{language}.md`:

```markdown
- [{title}](../snip-{hash}.md) - {type}
```

### 5.2 Pattern Indexes

<!-- ATOMIC: index-update -->
<!-- INPUTS: index_file, entry_data -->
<!-- OUTPUTS: updated_status -->
<!-- NOTES: Repeat for each pattern tag -->
For each pattern tag, add to `li/code/snippets/by-pattern/{pattern}.md`:

```markdown
- [{title}](../snip-{hash}.md) - {language}
```

### 5.3 Master Index

<!-- ATOMIC: index-update -->
<!-- INPUTS: index_file, entry_data -->
<!-- OUTPUTS: updated_status -->
Add to `li/code/snippets/index.md` under "All Snippets":

```markdown
- [{title}](snip-{hash}.md) - {language} {type}
```

---

## Step 6: Verify

### Verification Checklist

| Check | Command |
|-------|---------|
| File exists | `Test-Path li/code/snippets/snip-{hash}.md` |
| Language index updated | Check by-language/{lang}.md |
| Pattern indexes updated | Check by-pattern/{pattern}.md for each |
| Master index updated | Check index.md |
| Links work | Open and verify |

---

## Quick Reference

```
SNIPPET STORAGE WORKFLOW:

1. DEDUPLICATION CHECK
   ├── Normalize code
   ├── Generate hash
   ├── Check snip-{hash}.md exists
   ├── EXISTS → Add session context only
   └── NOT EXISTS → Continue

2. CLASSIFY
   ├── Language
   ├── Type (function/class/pattern/utility/config)
   ├── Patterns (file-io, api-calls, etc.)
   ├── Complexity
   └── Dependencies

3. GENERATE TITLE
   └── Descriptive, searchable name

4. CREATE FILE
   └── li/code/snippets/snip-{hash}.md

5. UPDATE INDEXES
   ├── by-language/{lang}.md
   ├── by-pattern/{pattern}.md
   └── index.md

6. VERIFY
   └── File + indexes + links
```

---

## Automation

The extraction script can automate this:

```
to/genr/03.07/21/py/to.genr.03.07.21_snip-extr.py
```

Run periodically to extract new snippets from session logs.

---

## Next Workflow Options

```
1. Continue coding → Back to development
2. Create more code → kn.wkfl.00.01.19_code-crea.md
3. Process quarantine → kn.wkfl.00.01.19_quar-proc.md
4. End session → mod-sess-doc
```
