# Skills Audit — July 18, 2026

**Scope:** productivity, legal, medical, psychology, interviewer, and writer (Cambridge-level) domains, plus Alzheimer's/dementia and ADHD support. Every finding below was checked against actual file contents before deciding whether to change anything. The governing rule of this pass was **"do not change if it is good"** — and most of the library is good, so most of it was left alone.

---

## Headline finding: the domains are covered; the defects were coordination, not content

Three prior passes (2026-07-04, 2026-07-05, 2026-07-06) already built strong, source-grounded skills in every requested domain:

| Domain | Coverage (verified by reading, not filenames) | Verdict |
|---|---|---|
| Productivity | `pragmatic-productivity` (trio), `agents/Daily_Living_Productivity_Agent` (state-based routing), `system-design`, `objective-first`, `decision-battery-antifragile` | Good — unchanged |
| Legal | `legal-analysis-compliance` (trio, UPL boundary, no-invented-citations gate), `agents/Legal_Regulatory_Dossier_Agent` (CREAC, jurisdiction matrices, Bluebook), `prompts/legal-agent` | Good — unchanged |
| Medical | `medical-information-advisor` (trio, triage tiers, evidence grading) **and** `health-information-advisor` (red-flag reference file) | Good content, **duplicate scope** — see below |
| Psychology | `empathic-listening-psychology` (trio: Rogers, OARS, Linehan) **and** `empathetic-listening`, plus `psychology-agent` (WHO PM+ protocols) and `investigative-psychology` (research auditing) | Good content, **duplicate scope** in the listening pair — see below |
| Interviewer | `structured-interviewer` (trio), `life-history-elicitation`, the six-skill biography/memoir family | Good — unchanged |
| Writer (Cambridge) | `cambridge-writer` (trio), `writer-agent`, `agents/Biography_Memoir_Writer_Agent` | Good — unchanged |
| Alzheimer's / ADHD | `alzheimers-adhd-daily-support` (validation therapy per Feil, environment/routine design, wandering safety, caregiver burnout; ADHD externalization, task initiation, body doubling) + `family-memory-deep-probe-reliability` for memory-impaired narrators | Good — unchanged |

No new domain skills were needed, and none were written. What this pass found instead were three coordination defects left behind by the earlier passes running in parallel.

## Defect 1 — duplicate skills from parallel audit runs (fixed by cross-reference, not deletion)

The 2026-07-05 audit stated "no medical coverage existed at all" and "zero listening/empathy coverage" — but `medical-information-advisor` and `empathic-listening-psychology` had been created on 2026-07-04. The 07-05 run evidently executed on a branch that could not see the 07-04 work, and both branches merged. Result: two pairs of high-quality skills with near-identical activation triggers, each unaware of the other — a real routing defect, since an agent choosing skills sees two competitors for the same job and no guidance.

**Fix applied (minimal, non-destructive):** each of the four files gained a short "Related skill (overlap notice)" section stating the sibling's existence, the division of labor (structured-workflow trio vs. conversational register + red-flag reference file), and that consolidation is **an owner decision, deliberately not made unilaterally by this pass**. Nothing was deleted or rewritten.

- `skills/medical-information-advisor/SKILL.md` ↔ `skills/health-information-advisor/SKILL.md`
- `skills/empathic-listening-psychology/SKILL.md` ↔ `skills/empathetic-listening/SKILL.md`

**Recommendation for the owner:** keep one canonical skill per pair (the trio-complete 07-04 versions are the natural canon; the 07-05 versions' distinct assets — the `red-flag-triage.md` reference and the "signs you're doing it right" cues — are worth folding in before retiring them).

## Defect 2 — `config/skills_manifest.json` was stale and self-contradictory (fixed)

The manifest (last updated 2026-07-06) had two factual problems:

1. **Missing skills.** None of the 2026-07-05 audit's output was registered (health-information-advisor, empathetic-listening, alzheimers-adhd-daily-support, the five biography-family skills), nor the two skills added 2026-07-17 (decision-battery-antifragile, theme-factory). Ten entries added, with evals/references paths verified on disk, safety-gate lists, and explicit `overlap_note` fields on the two duplicate pairs.
2. **Wrong agent statuses.** All four `agents/*.md` files were still marked `"status": "stub"` — but they were fully rewritten on 2026-07-05 (5–6 KB each). Statuses corrected to `active` with accurate notes.

Also: manifest version bumped to 1.1, `updated` set to 2026-07-18, and two domains added to the taxonomy (`care-support`, `design`) so the new entries aren't misfiled. JSON validated with `python3 -m json.tool`.

## Defect 3 — no agent tied the care domains together (fixed by the one new artifact of this pass)

The requested "also create an agent" was pointed at the one genuine structural gap: strong specialist skills for dementia caregiving, ADHD, health triage, listening, legal paperwork, and depleted-state productivity existed with **no front door** — a caregiver would need to know this repo's internal map to reach the right one.

**Created: `agents/Cognitive_Support_Companion_Agent.md`** — an orchestrator, deliberately not a duplicate of any skill's content:

- **Listen-first sequence** (empathic-listening behavior runs before any triage or advice — the caregiver-shame example is spelled out).
- **Explicit routing map** to `alzheimers-adhd-daily-support` (core payload), `medical-information-advisor` + the red-flag thresholds file, `family-memory-deep-probe-reliability` (preserving a memory-impaired relative's story), `legal-analysis-compliance` (POA/benefits/accommodations paperwork, UPL boundary intact), and `Daily_Living_Productivity_Agent`'s depleted-state mode.
- **Inherited safety gates restated as non-overridable:** no diagnosis, no medication decisions, direct crisis inquiry with resources (988 / Adult Protective Services), never argue against care-seeking.
- **Continuity requirement:** STATE file per `Long_Task_Memory_Protocol.md`, because forcing an exhausted caregiver to re-explain their situation each session is the domain's cruelest failure mode.

Registered in the manifest and `_INDEX.md`.

## Left deliberately unchanged (verified good)

- `alzheimers-adhd-daily-support` — read in full; evidence-grounded (Feil validation therapy, externalization technique), correctly routes medication to clinicians. No changes needed.
- All six 2026-07-04 trio skills, the biography family, `psychology-agent`, `investigative-psychology`/`investigative-research`, `life-history-elicitation`, the four rewritten agents, `decision-battery-antifragile`, `theme-factory`, and all developer/security/teaching skills.
- Prior audit documents — historical records, not edited.

## Standing items re-flagged (decisions for the owner, not this pass)

1. **Consolidation of the two duplicate pairs** (above).
2. **Exposed credentials in git history** — the Ghost API key (flagged 2026-07-05) and `credentials/website-credentials.xml` (flagged 2026-07-06) remain in history; rotation + history scrub still pending.
3. Remaining one-line agent stubs outside this audit's domains (`ELT_Teaching_Master_Agent`, `Wiki_Knowledge_Management_Agent`, `Critical_Analysis_PostHoc_Agent` — the latter's content exists at root as `Post-hoc Analyzer Agent.md`; `Job_Application_Career_Agent` should be absorbed by `job-search-agent` per the 07-06 report).

## Files changed in this pass

| File | Change |
|---|---|
| `skills/medical-information-advisor/SKILL.md` | + overlap notice (append only) |
| `skills/health-information-advisor/SKILL.md` | + overlap notice (append only) |
| `skills/empathic-listening-psychology/SKILL.md` | + overlap notice (append only) |
| `skills/empathetic-listening/SKILL.md` | + overlap notice (append only) |
| `config/skills_manifest.json` | +10 skill entries, agent statuses corrected, +1 agent, 2 domains, overlap notes, v1.1 |
| `agents/Cognitive_Support_Companion_Agent.md` | **new** — care-domain orchestrator agent |
| `_INDEX.md` | + new agent row, + audit-trail line |
| `Skills_Audit_2026-07-18.md` | **new** — this document |
