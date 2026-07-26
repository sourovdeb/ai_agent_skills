# Domain Skills Audit — July 5, 2026

**Scope of this pass:** productivity, legal, medical, psychology, interviewer, and writer domains, plus a targeted look at Alzheimer's/dementia and ADHD support. Each finding below was checked against the actual file contents (not just filenames) before any change was made, and nothing was rewritten unless it was genuinely thin, broken, or missing — several strong existing skills were reviewed and deliberately left untouched.

---

## Security finding (fixed immediately, independent of the rest of this audit)

**`skills/investigative-psychology/references/publishing-template.md`** contained a live Ghost CMS Admin API key and Content API key, hardcoded in plain text and already pushed to `origin/main`. This has been redacted to match the pattern already used correctly in the sibling file `references/source-directory.md` ("stored in the personal API inventory skill... use environment variables"). **The key itself should still be rotated in Ghost's admin panel** — removing it from the working tree does not remove it from git history, and if this repository has ever been public or shared, the key should be treated as already exposed.

The `investigative-psychology` skill itself was otherwise left untouched — it's a well-developed, real tool (source-tier hierarchy, conflict-of-interest checklist, publishing templates) for a different purpose than "Psychology" as scoped in this audit: it's a media/claims-auditing and auto-publishing tool, not a listening or therapeutic-support skill. It does not overlap with the new `empathetic-listening` skill.

---

## Gaps identified

| Domain | Finding |
|---|---|
| Medical/Health | **No coverage existed at all.** A repo-wide search for medical/clinical/diagnosis/symptom/patient content turned up nothing except incidental jargon (debugging "diagnoses," ELT teaching "diagnoses") and one explicit guardrail in `deep-brainstorm` that routes health topics away from itself. |
| Psychology | The only "psychology" asset (`investigative-psychology`) is a journalism/bias-audit tool, not a listening/empathy skill. Zero coverage of active listening, validation, or empathetic-response technique. |
| Productivity | `agents/Daily_Living_Productivity_Agent.md` was a single-sentence stub (86 bytes) — a title with no workflow, no anchors, no routing logic behind its own description. |
| Legal | `agents/Legal_Regulatory_Dossier_Agent.md` was a single-sentence stub (72 bytes) — no jurisdictions, no dossier structure, no citation discipline. |
| Interviewer | All six biography/interview-related files (`agents/Skilled_Biography_Interviewer_Agent.md` and five `skills/*-biography*`/`*-interview*`/`*-memory*` directories) were one-line stubs missing even YAML frontmatter — functionally non-operational as skills, despite names implying a deliberate, structured system. |
| Writer | `agents/Biography_Memoir_Writer_Agent.md` was a one-line stub. (Separately, `content-research-writer`, `doc-coauthoring.MD.md`, and `email-agent.md` are genuinely strong existing writing skills and were left untouched — the gap was specifically in Cambridge-level narrative/memoir prose, not writing generally.) |
| Alzheimer's / dementia | Zero mentions anywhere in the repo (confirmed by case-insensitive grep across all files). |
| ADHD | Zero mentions anywhere in the repo (confirmed by case-insensitive grep across all files). |
| Navigation | `_INDEX.md`, the repo's own navigation hub, referenced none of the `agents/` or `skills/` directory files at all — every file touched in this pass was previously orphaned from the index. |

## What was created or rewritten, and why

### New skills (filling genuine gaps)

- **`skills/health-information-advisor/`** (+ `references/red-flag-triage.md`) — general health information and patient education, grounded in AHA/CDC/WHO/NIA/SAMHSA red-flag thresholds (cardiac, BE-FAST stroke screen, sepsis, anaphylaxis, pediatric, obstetric, mental-health-crisis). Explicitly scoped to never diagnose, dose, or replace a clinician; always screens for emergencies before general education.
- **`skills/empathetic-listening/`** — reflective listening grounded in Rogerian person-centered technique and motivational interviewing (reflect-before-fix, OARS-style reflection-to-question ratio, validation without forced agreement), with an explicit, concrete crisis-escalation section (988, abuse disclosures, signs beyond peer-support scope).
- **`skills/alzheimers-adhd-daily-support/`** — two distinct but related sections: dementia caregiving (validation therapy over correction, environment/routine design, wandering safety, caregiver burnout) and ADHD executive-function support (externalizing time and memory, body doubling, task-initiation technique, the "Wall of Awful"/PINCH framework). Both sections explicitly route medication questions to the person's own clinician.

### Rewritten stubs (same file, same domain, real content)

- **`agents/Daily_Living_Productivity_Agent.md`** — state-based routing (clear-headed / scattered / depleted / catch-up), GTD-grounded capture-clarify-organize workflow, context-based next-action lists, and anchors/closing-ritual design; hands off to the new ADHD skill when forgetfulness looks executive-function-shaped rather than a one-off bad week.
- **`agents/Legal_Regulatory_Dossier_Agent.md`** — CREAC-structured analysis (not bare IRAC), explicit jurisdiction framing and jurisdiction matrices for multi-jurisdiction dossiers, Bluebook signal discipline, Garner's plain-language edit pass, Likelihood×Impact risk scoring for compliance dossiers, and a non-negotiable attorney-client-relationship disclaimer.
- **`agents/Skilled_Biography_Interviewer_Agent.md`** — now a persona/rules card that routes to the six-skill interview family below rather than duplicating methodology.
- **`agents/Biography_Memoir_Writer_Agent.md`** — Cambridge-level prose guidance grounded in Orwell's rules, Strunk & White, and the Cambridge University style guide, plus a concrete list of AI-tell vocabulary and sentence structures to purge on sight; works only from interview material tagged for publication.

### The biography/interview family (six files, one coherent system instead of six duplicate stubs)

All six were equally broken (one-line, no frontmatter) before this pass. Rather than write six near-identical essays, they were built as a proper progressive-disclosure system per this repo's own `skill-creator` guidance (shared reference + distinct variant skills):

- **`skills/biography-memoir-system/`** — orchestrator: which variant to use, when, and how interviewing hands off to writing.
  - **`references/interview-methodology.md`** — the shared technique (sensory/timeline elicitation, reliability coding, working with memory-impaired narrators, sensitive-material handling) that every variant below reads rather than restates.
- **`skills/biography-interview-kit-private-master/`** — complete, unfiltered archive interviews (the default starting point).
- **`skills/biography-interview-kit-public/`** — publication-intended interviews, with the private/public boundary set before the session, not after.
- **`skills/dual-biography-interview-skill-v2/`** — one session, two tagged outputs (private + publishable), so no one gets interviewed twice.
- **`skills/memory-elicitation-interview-skill/`** — right-sized for a single memory or topic rather than a full life.
- **`skills/family-memory-deep-probe-reliability/`** — elderly/memory-impaired narrators and cross-relative reliability reconciliation; this is where the Alzheimer's-aware interviewing technique (validation over correction, session-length limits, concrete memory triggers) lives, cross-referenced from `alzheimers-adhd-daily-support`.

### JSON configuration

Following this repo's own `evals/evals.json` convention (documented in `JSON Schemas.MD.md`), each new or substantially rewritten skill in `skills/` now has an `evals/evals.json` with 1-3 realistic test prompts and expected-output descriptions (no assertions yet, matching `skill-creator`'s own "prompts first" pattern) — 9 files total. The root-level `agents/*.md` persona files don't carry eval infrastructure, consistent with how existing files of that type (`email-agent.md`, `doc-coauthoring.MD.md`) are already handled in this repo.

`_INDEX.md` was updated with a new table so all of the above is actually discoverable from the repo's navigation hub, which previously linked to none of it.

## Left deliberately unchanged (already good, or out of scope)

- `skills/investigative-psychology` (content, not the key) — real depth, different intended purpose than the "Psychology" gap identified here.
- `skills/content-research-writer`, `doc-coauthoring.MD.md`, `email-agent.md` — genuinely strong existing writing skills.
- `skills/deep-brainstorm`, `skills/brainstorming-matrix` — well-developed, unrelated to these domains.
- All developer/security/testing skills (`test-driven-development`, `systematic-debugging`, `ffuf-security-fuzzer`, etc.) — out of scope for this pass and already solid.
- `Consolidated_Skills_Summary.md` — a historical record of a prior, unrelated batch of skill creation; left as-is rather than edited, since it documents what it documents.

## Not done, flagged for your decision

- The interview-family redundancy itself (six overlapping stub names before this pass) suggests these may have been scaffolded faster than they were thought through. They're now each functionally distinct and non-duplicative, but if on review you'd rather consolidate two or three of them into one, that's a naming/architecture call worth making deliberately rather than something this pass should decide unilaterally.
- Git history still contains the exposed Ghost API key (see security finding above) — rotating the live key and, if desired, scrubbing history is a decision and action for you, not something done as part of this pass.
