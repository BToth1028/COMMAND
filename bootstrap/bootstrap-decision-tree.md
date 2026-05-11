# Bootstrap Protocol Decision Tree

Derived from:

- `C:/Users/rtoth/.cursor/commands/bootstrap/bootstrap-start.yaml`
- `C:/Users/rtoth/.cursor/commands/bootstrap/bootstrap-ingest.yaml`
- `C:/Users/rtoth/.cursor/commands/bootstrap/bootstrap-audit.yaml`
- `C:/Users/rtoth/.cursor/commands/bootstrap/bootstrap-init.yaml`
- `C:/Users/rtoth/.cursor/commands/bootstrap/bootstrap-checkpoint.yaml`
- `C:/Users/rtoth/.cursor/commands/bootstrap/bootstrap-finalize.yaml`
- `C:/Users/rtoth/.cursor/commands/bootstrap/COMMAND.md`
- `C:/code/_PARA/governance/ontology/tree-structures/ascii-decision-tree-spec.md`

This file is a generated explanatory map of the bootstrap lifecycle. It is not
authority. Command YAMLs and `COMMAND.md` remain authoritative.

```text
START bootstrap-start
│
└─► SELECT PRIOR STATE
    │   Purpose: decide whether this session resumes, recovers, or starts clean.
    │   Rule: the agent never picks silently; operator supplies or confirms.
    │
    ├─► IF exact bootstrap path supplied
    │   │   The operator gave an @ref, absolute path, or exact YAML filename.
    │   │   The supplied file becomes the resume source.
    │   │   project_root is the fourth parent above the file.
    │   └────────────────────────────────────────────────────────────► [INGEST]
    │
    ├─► ELSE IF existing project supplied
    │   │   The operator identified a project, not a session file.
    │   │   Inspect {project_root}/02_working/chat-sessions/bootstrap/.
    │   │
    │   ├─► IF lock present
    │   │   │   A prior session may have ended incorrectly.
    │   │   │   Operator chooses whether to remove the stale lock or halt.
    │   │   │
    │   │   ├─► operator chooses halt ───────────────────────────────► [STOP]
    │   │   │
    │   │   └─► operator chooses remove lock
    │   │       │   Verify the locked session has a corresponding bootstrap.
    │   │       │
    │   │       ├─► IF locked bootstrap missing ─────────────────────► [RECOVERY]
    │   │       │
    │   │       └─► ELSE bootstrap exists ───────────────────────────► fall through to scan
    │   │
    │   └─► SCAN CANONICAL LIVE DIR
    │       │   Only canonical bootstrap YAMLs count.
    │       │   Supplemental derivatives are not auto-selected.
    │       │
    │       ├─► IF multiple candidates
    │       │   │   Ambiguous resume state; list candidates.
    │       │   │   Operator chooses the exact file.
    │       │   └────────────────────────────────────────────────────► [OPERATOR-PICK]
    │       │
    │       ├─► ELSE IF exactly one candidate
    │       │   │   Agent may propose it, but cannot assume it.
    │       │   │
    │       │   ├─► operator confirms ───────────────────────────────► [INGEST]
    │       │   │
    │       │   └─► operator declines ───────────────────────────────► [STOP]
    │       │
    │       └─► ELSE zero candidates
    │           │   Existing project has no usable prior bootstrap.
    │           │   Operator decides whether this becomes session-zero.
    │           │
    │           ├─► operator confirms session-zero ──────────────────► [INIT]
    │           │
    │           └─► operator declines ───────────────────────────────► [STOP]
    │
    ├─► ELSE IF new project declared
    │   │   No prior bootstrap is expected.
    │   │   Collect project_name and absolute project_root.
    │   └────────────────────────────────────────────────────────────► [INIT]
    │
    └─► ELSE request is ambiguous
        │   The command cannot infer intent.
        │   Surface the three valid start paths and wait.
        └────────────────────────────────────────────────────────────► ↺ loop SELECT PRIOR STATE

[OPERATOR-PICK]
│
├─► operator selects one bootstrap
│   │   Selection is explicit; resume can begin.
│   └────────────────────────────────────────────────────────────────► [INGEST]
│
└─► operator declines all candidates
    │   No valid resume target remains.
    └────────────────────────────────────────────────────────────────► [STOP]

[INGEST]
│
│   Purpose: load the selected prior bootstrap and prove it is usable.
│   Rule: ingest does not choose files; selection already happened.
│
├─► IF bootstrap loads, parses, and passes integrity checks
│   │   Prior session state is available.
│   │   Count active work, open issues, and stale audit items.
│   └────────────────────────────────────────────────────────────────► [AUDIT]
│
└─► ELSE bootstrap missing, broken, or inconsistent
    │   Do not repair in place.
    │   Do not reconstruct from agent memory.
    └────────────────────────────────────────────────────────────────► [RECOVERY]

[RECOVERY]
│
│   Purpose: recover continuity without active _ar dependency.
│   While archive housekeeping is deferred, use loose live-dir bootstraps.
│
├─► IF usable loose prior bootstrap exists
│   │   Select deterministically from valid live-dir candidates.
│   │   Generate and validate a supplemental bootstrap.
│   └────────────────────────────────────────────────────────────────► [INGEST]
│
├─► ELSE no usable prior state; operator confirms session-zero
│   │   Recovery cannot preserve history.
│   │   Start clean with known project_name and project_root.
│   └────────────────────────────────────────────────────────────────► [INIT]
│
└─► ELSE no usable prior state and no confirmation
    │   Halt rather than guessing.
    └────────────────────────────────────────────────────────────────► [STOP]

[AUDIT]
│
│   Purpose: classify context files before work begins.
│   Audit is read-only; it flags drift but does not fix or delete anything.
│
├─► IF audit completes
│   │   Classify command sources, generated mirrors, schema/example,
│   │   validator, and referenced context files.
│   └────────────────────────────────────────────────────────────────► [INIT]
│
└─► ELSE audit halts
    │   Ingest succeeded, but the session is not ready for project work.
    └────────────────────────────────────────────────────────────────► [STOP]

[INIT]
│
│   Purpose: create the new in-memory bootstrap for this session.
│   This is where carry-forward rules are applied.
│
├─► IF session-zero
│   │   Create all required sections with valid empty values.
│   │   No carry-forward occurs.
│   │   Create only the live bootstrap directory if missing.
│   └────────────────────────────────────────────────────────────────► [WORK]
│
└─► ELSE prior state exists
    │   Carry ACTIVE, BLOCKED, and DEFERRED tasks only.
    │   Drop DONE/CANCELLED tasks and all prior decisions.
    │   Carry open issues and refreshed audit context.
    └────────────────────────────────────────────────────────────────► [WORK]

[WORK]
│
│   Purpose: normal project work after bootstrap initialization.
│   The in-memory bootstrap must stay aligned with reality.
│
├─► IF task, decision, issue, scope, or environment changes
│   │   Checkpoint updates in-memory state only.
│   └────────────────────────────────────────────────────────────────► [CHECKPOINT]
│
└─► IF session is ending
    │   Finalize persists the in-memory bootstrap to disk.
    └────────────────────────────────────────────────────────────────► [FINALIZE]

[CHECKPOINT]
│
│   Purpose: prevent drift during the session.
│   Checkpoint never writes to disk; finalize owns persistence.
│
├─► IF update is unambiguous and validates
│   │   Add tasks/issues/this-session decisions as needed.
│   │   Ambiguous task status defaults to ACTIVE with task note.
│   └────────────────────────────────────────────────────────────────► ↺ loop WORK
│
└─► ELSE conflict requires canonical answer
    │   Conflicting state is surfaced instead of silently resolved.
    └────────────────────────────────────────────────────────────────► [STOP]

[FINALIZE]
│
│   Purpose: write the lean finalized bootstrap.
│   Refresh environment, audit, issues, and session summary.
│
├─► IF validation passes and write succeeds
│   │   Write {ProjectName}_{YYMMDD-HHMM}.yaml to the canonical live path.
│   │   Never overwrite an existing bootstrap.
│   └────────────────────────────────────────────────────────────────► [SESSION-COMPLETE]
│
├─► ELSE IF serialization/write failure risks content loss
│   │   Normal output rules yield to preservation.
│   │   Emit structured emergency fallback payload.
│   └────────────────────────────────────────────────────────────────► [EMERGENCY-FALLBACK]
│
└─► ELSE validation fails
    │   Do not write partial or invalid bootstrap content.
    └────────────────────────────────────────────────────────────────► [STOP]

[EMERGENCY-FALLBACK]
│
└─► dump structured recovery payload
    │   Include failure type, exact error, intended path,
    │   and YAML/internal state needed to preserve continuity.
    └────────────────────────────────────────────────────────────────► [STOP]
```
