# Long Task Memory Protocol

Every skill's prompt.json references this file via `state_protocol`. Purpose: large tasks must survive context loss, session breaks, and agent handoffs. The mechanism is externalized state — the agent's memory lives in a file, not in the conversation.

## Rules

1. **Decompose before executing.** Any task expected to exceed ~10 actions is broken into numbered steps (as many as needed — 20, 40, 100) before step 1 runs. Each step is small enough to complete and verify in one pass.
2. **One STATE file per task.** Create `STATE_<task-slug>.md` at task start containing: goal (one sentence) · the numbered plan · current step · decisions made so far (one line each, with reason) · open questions · files touched.
3. **Checkpoint after every completed step.** Update the STATE file before starting the next step: mark the step done, record any decision or discovery in one line. Never batch checkpoints.
4. **Resume from file, not from memory.** On any new session, handoff, or doubt about earlier context: re-read the STATE file first and trust it over recollection. If the STATE file and recollection conflict, the file wins.
5. **Decisions are append-only.** Never rewrite a recorded decision; append a dated reversal line instead. The trail of changed minds is part of the memory.
6. **Deliverables named at step 0.** The STATE file lists the exact output artifacts expected, so a resumed session knows what "done" means without asking.
7. **Close-out.** On completion, the STATE file's final section records: what shipped, what was cut and why, and follow-ups. It is the handover document by construction.

## Failure this protocol prevents

Mid-task context loss silently drops constraints and repeats or contradicts earlier decisions. A five-second checkpoint after each step is cheaper than one re-derivation of lost intent.
