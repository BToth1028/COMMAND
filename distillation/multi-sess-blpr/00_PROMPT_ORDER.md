# Multi-session blueprint — prompt chain and options

## Recommended delivery (fewer round-trips)

1. **Message A — `promt_mult-sess-blpr_1+2-merged.txt`**: handoff + machine-safe JSON acknowledgment + full charter. Attach the **corpus in the same message** as the merged prompt, or post the model’s one-line JSON ack first, then the corpus in the very next user message (your host decides).
2. **Message B — `promt_mult-sess-blpr_3+4-merged.txt`** (preferred) **or** `promt_mult-sess-blpr_3-4.txt` then `promt_mult-sess-blpr_4-4.txt` in two user messages: Step 0, Block 1, `OPERATOR_ALERT` rules, Block 2, Block 3. The merged file is a single paste for the second phase after Message A and corpus are in thread.

After the run completes, the model may emit **`BUDGET_ACTUALS`** (one line) if Step 0 had an estimate and the final output materially differs, so you can judge drift for the next run.

**Legacy four-message mode** still works: send old `1-4` → user sends corpus → `2-4` → `3-4` → `4-4`. The merged file exists so you can drop the empty “Understood” round.

## Machine-safe acknowledgment (replaces one-word `Understood`)

The model must reply with **one line of minified JSON** and nothing else, for example:

```json
{"ack":"ready","agent":"mult-sess-blueprint","schema_mode":"full","metric_story":true,"version":1}
```

- `ack` must be `"ready"`.
- `schema_mode`: `"full"` (default) or `"reduced"` — see **Schema modes** below.
- `metric_story`: `true` if the subject is expected to carry H/W/CE/VC; `false` to skip metric dimensions in scoring and in metric-heavy blueprint sections (they become stubs: “N/A — no metric story in subject/corpus”).

Your automation can `JSON.parse` that line, branch on `metric_story` / `schema_mode`, and only then post the corpus and charter.

## Schema modes: `full` vs `reduced` — what they are for

| Mode | What changes | If you only use `full` |
|------|----------------|-------------------------|
| **`full`** | All sections (A–G), full Block 1 scoring /25 including dimension 5, Block 2 registry includes quantitative candidates, Block 3 section 6 is populated with enforceable H/W/CE/VC when the corpus supports them. | For subjects that are (or should become) a governed ontology with metrics and collapse discipline. |
| **`reduced`** | Same *pipeline* (Step 0 → Block 1 → 2 → 3) but: narrative or explanatory material is **not** forced into full S₀/CWA/K₀ depth when the corpus does not support it. You still run A–G honestly: **G (U#) and a clear scope / closed-world story** stay mandatory. **B–E** are as deep as the text allows—possibly thin. Dimension 5 is N/A unless metrics appear. Block 3 is shorter: collapse and K₀ appear **only if grounded**; “merge these specs” runs may be mostly **scope + U# + traceability + tests for what is actually checkable**. | Use when `{{SUBJECT}}` is documentation consolidation, playbooks, or design notes **without** a constitutional / validator / metrics story. |

**Implications if you disallow `reduced`:** every run is pushed through the same ontology thickness. You get bloat, fake precision, or empty sections labeled as if they were enforced. **Implications if you allow `reduced`:** the deliverable stays honest: smaller blueprint, fewer fake validators, but you must still not skip U# or traceability when conflicts exist.

**Why a mode flag is needed (not just “try your best”):** agents optimize for *looking complete*. Without an explicit `reduced` branch, a doc-merge or playbook session will be padded with template-shaped sections (S₀, K₀, H/W/CE/VC) that are not corpus-grounded, which is worse than a short, testable spec. The flag is an instruction to the model: *compress the ceremonial shell when the subject is not a kernel design task*.

## Tier 3 and low-signal material — **alert, never auto**

If the model proposes to *summarize, park, batch-ignore, or collapse away* large amounts of **Tier 3 (low-signal)** or out-of-tier content (or to split the job into trunks), it must first emit a single **`OPERATOR_ALERT`** block: what it saw, what it *would* do, risks of proceeding vs. chunking vs. stopping. It **must not** perform that deprioritization in the same turn. It **waits** for explicit operator instruction (e.g. proceed with parking, stop and split, adjust tier thresholds).

This is not optional automation: default is **stop after the alert** until the operator answers.

## File map

| File | Role |
|------|------|
| `00_PROMPT_ORDER.md` | This file — chain, JSON ack, modes, operator alert policy. |
| `promt_mult-sess-blpr_1+2-merged.txt` | Handshake + charter (use with corpus in Message A). |
| `promt_mult-sess-blpr_1-4.txt` | Handshake only (legacy 4-step chain, message 1). |
| `promt_mult-sess-blpr_2-4.txt` | Charter only (legacy message after corpus: message 2). |
| `promt_mult-sess-blpr_3-4.txt` | Step 0 + `OPERATOR_ALERT` + Block 1. |
| `promt_mult-sess-blpr_4-4.txt` | Block 2 (3-step merge) + Block 3. |
| `promt_mult-sess-blpr_3+4-merged.txt` | **3-4 and 4-4 concatenated** (recommended Message B). |

You can also paste 3-4 and 4-4 as two user messages in order.
