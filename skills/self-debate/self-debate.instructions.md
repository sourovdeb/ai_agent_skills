# Agent Instruction: self-debate

Source: skills/self-debate/SKILL.md (validated 2026-07-06).

## Role
Adversarial self-refinement: after any substantial job, and on any contested idea, plan, or decision, the agent argues against its own outcome in structured rounds and rewrites from what survives. This is the standing "how good was this job and what would make it better" pass.

## Core rules
- Both sides get the strongest case; a strawmanned side voids the round. Grounds labeled DOCUMENTED, RECOLLECTION-ONLY, or INFERRED.
- Judge scores only against declared success criteria, never against which side sounds better.
- Distinct from socratic-self-review: that verifies factual deliverables against evidence; self-debate refines where no single ground truth exists.
- Runs proactively on brainstorm winners and before committing contested decisions; runs as a closing pass on completed work.

## Workflow
1. Frame: outcome under debate, declared success criteria (pull from the Objective Card when one exists), stakes, round count (default 2, max 3).
2. Proponent position paper: steelman with Toulmin anatomy — claim, grounds, warrant, backing, qualifier, rebuttal.
3. Opponent position paper: same anatomy, best case against.
4. Rebuttal round: each side attacks the other's weakest warrant, not its phrasing.
5. Cross-examination: each side asks the one question the other least wants answered; evasion counts against the evader.
6. Judge pass: score both cases against the declared criteria only; name what survived from each side.
7. Synthesis: rewrite the outcome from surviving material, with a changelog naming what changed and which argument forced it.
8. Closing self-audit (every substantial job): what was done well, what was weakest, what one change would most improve the next run — appended to OUTCOME-LOG.
9. Multi-round or recurring debates: record positions and verdicts in the STATE file per Long_Task_Memory_Protocol.md so later rounds do not relitigate settled points.

## Constraints
- Maximum 3 rounds; past that, the disagreement is a missing fact, not a debate — name the fact.
- The synthesis must differ from the original where the opponent scored; a debate that changes nothing is flagged as ritual.

## Activation
debate this, argue against yourself, challenge this idea, devil's advocate, stress-test this plan, refine by debate, how good was this, what could be better, post-task review.

## Output discipline
Output discipline: terse by default; expand only where the task requires. No contractions. No inline bold or italic. Formatting reserved for headings and structured data. No emojis. Improvement loop: append each session to OUTCOME-LOG; revise via skill-creator at ten sessions or a recurring failure pattern.
