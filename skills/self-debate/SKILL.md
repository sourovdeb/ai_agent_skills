---
name: self-debate
description: Adversarial self-debate the agent runs on its own idea, plan, decision, draft, or outcome to refine it — the agent argues against itself in structured rounds and rewrites the outcome from what survives. Trigger on "debate this," "argue against yourself," "challenge this idea," "be judgmental about the outcome," "play devil's advocate," "stress-test this plan," "refine by debate," and proactively on the top ideas of a brainstorm or before committing to a contested decision. Distinct from socratic-self-review — that skill verifies factual deliverables against evidence pre-delivery; self-debate refines contested ideas and decisions where no single ground truth exists. Structure — steelman proponent and opponent built with Toulmin argument anatomy, fixed rebuttal and cross-examination rounds, a neutral judge pass scored only against declared criteria, then a synthesis with changelog.
---

# Self-Debate

Dialectic refinement. The agent builds the strongest case for and against its own outcome, lets them collide under fixed rules, and rewrites the outcome from what survives.

## Core rule: both sides get the strongest case

A strawmanned side voids the round. Each position is written as its best defender would write it, grounds labeled DOCUMENTED / RECOLLECTION-ONLY / INFERRED.

## Boundary — which skill

| Situation | Skill |
|---|---|
| Contested idea, plan, decision — no single ground truth | self-debate |
| Factual deliverable before delivery or publication | socratic-self-review |
| Nothing to refine yet | deep-brainstorm, then feed winners here |

## The pass

**0. Frame.** Outcome under debate · declared success criteria (from the user or the prior brainstorm Step 0) · stakes · round count (default 2, max 3).

**1. Position papers.** Proponent and Opponent each build a steelman with Toulmin anatomy — claim · grounds · warrant · backing · qualifier · rebuttal (Toulmin, 1958).

**2. Rebuttal round.** Each side attacks the other's weakest warrant, not its weakest phrasing.

**3. Cross-examination.** Each side poses the one question the other least wants answered. Answers go on record; evasion counts against the evading side.

**4. Judge pass.** Neutral scoring against Step-0 criteria only. Verdict per argument: survived · conceded · unresolved (needs the user or a live source). The judge may not import criteria mid-debate.

**5. Synthesis.** Rewrite the outcome keeping survived positions, integrating conceded objections as concrete changes. Changelog table: # · change · driving argument · label.

**6. Escalation.** A factual dispute exits the debate — route it to source verification or mark it unresolved. Deciding facts by rhetoric is prohibited.

## Stop criterion

Stop at the round limit, or earlier when a round produces no new surviving argument. List unresolved items for the user; never force a verdict.

## Anti-patterns

- Strawman opponent — token objections built to lose.
- Judge echoing the proponent — confirmation dressed as verdict.
- Manufactured balance — conceding nothing real while adding hollow caveats.
- Rounds past the limit — over-debating is its own failure mode.
- Settling factual questions inside the debate instead of by source.

## Method grounding

Dialectical inquiry and devil's advocacy outperform consensus approaches in strategic-decision research (Schweiger, Sandberg & Ragan, 1986). Structured multi-agent debate and iterative self-refinement improve model output quality (Du et al., 2023, multiagent debate; Madaan et al., 2023, Self-Refine). All RECOLLECTION-ONLY — verify before quoting in publications.
