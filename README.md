# 43.02 — Cursor slash commands (in-repo canonical)

Author **`COMMAND.md`** trees live here — one subfolder per command (e.g. **`audit-engine/`**). **`jdex.yaml`** declares this ID as canonical for repo edits; profile pick-up mirrors via **`%USERPROFILE%\.cursor\commands\`** (same folder layout).

## Optional directory junctions (Windows)

For IDE navigation without duplicating bytes, you may add **directory junctions** at the **root of this ID** pointing at the matching folder under the profile:

**`%USERPROFILE%\.cursor\commands\<name>\`**

Junction basenames are **gitignored** (see **`.gitignore`**) so Git does not traverse them when **`core.symlinks`** is false. After a fresh clone, recreate junctions (examples):

```powershell
New-Item -ItemType Junction `
  -Path "c:\dev\40-49-ai-agents-and-prompts\43-rules-skills-subagents\43.02-commands\master-router" `
  -Target "$env:USERPROFILE\.cursor\commands\master-router"

New-Item -ItemType Junction `
  -Path "c:\dev\40-49-ai-agents-and-prompts\43-rules-skills-subagents\43.02-commands\create-facet" `
  -Target "$env:USERPROFILE\.cursor\commands\create-facet"
```

During consolidation, content that matched the profile copy byte-for-byte was removed from this tree; divergent copies were moved to **`%USERPROFILE%\.cursor\commands\_staging`** (same relative paths) for manual review.

## Related single-home paths

- **User skills (Cursor):** `%USERPROFILE%\.cursor\skills-cursor` — conflicts, if any, under `_staging`.
- **Canonical skill bundles in this repo:** `43.01-custom-skills\<skill-name>\` (e.g. **`ontology-tutor/`**). Profile often uses a **junction** `%USERPROFILE%\.cursor\skills-cursor\<skill-name>\` → that JDex folder. Session bootstrap YAML remains **`46.01-bootstrap-yamls`** (flat).
- **Superpowers plugin skills:** `%USERPROFILE%\.cursor\plugins\cache\cursor-public\superpowers\<plugin-id>\skills`

Bootstrap **protocol** YAMLs that must stay in-repo for JDex parity remain under **`46.05-bootstrap-command-contracts`**, not here.
