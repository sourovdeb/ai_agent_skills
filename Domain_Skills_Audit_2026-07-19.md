# Domain Skills Audit — July 19, 2026

**Scope of this pass:** productivity, legal, medical, psychology, interviewer, and writer domains, plus Alzheimer's/dementia and ADHD support. This is a follow-up to the 2026-07-04/05/06 passes (`Skills_Update_Summary_2026-07-04.md`, `Domain_Skills_Audit_2026-07-05.md`, `QC_Upgrade_Report_2026-07-06.md`). Every domain skill was re-checked against its actual file contents before deciding whether to touch it.

## Headline finding: the domains are covered, and covered well

All six requested domains now have substantive, safety-gated skills, most in the repo-standard trio format (SKILL.md + .instructions.md + .prompt.json):

| Domain | Coverage | Verdict |
|---|---|---|
| Productivity | `pragmatic-productivity` (trio + evals), `Daily_Living_Productivity_Agent`, `job-search-agent`, `system-design`, `objective-first` | Good — unchanged |
| Legal | `legal-analysis-compliance` (trio + evals, UPL boundary, no-invented-citations gate), `Legal_Regulatory_Dossier_Agent` (CREAC, Bluebook), `prompts/legal-agent` | Good — unchanged |
| Medical | `medical-information-advisor` (trio + evals, evidence grading) + `health-information-advisor` (red-flag-triage reference file) | Good — unchanged; pair documented (below) |
| Psychology | `empathic-listening-psychology` (trio + evals), `empathetic-listening`, `psychology-agent` (WHO PM+/mhGAP), `investigative-psychology` | Good — unchanged; pair documented (below) |
| Interviewer | `structured-interviewer` (trio + evals), `life-history-elicitation`, the 5-skill biography family + shared methodology reference | Good — unchanged |
| Writer | `cambridge-writer` (trio + evals) + `writer-agent` (plain-language counterpart), `content-research-writer`, `Biography_Memoir_Writer_Agent` | Good — unchanged |
| Alzheimer's / ADHD | `alzheimers-adhd-daily-support` (validation therapy, environment design, wandering safety, caregiver burnout; ADHD externalization, task initiation, body doubling) + dementia-aware interviewing in `family-memory-deep-probe-reliability` | Good — unchanged; now orchestrated (below) |

Per the standing instruction "do not change if it is good," **no existing skill body was rewritten in this pass.** The gaps found were in the connective tissue — registry, navigation, orchestration — not in the skills themselves.

## Gaps found and fixed in this pass

### 1. `config/skills_manifest.json` was two weeks stale (fixed — v1.0 → v1.1)

The manifest (last updated 2026-07-06) had drifted from the repository in three ways:

- **Ten skills existed on disk but were unregistered:** the entire 2026-07-05 audit batch (`health-information-advisor`, `empathetic-listening`, `alzheimers-adhd-daily-support`, `biography-memoir-system`, `biography-interview-kit-private-master`, `biography-interview-kit-public`, `dual-biography-interview-skill-v2`, `family-memory-deep-probe-reliability`) — the July 5 and July 6 passes ran in parallel and never reconciled — plus the later additions `decision-battery-antifragile` (Jul 14) and `theme-factory` (Jul 17). All ten are now registered with domains, eval paths, safety gates, and cross-references. Skill count: 24 → 34.
- **Four agent statuses were wrong:** `Daily_Living_Productivity_Agent`, `Legal_Regulatory_Dossier_Agent`, `Skilled_Biography_Interviewer_Agent`, and `Biography_Memoir_Writer_Agent` were still marked `"stub"` although the July 5 pass fully rewrote them (they are 3.7–6.2 KB working files). Corrected to `"active"` with dated notes.
- **Five genuine stubs were invisible:** the remaining one-line agent files are now registered as `"stub"` with notes on where their function actually lives, so the next pass doesn't have to rediscover them. `Wiki_Knowledge_Management_Agent` is explicitly flagged as the one stub with no covering skill — a candidate for a future pass, not silently orphaned.

**Rationale:** a machine-readable registry that misses a third of the skills defeats its purpose; this was the highest-value fix available without touching any content that was already good.

### 2. Parallel-run near-duplicates needed a documented division of labor (documented, not deleted)

Two pairs were created by parallel July runs and genuinely overlap:

- **`empathetic-listening` vs `empathic-listening-psychology`** — kept both: the former is the fuller technique essay (why the method works, failure modes, "signs you're doing it right"); the latter is the enforced protocol (banned first-response advice, trio format for agent duty). 
- **`health-information-advisor` vs `medical-information-advisor`** — kept both: the former carries the detailed `red-flag-triage.md` reference (BE-FAST, sepsis, anaphylaxis, pediatric/obstetric thresholds); the latter is the trio-format protocol with the evidence-grading scheme (`GUIDELINE`/`SYSTEMATIC-REVIEW`/`SINGLE-STUDY`).

Both divisions are now recorded in the manifest (`related` + `note` fields), extending the overlap-decision table begun in the 2026-07-06 QC report §4. **Deleting or merging either pair would lose real content and is deliberately left as an owner decision**, consistent with how the earlier passes handled overlap.

### 3. New agent: `agents/Care_Support_Companion_Agent.md` (created)

The task asked for an agent, and this was the one genuinely missing orchestration layer: the medical, psychology, and Alzheimer's/ADHD skills existed as strong individual pieces with cross-references but nothing routing between them. Real conversations in this space are mixed — a caregiver's message typically contains a possible medical red flag, emotional exhaustion, and a daily-living design problem at once, and answering in the wrong order is the classic failure (comforting the feeling while missing the red flag, or answering the fact while ignoring the burnout).

The new agent is a persona/router card in the established house style (mirrors `Skilled_Biography_Interviewer_Agent`): full skill references, a **fixed safety-first routing order** (red-flag/crisis screen → listening → information → daily-living design → caregiver check), and six non-compromisable rules (never diagnose/dose, never argue against care-seeking, validation over correction for dementia, ADHD ≠ motivation problem, no crisis close without a concrete next step, never a clinician substitute). This directly serves the Alzheimer's/ADHD directive: those skills are now reachable from a top-level agent instead of only by name.

### 4. `agents/Job_Application_Career_Agent.md` stub completed (71 bytes → router card)

The 2026-07-06 QC report explicitly left this as an open follow-up ("job-search-agent should absorb the Job_Application_Career_Agent stub"). Completed as a short router card pointing to `skills/job-search-agent` plus the natural chain (`structured-interviewer` for interview prep, `cambridge-writer` for high-stakes letters, `pragmatic-productivity` for campaign cadence), with anti-fabrication and review-before-send non-negotiables. Kept deliberately thin — the methodology lives in the skill, per the repo's router-card pattern.

### 5. `_INDEX.md` navigation extended

The index's domain-skills table predated the July 4/6 trio skills and the July 14/17 additions. Added rows for the six trio skills, the two new/completed agents, `decision-battery-antifragile`, `theme-factory`, and the manifest itself. No existing rows changed.

## Left deliberately unchanged (checked and found good)

- All six domain trio skills and their evals — re-read this pass; substantive, safety-gated, non-generic.
- `alzheimers-adhd-daily-support` — strong, evidence-grounded (validation therapy per Feil, ADHD externalization technique); needed orchestration, not editing.
- The biography/interview family and its shared methodology reference.
- `psychology-agent`, `writer-agent`, `investigative-*`, `deep-brainstorm`, `self-debate`, `objective-first`, `data-analysis`, and all developer/security skills — out of scope or already solid.
- The prior audit/QC reports — historical records, untouched.
- The four rewritten agents from July 5 — good as they stand; only their manifest status was corrected.

## Standing items still open for the owner (unchanged from prior reports, not re-actioned here)

1. **Rotate the exposed Ghost API key** (found and redacted 2026-07-05; git history still contains it) and the already-public `credentials/website-credentials.xml`.
2. **Private-repo decision** for the withheld `project1files/` regulatory dossier.
3. Optional: consolidate the interview-family naming, and decide whether `Wiki_Knowledge_Management_Agent` deserves a real skill.

## Files changed in this pass

| File | Change |
|---|---|
| `agents/Care_Support_Companion_Agent.md` | **New** — care-support orchestrator agent |
| `agents/Job_Application_Career_Agent.md` | Stub → router card (closes QC 2026-07-06 follow-up) |
| `config/skills_manifest.json` | v1.1 — +10 skill registrations, +7 agent entries, pair division-of-labor notes, status corrections |
| `_INDEX.md` | +13 navigation rows for previously unindexed skills/agents |
| `Domain_Skills_Audit_2026-07-19.md` | **New** — this report |
