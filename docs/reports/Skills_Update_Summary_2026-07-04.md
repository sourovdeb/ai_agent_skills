# Skills Update Summary — 2026-07-04

Gap analysis and update across five requested domains (productivity, legal, medical, psychology, interviewer) plus writer. Six new skills, seven JSON configurations, and this rationale document.

---

## 1. Gap Analysis

| Domain | What existed | Gap found |
|---|---|---|
| Productivity | `Daily_Living_Productivity_Agent.md` (86-byte one-line stub); `invoice-file-organizer` (narrow) | No actual workflow instructions anywhere. The agent file is a description with no body. |
| Legal | `Legal_Regulatory_Dossier_Agent.md` (72-byte stub) | No legal skill at all in `skills/`. No rigor standards, no citation discipline, no UPL boundary defined anywhere. |
| Medical | **Nothing** | The single largest gap: zero medical content in the repo despite it being a listed target domain. |
| Psychology | `investigative-psychology` (research/audit methodology) | Existing skill is adversarial research — no skill for the empathy/listening use case the domain brief specifies. These are different jobs; per the repo's own single-responsibility rule they need separate skills. |
| Interviewer | Three biography-interview kits + agent stub | All interviewing content is biography/memoir-specific. No general structured interviewing (hiring, mock interviews, user research, expert elicitation). |
| Writer | `content-research-writer` (citations/formatting); memoir agent stub | Existing writer skill handles mechanics (citations, formatting), not prose craft or argument quality. No skill sets a high-standard writing bar. |
| JSON configs | `JSON Schemas.MD.md` documents an `evals.json` schema — but **zero `.json` files exist in the repo** | The documented convention was never instantiated. No machine-readable registry of skills exists. |

## 2. New Skills (with rationale)

### `skills/pragmatic-productivity/` — Productivity
Practical, non-generic workflows as the brief demands: capture-and-triage (4D gate), weekly review, calendar defense, energy-based routing, procrastination breaker, project shutdown. Its core rule **bans generic advice** — if the user supplies inputs, the skill does the breakdown/scheduling in the response rather than telling the user to do it. Grounded in GTD (Allen), Deep Work (Newport), maker/manager schedules (Graham), and implementation-intentions research (Gollwitzer).
*Rationale: the productivity agent was an empty stub, and "productivity advice" is the domain most prone to generic filler — so the skill's central mechanism is a filler ban plus mandatory concrete next actions (verb + time + 15-minute first step).*

### `skills/legal-analysis-compliance/` — Legal
Attorney-level rigor operationalized: jurisdiction-first rule, **deadlines flagged before analysis** (a blown limitation period invalidates any analysis), IRAC-plus with mandatory counter-analysis, three-tier citation labeling (DOCUMENTED / RECOLLECTION-ONLY / INFERRED) with an explicit ban on invented citations, contract RED/AMBER/GREEN protocol, compliance obligation mapping, and an escalation matrix. UPL boundary per ABA Model Rule 5.5: information and analysis, never representation or strategy selection in high-stakes matters.
*Rationale: rigor in legal work is mostly discipline about jurisdiction, time bars, and source verification — the three failure modes that most embarrass AI legal output — so each is a non-negotiable rule rather than a suggestion.*

### `skills/medical-information-advisor/` — Medical
Advisor-level, exactly as briefed: **flag issues, then escalate through proper channels**. Red-flag triage runs before any other content (emergency / same-day / GP-within-days / self-care-with-safety-net, modeled on NHS-style triage tiers). Evidence grading (GUIDELINE / SYSTEMATIC-REVIEW / SINGLE-STUDY / RECOLLECTION-ONLY). Workflows for symptom discussion, test-result literacy, appointment preparation (the highest-leverage advisor function), medication literacy (routing interaction questions to pharmacists — the correct underused channel), chronic-condition support, and a formal escalation ladder (clinician → practice manager → second opinion → ombudsman) with drafted first messages. Hard bans: no diagnosis, no dosing, never argue against care-seeking.
*Rationale: filled the repo's only completely empty target domain. The advisor framing — prepare the user to get more from real clinicians rather than substitute for them — is both the safe and the genuinely useful position.*

### `skills/empathic-listening-psychology/` — Psychology
Listening and empathy prioritized structurally, not rhetorically: the **first response may contain no advice** — only reflection, feeling-naming, and invitation. Techniques: Rogers' reflective listening, Linehan's validation levels (validate emotion, stay honest about facts), Miller & Rollnick's OARS, a six-stage conversation arc where help is offered only if invited, and a "working assumptions about human nature" section (anger as bodyguard for hurt; "am I overreacting" as a legitimacy question; patterns as protection; the paradox of change). Crisis protocol asks directly about safety (evidence-backed: Dazzi et al. 2014 — asking does not increase risk), provides resources, and stays present rather than disclaimer-and-exit.
*Rationale: the existing psychology skill audits research; nothing served the person who needs to be heard. Advice-before-empathy is the classic failure mode, so the skill makes it impossible by rule rather than by exhortation.*

### `skills/structured-interviewer/` — Interviewer
General interviewing built on the strongest evidence in the field: structured interviews roughly double predictive validity (Schmidt & Hunter). Five workflows: interview design (role-derived competencies, behavioral questions, BARS scorecards written before interviewing), conducting/probing (STAR extraction, verification probes that expose fabrication), bias-controlled evaluation (independent scoring before discussion), candidate mock-interview coaching (story banks), and research/expert elicitation (Mom Test discipline: past behavior, never hypothetical intent).
*Rationale: existing interview assets were all biography-specific. This covers the general seat — interviewer, candidate, or researcher — and encodes the bias controls that ad-hoc interviewing always skips.*

### `skills/cambridge-writer/` — Writer
Cambridge-supervision standard operationalized: a thesis "precise enough to be wrong," skeleton-argument check before prose, mandatory steel-manned counter-argument, evidence discipline (no unattributed "studies show"), and a mandatory three-pass edit (argument → sentence → ear) with a minus-10–15% length target. Register control (audience/distance/temperature dials) and genre notes for essays, personal statements, op-eds, and speeches. Grounded in Williams (*Style*), Zinsser, Orwell, Graff & Birkenstein.
*Rationale: `content-research-writer` handles citation mechanics; nothing set a quality bar for the prose and the argument itself. "Cambridge level" is defined here as contestable-thesis + fair counter-argument + plain exact language — checkable standards, not vibes.*

## 3. JSON Configurations Created

The repo documented an `evals.json` schema (`JSON Schemas.MD.md`) but contained **no JSON file anywhere**. Fixed:

- **Six `skills/<name>/evals/evals.json` files** — 3 evals each (18 total), following the documented schema exactly (`skill_name`, `evals[].id/prompt/expected_output/expectations`). Evals deliberately test the safety gates: the medical eval includes a chest-pain prompt that must produce emergency routing as the first line; the legal eval includes a criminal-matter prompt that must refuse strategy and route to counsel; the psychology eval includes a passive-ideation prompt that must trigger direct safety inquiry.
- **`config/skills_manifest.json`** (new) — machine-readable registry: every new skill with domain, path, eval path, and explicit `safety_gates`; key existing skills for context; and the four agent stub files flagged `status: "stub"` so the gap is tracked in data, not just prose.

## 4. Flagged for Future Work (not done in this pass)

- **Agent stubs:** all 10 files in `agents/` are one-line descriptions (0 newlines, 58–89 bytes). The four relevant to these domains are flagged in the manifest; the new skills carry the substance in the meantime. Recommend either expanding stubs into full agent prompts that *reference* these skills, or removing the directory.
- **`skills_export_2026-06-18.zip`** is 97 bytes — almost certainly a broken/placeholder archive.
- **`credentials/website-credentials.xml`** — credentials committed to a repo; recommend moving to a secret manager and purging history.

## 5. Conventions Followed

All new skills match the repo's established standards (per `Consolidated_Skills_Summary.md` and skill-creator): YAML frontmatter with name + sub-500-character description, 10 natural triggers, single responsibility, concrete examples/protocols, reference links, under 120 lines each.
