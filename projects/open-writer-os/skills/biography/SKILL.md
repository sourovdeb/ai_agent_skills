---
name: biography
description: Specialized skill pack for biography and memoir writing in Open Writer OS. Use when the writer is working from lived experience — their own life or another person's — and needs evidence-status discipline, interview-to-prose flow, and privacy rules for real people. Combine with the --memoir flag.
---

# Biography & Memoir Skill Pack

Load this pack with `run <mode> --skill biography --memoir`. The `--memoir`
flag adds the eight evidence statuses to the system prompt; this pack adds
the workflow around them.

## Evidence statuses (from the MISHU Writer OS memoir mode)

Label important real-world material with exactly one of:

| Status | Meaning |
|---|---|
| REMEMBERED | The writer's own memory of it |
| DOCUMENTED | A source exists (letter, photo, record, receipt) |
| CORROBORATED | An independent account agrees |
| RECONSTRUCTED | Built from partial memory; flagged as such |
| INFERRED | Concluded from evidence, not directly known |
| UNCERTAIN | The writer is not sure |
| DISPUTED | Accounts conflict; keep both |
| FICTIONALIZED | Changed deliberately for the published version |

Rules: never upgrade REMEMBERED to DOCUMENTED without a source. Never
invent details to fill gaps — write "I don't remember" or label the gap
UNKNOWN/UNCERTAIN. Preserve incompatible accounts; do not silently pick
one. When the prose needs a detail the record lacks, mark it RECONSTRUCTED
in the text or the canon ledger, not as fact.

## Privacy rules for real third parties

- Never publish identifying details about a living person without the
  writer's explicit, informed consent.
- Propose anonymization (changed name, merged composite, withheld detail)
  whenever a living person is identifiable.
- Treat the subject's own draft as private by default; the writer decides
  what is shared.
- For deceased subjects, still prefer the minimum identifying detail the
  story needs.
- If the writer asks to include sensitive material (health, finances,
  trauma, legal matters), remind them once of the consent question, then
  follow the writer's decision — the writer owns the publication choice.

## Interview-to-prose flow

1. **Capture** — Transcripts, notes and recordings go in `NOTES/` as raw
   material. Do not edit them into prose in the same pass.
2. **Tag** — Run CONTINUITY with the memoir flag over the notes: label
   each important memory with an evidence status and flag contradictions
   between accounts.
3. **Select** — Run DISCOVER or ARCHITECT to choose which memories carry
   the book and in what order. Selection is a meaning decision; the writer
   makes it.
4. **Draft** — Run DRAFT scene by scene. Prose may dramatize ( FICTIONALIZED
   composite scenes, compressed time) but the canon ledger must record what
   was changed and why.
5. **Audit** — Run CONTINUITY again over the manuscript against the tagged
   notes: dates, ages, names, and every claim that presents memory as
   verified fact.

## Mode adaptations

- **DISCOVER** — Elicit, don't interrogate. Ask one open question at a
  time. Silence is data. Never push the writer to "remember more."
- **ARCHITECT** — A memoir's structure is thematic or chronological, not
  plot-driven. Offer both and let the writer choose; do not force a
  three-act shape onto a life.
- **SCENE_PLAN** — A memoir scene is a *felt* scene: what the writer
  believed at the time matters more than what they know now. Plan the gap
  between then-knowledge and now-knowledge.
- **DRAFT** — Write in the writer's voice, learned from prose the writer
  has approved (STYLE_TARGET.md), not from generic "literary memoir" voice.
  First person is common but not mandatory; the writer chooses.
- **DIALOGUE** — Reconstructed conversation must be labelled. Prefer
  "she said, in substance" over invented exact quotes when the exact words
  are not DOCUMENTED.
- **DESCRIBE** — Sensory detail is a memoir's evidence. A specific object,
  smell or sound often carries more truth than a summary of the era.
- **DEEPEN** — Interiority must come from the writer's own reflection,
  not the AI's interpretation of what the writer "must have felt."
- **COMPRESS** — Memoirs compress time constantly. Keep the cuts visible
  and record in the canon ledger what was elided.
- **CONTINUITY** — Audit dates, ages (a person's age at each dated event),
  relationships, locations, and evidence-status labels. Flag any passage
  where RECONSTRUCTED or UNCERTAIN material reads as verified fact.
- **REVISE** — Preserve the writer's voice and their uncertainty. Do not
  "fix" a hedge ("I think", "maybe") into a confident statement.
- **CANON_UPDATE** — The canon ledger for a memoir is an *evidence* ledger:
  each entry carries its evidence status and its source.
- **PROFILE_UPDATE** — Record the writer's voice preferences and any
  corrections to reconstructed material.

## Anti-patterns to refuse

- Presenting a reconstructed scene as if it were documented.
- Smoothing over a contradiction between two family accounts.
- Inventing dialogue and passing it off as remembered.
- Adding a moral or lesson the writer did not state.
- Exposing a living third party's identifying details without consent.
- Treating the writer's unpublished draft as publishable by default.
