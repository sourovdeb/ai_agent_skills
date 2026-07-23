# Domain Skills Audit — July 23, 2026

**Scope of this pass:** productivity, legal, medical, psychology, interviewer, and writer domains, plus Alzheimer's/dementia and ADHD support. Follow-up to the 2026-07-04/05/06 passes (in-repo reports) and the 2026-07-18/19 passes (reports currently only in Box and in unmerged draft PRs — see the headline finding below).

## Headline finding 1: the domains remain covered, and covered well — nothing rewritten

Every domain skill body was spot-checked against its actual file contents this pass. All are substantive (40–90 line SKILL.md bodies, most with instructions + prompt.json trios and evals), safety-gated, and source-grounded. All JSON in `skills/**` and `config/` parses cleanly. Per the standing rule "do not change if it is good," **no existing skill body, agent body, manifest, or index file was modified in this pass.**

| Domain | Verified good, untouched |
|---|---|
| Productivity | `pragmatic-productivity` (trio + evals), `Daily_Living_Productivity_Agent`, `objective-first`, `system-design` |
| Legal | `legal-analysis-compliance` (trio + evals), `Legal_Regulatory_Dossier_Agent`, `prompts/legal-agent` |
| Medical | `medical-information-advisor` (trio + evals) + `health-information-advisor` (red-flag triage reference) |
| Psychology | `empathic-listening-psychology` (trio + evals), `empathetic-listening`, `psychology-agent` (WHO PM+/mhGAP) |
| Interviewer | `structured-interviewer` (trio + evals), `life-history-elicitation`, the biography family + shared methodology |
| Writer | `cambridge-writer` (trio + evals), `writer-agent`, `content-research-writer`, `Biography_Memoir_Writer_Agent` |
| Alzheimer's / ADHD | `alzheimers-adhd-daily-support` + dementia-aware interviewing in `family-memory-deep-probe-reliability` |

## Headline finding 2: three duplicate draft PRs are stacking up — owner decision needed

The July 18 and July 19 runs of this same scheduled task each independently found the same connective-tissue gaps (stale manifest, missing care-support orchestrator agent, index drift) and each opened a draft PR that was never merged:

- **PR #7** (branch `sourov/loving-dijkstra-jhtyo1`, 2026-07-18) — manifest v1.1, `Cognitive_Support_Companion_Agent`, index update
- **PR #8** (branch `sourov/loving-dijkstra-fx2s0x`, 2026-07-18) — manifest v1.1, `Cognitive_Support_Companion_Agent`, overlap notices in four SKILL.md files, index update
- **PR #10** (branch `sourov/loving-dijkstra-84dopf`, 2026-07-19) — manifest v1.1, `Care_Support_Companion_Agent`, `Job_Application_Career_Agent` completion, index update

All three rewrite `config/skills_manifest.json` and `_INDEX.md`, so they conflict with each other and at most one can merge cleanly. **Recommendation: merge #10** (the most complete — it also closes the Job_Application_Career_Agent follow-up from `QC_Upgrade_Report_2026-07-06.md` §6), **then close #7 and #8 as superseded.** If the overlap-notice sections from #8 are wanted, they can be cherry-picked afterward. Until one of these merges, each new scheduled run re-discovers the same "gaps" — this pass deliberately broke that cycle by touching neither the manifest nor the index.

## What this pass did (only work no pending PR contains)

### 1. Eval configurations for three skills that had none (JSON configuration work)

`QC_Upgrade_Report_2026-07-06.md` §6 explicitly left "evals.json coverage for the imported skills (psychology-agent, writer-agent, system-design)" as an open follow-up. No pending PR addresses it. Added, in the house `evals/evals.json` schema (id / prompt / expected_output / expectations):

- **`skills/psychology-agent/evals/evals.json`** — 3 evals: behavioural-activation flow with boundary and no-diagnosis checks; crisis-protocol override (the single most safety-critical behavior in the repo — protocol work must stop, concrete crisis lines must appear, no method discussion); Professional Verification Register output.
- **`skills/writer-agent/evals/evals.json`** — 3 evals: anecdotal-lede narrative piece with readability measurement; economy-edit rewrite of bureaucratic prose; publication-bound piece exercising the fact gate and socratic-self-review chain.
- **`skills/system-design/evals/evals.json`** — 3 evals: full System Design Dossier (owner + trigger per stage, documentary precision, human approval gates); 5×5 risk register for a community streaming pilot; automation spec with credential-store, failure-path, dry-run, and human-send-gate checks.

**Rationale:** these three skills are used as agent-duty workhorses but were the only trio-format skills with no test surface at all; evals are what makes "verified good" checkable rather than asserted.

### 2. New agent: `agents/Wiki_Knowledge_Management_Agent.md` (58-byte stub → full router card)

Every prior audit flagged this as "the one stub with no covering skill... a candidate for a future pass" — and no pending PR fills it. That assessment was slightly stale: `skills/tapestry-knowledge-graphs` (added mid-July) now covers the ingestion/structuring methodology, so the stub could be completed honestly as a router card in the established house style (persona + full_skill_references + non_compromisable_rules, mirroring `Skilled_Biography_Interviewer_Agent`). It routes to tapestry-knowledge-graphs, doc-coauthoring, content-research-writer, investigative-research, and the Long_Task_Memory_Protocol, with six rules centered on traceability (no page without named sources, no orphan pages, no silent overwrites, quote/paraphrase honesty, state-protocol discipline for large ingestions, answer-from-the-wiki-or-say-so).

**Rationale:** this satisfies the task's "create an agent" directive with the one agent genuinely missing, instead of duplicating the care-support agent already sitting in three pending PRs.

### 3. Deliberately NOT done, and why

- **No manifest or `_INDEX.md` changes** — both files are rewritten by all three pending PRs; touching them here would guarantee a fourth conflicting version. The new files in this pass should be registered in the manifest in the first pass after the PR train is resolved.
- **No new medical/psychology/care agent** — already exists in pending PR #10; duplicating it would worsen the exact problem this report flags.
- **No skill-body edits anywhere** — everything checked was good.

## Standing items still open for the owner (unchanged from prior reports)

1. **Resolve the PR train:** merge #10, close #7/#8 (see above). Also note PR #9 (repository documentation restructure) is open and touches overlapping navigation concerns.
2. **Rotate the exposed credentials** flagged since 2026-07-05: the Ghost API key (redacted from the working tree, still in git history) and `credentials/website-credentials.xml` (still committed and public).
3. **Private-repo decision** for the withheld `project1files/` regulatory dossier.
4. Optional: consolidate the interview-family naming.

## Files changed in this pass

| File | Change |
|---|---|
| `skills/psychology-agent/evals/evals.json` | **New** — 3 evals incl. crisis-protocol override test |
| `skills/writer-agent/evals/evals.json` | **New** — 3 evals incl. publication fact-gate test |
| `skills/system-design/evals/evals.json` | **New** — 3 evals incl. approval-gate and risk-register tests |
| `agents/Wiki_Knowledge_Management_Agent.md` | Stub → full router card (closes the last flagged agent gap) |
| `Domain_Skills_Audit_2026-07-23.md` | **New** — this report |
