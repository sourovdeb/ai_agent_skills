# QC & Upgrade Report — 2026-07-06

Integration of five uploaded archives plus a repo-wide quality upgrade: every core skill now ships as a trio (SKILL.md + agent instructions + prompt JSON), and a shared long-task memory protocol prevents context loss on large jobs.

## 1. Where each archive landed

| Archive | Placed at | Notes |
|---|---|---|
| Creating_reusable_skill_instructions_and_prompts | `skills/psychology-agent/`, `skills/writer-agent/` (full trios); companion instructions+prompt pairs merged into `skills/deep-brainstorm/`, `skills/universal-upgrade/`, `skills/investigative-psychology/`, `skills/memory-elicitation-interview-skill/`; unmatched pairs to `prompts/` library (socratic-self-review, frontend-design, job-search-agent, legal-agent) | The trio format (SKILL.md + .instructions.md + .prompt.json) is adopted as the repo standard |
| Organizing_private_APIs | `skills/api-reference/SKILL.md` | Credentials file **excluded** — see §3 |
| Selfhosting Raspberry Pi + n8n | `skills/self-hosting-infra-advisor/` with feasibility breakdown as reference | |
| Sourov_DEB website redesign | `skills/system-design/` (skill); `projects/website-redesign/` (theme zip + preview HTML) | Theme is a site asset, not a skill — separated |
| project1files | **Not committed** — see §3 | Personal regulatory dossier |

## 2. Quality upgrades applied

- **Trio completion.** The six 2026-07-04 skills (pragmatic-productivity, legal-analysis-compliance, medical-information-advisor, empathic-listening-psychology, structured-interviewer, cambridge-writer) each received a terse `.instructions.md` and structured `.prompt.json` in the uploaded trio format, with numbered 8–11 step workflows.
- **Long_Task_Memory_Protocol.md** (new, root). Implements the many-small-steps requirement: decompose before executing, one STATE file per task, checkpoint after every step, resume from file not from memory, append-only decisions. Every prompt.json references it via `state_protocol`.
- **Anti-generic enforcement.** No skill was imported or written as a generic capability: each has a named niche, activation phrases, and a `related` cross-reference where siblings exist, so overlap is deliberate, not accidental.
- **Manifest.** `config/skills_manifest.json` now registers 18 skills with instructions/prompt paths, the `prompts/` library, the state protocol, and an `excluded_from_repo` section documenting what was held back and why.
- **.gitignore** hardened: `*LOCAL_ONLY*` and `*credentials*` patterns.

## 3. Excluded from the public repo (deliberate)

The repository is **public** (verified via GitHub API). Two uploads were held back:

1. **`api_credentials_LOCAL_ONLY.md`** — its own first line forbids committing ("DO NOT commit to GitHub"). It contains live API credentials. Keep it in a password manager. The companion `skills/api-reference/SKILL.md` was designed credential-free and is safely included.
2. **`project1files/` (regulatory dossier)** — real legal case files naming third parties: contracts, warning letters, WhatsApp exports, authority correspondence, GDPR emails. Publishing these in a public repository exposes personal data of identifiable people, is difficult to reverse (forks, caches), and could undermine the dossier itself. Recommendation: a separate **private** repository (e.g. `regulatory-dossier-private`). The generic, reusable parts (MASTER_REGULATORY_GUIDE, HANDOVER_INSTRUCTIONS_CLAUDE_AGENT) could be de-identified and imported later if wanted.

Related standing issue: `credentials/website-credentials.xml` is already committed and therefore already public. Rotate those credentials and purge history.

## 4. Overlap decisions (why both were kept)

| Pair | Division of labor |
|---|---|
| psychology-agent vs empathic-listening-psychology | Intervention end (WHO PM+ protocols, worksheets) vs receiving end (listening-first, no advice in first response) |
| writer-agent vs cambridge-writer | Plain-language explanation vs contested argument and high-stakes register |
| deep-brainstorm (repo) vs uploaded variant | Repo version kept canonical (multi-perspective, concreteness gate); uploaded diverge/converge variant preserved at `references/evidence-based-variant.md`; its methods-registry imported |
| legal-agent (prompts/) vs legal-analysis-compliance | Paralegal drafting counterpart vs analysis/compliance framework; cross-referenced |

## 5. Batch 3 (same day, second upload set)

**Placed:** `AI_Agent_Core_Instructions.md` (upload contained three drafts; the latest — with Output Scaling Class A/B — was kept, earlier two discarded as superseded); `skills/investigative-research/` (real SKILL.md + methodology.md reunited with their companion pair, moved from investigative-psychology); `skills/job-search-agent/` (SKILL.md reunited with its pair, `prompts/job-search-agent/` dissolved); `skills/self-debate/` and `skills/life-history-elicitation/` from the upgrade zip (the zip's four items were upgrade, debate, brainstorm, elicitation — the brainstorm and upgrade items differed from repo only in richer trigger descriptions, which were adopted while keeping the fuller repo bodies; `.skill` binaries skipped as duplicate archives). `memory-elicitation-interview-skill` marked **superseded** by life-history-elicitation.

**Authored:**
- `skills/objective-first/` (full trio) — the requested aim-and-objective gate: Objective Card (aim, beneficiary, verifiable success criteria, non-goals, kill condition, first step) required before any nontrivial work; execution checked against the card via the STATE file.
- `skills/data-analysis/` (full trio) — question-first analysis: severity-ranked data audit before any statistic, describe-before-infer, effect sizes over p-values, honest visualization, reproducible scripts, closing self-debate on the interpretation.
- `skills/self-debate/` companions (instructions + prompt.json) — wired as the standing post-job pass: every substantial job ends with "what was done well, what was weakest, what one change improves the next run," appended to OUTCOME-LOG.
- `skills/investigative-research/references/methodology-future.md` — the requested future methodology: provenance chains, AI-contamination screen (SYNTHETIC-RISK label), mandatory live-verification pass with archive links, four-grade uncertainty grammar, time-decay re-verification, counter-evidence quota, publication gate.

**Skill-chain now closed:** objective-first (aim) → deep-brainstorm (options) → self-debate (refinement) → execution skills → socratic-self-review / self-debate closing audit, all checkpointed through Long_Task_Memory_Protocol.md.

## 6. Open follow-ups

- Author trios for reference-style skills (api-reference, self-hosting-infra-advisor) if they get agent duty — currently lookup references, so instructions add little.
- Create SKILL.md bodies for the four `prompts/` entries when their skills are (re)built; job-search-agent should absorb the Job_Application_Career_Agent stub.
- Decide the private-repo question for project1files.
- evals.json coverage for the imported skills (psychology-agent, writer-agent, system-design).
