# Domain Skills Audit — July 18, 2026

**Scope of this pass:** the same standing brief as the 2026-07-05 audit and 2026-07-06 QC report — productivity, legal, medical, psychology, interviewer, and writer domains, plus Alzheimer's/ADHD support — re-checked twelve days later against the current state of the repository. Per the standing rule ("do not change if it is good"), content was verified before anything was touched, and no skill body was rewritten in this pass.

## Headline

**The domain skills themselves are in good shape and were left unchanged.** All five requested domains (plus writer and Alzheimer's/ADHD) are covered by full, substantive skills built and QC'd in the July 4–6 passes; spot-checks this pass (e.g., `alzheimers-adhd-daily-support` — validation therapy, Barkley's externalization model, Wall of Awful/PINCH, clinician-routing gates all present and accurate) confirmed real depth, not scaffolding. What had drifted was the **infrastructure around them**: the JSON registry and the navigation index had not kept up with twelve days of additions, and one genuinely missing piece — an agent tying the cognitive-support skills together — was created.

## Changes made, with rationale

### 1. `config/skills_manifest.json` → v1.1 (the JSON-configuration update)

The manifest was last written 2026-07-06 and had gone stale in three verifiable ways:

- **27 skills existed on disk with no registry entry** — everything added after Jul 6 (`prompt-architect` Jul 8, `decision-battery-antifragile` Jul 14, `theme-factory` Jul 17) plus two batches that predated the manifest but were never registered: the 2026-07-01 developer/security/meta set (18 skills: superpowers, systematic-debugging, test-driven-development, ffuf-security-fuzzer, etc.) and the 2026-07-05 audit's own creations (`health-information-advisor`, `empathetic-listening`, `alzheimers-adhd-daily-support`, and the five-skill biography family). All are now registered with domain, path, evals/references where present, first-commit date (verified via git log), and safety gates where the skill has them.
- **Factually wrong agent statuses.** The manifest still listed `Daily_Living_Productivity_Agent`, `Legal_Regulatory_Dossier_Agent`, `Skilled_Biography_Interviewer_Agent`, and `Biography_Memoir_Writer_Agent` as `"stub"` — but all four were rebuilt with full content on 2026-07-05 (5.5–6.2 KB each, verified). Now `"active"` with rebuild notes. The six agents that genuinely are still one-line stubs are now honestly registered as such, each with a note pointing to the skill that covers its ground.
- **Missing domain.** Added `design` (theme-factory, web-asset-generator had no home in the taxonomy).

### 2. `agents/Cognitive_Support_Companion_Agent.md` (new — the requested agent)

The Alzheimer's/ADHD brief was covered at the *skill* level, but nothing tied those skills together at the *agent* level: a caregiver or ADHD adult arriving mid-crisis would need to know which of six skills to invoke. The new agent is deliberately a thin routing persona, not a seventh copy of the technique: listen first (`empathetic-listening`), silent red-flag screen (`health-information-advisor` triage), then route dementia-caregiver vs. ADHD executive-function vs. appointment-preparation vs. memory-preservation work to the existing skills. Non-negotiables: never diagnose, never advise on medication, treat the caregiver as a client too. This follows the same pattern as `Skilled_Biography_Interviewer_Agent` (persona + rules + routing table, no duplicated methodology).

### 3. `_INDEX.md`

Added the new agent to the domain-skills table and a new table registering the 18 developer/design/meta skills that the index (like the manifest) had never referenced. The index's own job — per the 2026-07-05 audit — is that nothing in `skills/` or `agents/` be orphaned from navigation; it had drifted back out of that state.

## Verified good and deliberately left unchanged

- **Productivity:** `pragmatic-productivity` (+ trio), `objective-first`, `system-design`, `Daily_Living_Productivity_Agent`, and the new-since-last-audit `decision-battery-antifragile` — the latter reviewed and left as committed; it's substantive (42 documented steps, own AGENT.md and README).
- **Legal:** `legal-analysis-compliance` (+ trio, UPL/citation/deadline gates), `Legal_Regulatory_Dossier_Agent`, `prompts/legal-agent`.
- **Medical:** `medical-information-advisor` (+ trio) and `health-information-advisor` (+ red-flag triage reference). The 07-06 overlap ruling (education/triage vs. advisor-workflow) still holds; both kept, now cross-referenced via `related` in the manifest.
- **Psychology:** `empathic-listening-psychology` (+ trio), `empathetic-listening`, `psychology-agent` (WHO PM+/mhGAP), `investigative-psychology`. The listening-first/no-advice-in-first-response and crisis-protocol gates are intact.
- **Interviewer:** `structured-interviewer` (+ trio), `life-history-elicitation`, the biography family. `memory-elicitation-interview-skill` remains correctly marked superseded.
- **Writer:** `cambridge-writer` (+ trio), `writer-agent`, `content-research-writer`, `Biography_Memoir_Writer_Agent`.
- **Alzheimer's/ADHD:** `alzheimers-adhd-daily-support` and `family-memory-deep-probe-reliability` — spot-checked line-by-line this pass; accurate, safety-gated, non-generic.

No content gaps warranting new *skills* were identified in the five domains this pass — the gap was registry/navigation drift plus the missing routing agent, both now closed.

## Standing items not resolved by this pass (owner decisions, unchanged from prior audits)

1. **Exposed credentials in git history** — the Ghost API key (redacted 07-05) and `credentials/website-credentials.xml` are still in history of a public repo; rotation + history scrub remain owner actions.
2. **`project1files/` private-repo decision** (07-06 report §3).
3. **Interview-family consolidation** — six functionally distinct variants; consolidation remains a deliberate architecture call, not something an automated pass should decide.
4. **Stub agents** — six remain stubs; each now has a manifest note naming the skill that covers it, so absorbing or deleting them is a quick decision when wanted.
