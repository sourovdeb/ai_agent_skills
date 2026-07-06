---
name: deep-brainstorm
description: Evidence-based ideation agent that finds easy and efficient methods and generates ranked options. Trigger whenever the user asks to brainstorm, generate ideas, list options or alternatives, find the easiest or most efficient method or approach, name something, unblock a stuck problem, or explore possibilities — even when the word brainstorm is absent. Runs divergence before convergence, grounded in documented findings on why naive group brainstorming underperforms (production blocking, Diehl and Stroebe 1987; Mullen et al. 1991) and which structured methods outperform it (nominal-group generation, brainwriting, SCAMPER transforms, morphological analysis). Ends with a criteria-based convergent screen and an effort-impact ranking so the easiest efficient option surfaces first. Includes an outcome-log improvement loop.
---

# Deep Brainstorm

Generate many options fast, then converge on the easiest efficient one. Method selection is itself evidence-based: the agent picks the lightest documented technique that fits the problem, not a ritual.

## Core rule: diverge, then converge — never both at once

Deferred judgment and quantity-first generation are the founding rules of the method (Osborn, 1953). Evaluating while generating suppresses output. Convergence happens only after the divergent burst is complete.

## Evidence base for method choice

- Interactive verbal groups produce roughly half the unique ideas of the same people generating alone; production blocking is the primary cause (Diehl and Stroebe, 1987, Journal of Personality and Social Psychology 53(3); Mullen, Johnson and Salas, 1991, meta-analysis). LIVE-VERIFIED this session.
- Structural fixes: nominal-group technique — independent generation before discussion (Delbecq et al.); brainwriting — parallel written generation (Rohrbach, 1968, 6-3-5 format; Paulus and Yang, 2000). LIVE-VERIFIED this session.
- Consequence for solo work with an AI: the agent plays the nominal-group role — it generates independent idea sets in parallel streams rather than one serial stream, and never critiques during generation.

## The pass

**0. Frame.** One block before generating: problem statement as a neutral question · constraints that must survive · quantity target (default 15–25 raw ideas) · effort budget (minutes the user will spend) · convergence criteria (3–5, measurable where possible). If the user has standing decision gates (for example a Net Decision Value framework), list them here; they govern Step 4.

**1. Method selection.** Choose the lightest documented method that fits, from `references/methods-registry.md`. Default ladder: free-list burst → SCAMPER transforms → morphological grid → constraint-based prompts. Escalate only when the previous rung stalls. State the chosen method and its source in one line.

**2. Divergent burst.** Quantity first, judgment deferred, wild welcomed, combination encouraged (Osborn's four rules, paraphrased). No evaluation, no ranking, no feasibility talk. Number every idea.

**3. Cross-pollination.** Run one transform pass on the raw list: SCAMPER verbs on the strongest fragments, forced pairings of distant items, or a morphological grid when the problem has separable dimensions. Add, never delete.

**4. Convergent screen.** Deduplicate and cluster. Score surviving candidates against the Step 0 criteria in a table. Apply the effort-impact screen: rank by (impact per criteria) against (effort to execute); the easiest efficient option leads the shortlist. Effort-impact scoring is practitioner-tier method (label TIER-4); the criteria matrix itself is the load-bearing instrument.

**5. Deliver.** Ranked shortlist (3–5) with one-line rationale each · full numbered raw list preserved as a parking lot · stated assumptions · next single action for the top option.

**6. Improvement loop.** Append one row to a persistent OUTCOME-LOG the user controls (repo, Drive, or Obsidian vault): date · problem · method used · ideas generated · option chosen · result when known. When the log shows a recurring failure pattern or ten sessions, revise this skill via skill-creator and record the change. Skill files are static; improvement occurs through this documented revision protocol, not through self-modification.

## Constraints

- Never critique during Steps 2–3.
- Never present a preference as a scored result; every ranking traces to the Step 0 criteria.
- One clarification round maximum; otherwise proceed on stated assumptions and mark them.

## Provenance

Diehl and Stroebe 1987, Mullen et al. 1991, nominal-group and brainwriting findings: LIVE-VERIFIED 2026-07-04. Osborn 1953, Rohrbach 1968, Eberle SCAMPER, Zwicky morphological analysis, Guilford divergent-convergent distinction: TRAINING-CITED, stable pre-cutoff references.

## Reference file

Read `references/methods-registry.md` before Step 1 when the problem is non-trivial.
