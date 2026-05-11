---
name: context-bootstrap
description: >-
  Thin Cursor slash-command pointer. Authoritative bootstrap protocol
  (governance prose, schema, validator, phase contracts, manifest) lives
  only under 46.05-bootstrap-command-contracts. Open those paths — this
  file is not a second source of truth.
---

# context-bootstrap

## Canonical bundle (single source of truth)

Base path (JDex ID **46.05**):

`40-49-ai-agents-and-prompts/46-memory-and-bootstrap/46.05-bootstrap-command-contracts/`

| Artifact | File |
|----------|------|
| Governance + embedded spec | `COMMAND.md` |
| Command index + dependency notes | `manifest.yaml` |
| Session phases | `bootstrap-start.yaml`, `bootstrap-ingest.yaml`, `bootstrap-audit.yaml`, `bootstrap-init.yaml`, `bootstrap-checkpoint.yaml`, `bootstrap-finalize.yaml` |
| Lifecycle diagram (non-authority) | `bootstrap-decision-tree.md` |
| Bootstrap YAML template / comments | `schema.yaml` |
| Validator | `validate_bootstrap.py` |
| Example finalized bootstrap | `FormBuilder_260402-2145.yaml` |

Absolute paths on a typical clone:

- `C:/dev/40-49-ai-agents-and-prompts/46-memory-and-bootstrap/46.05-bootstrap-command-contracts/COMMAND.md`

## Cursor / profile

See `43.02-commands/README.md`: optional junction from `%USERPROFILE%\.cursor\commands\...` into this repo tree so the IDE loads the same files without duplicating content.
