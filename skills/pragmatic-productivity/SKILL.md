---
name: "pragmatic-productivity"
description: "Practical, non-generic productivity workflows for real-world tasks: weekly review, inbox-zero triage, calendar defense, energy-based task routing, and project shutdown checklists. Activates for overwhelm, task backlog, time blocking, prioritization, procrastination, weekly planning, and 'too many things to do' requests. Produces concrete next actions, never motivational filler."
---

# Pragmatic Productivity

Turn vague overwhelm into a concrete, executable plan. Every output ends in a physical next action with a time and place — never advice like "stay focused" or "prioritize better."

## Natural Triggers
- "I'm overwhelmed / too much to do"
- "help me plan my week"
- "organize my task list"
- "I keep procrastinating on X"
- "time block my calendar"
- "triage my inbox"
- "what should I work on first"
- "set up a weekly review"
- "I can't finish anything"
- "build me a daily routine"

## Core Rule: No Generic Advice

Banned outputs: "break it into smaller steps" without doing the breaking, "use the Pomodoro technique" without scheduling the first pomodoro, "prioritize ruthlessly" without producing the ranked list. If the user gives you the inputs, you do the work in the response.

## Workflows

### 1. Capture-and-Triage (when: overwhelm, scattered tasks)
1. Dump everything — ask the user to list every open loop, or extract them from the message.
2. For each item, apply the 4D gate: **Do** (under 2 minutes → schedule it now), **Defer** (real task → next-action + date), **Delegate** (name the person + the handoff message), **Delete** (say why it's safe to drop).
3. Rewrite every deferred item as a physical next action: verb + object + context ("email Sarah the draft contract" not "contract stuff").
4. Output a table: item · decision · next action · when · 15-min-or-less first step.

*Basis: capture/clarify stages of Allen's Getting Things Done; two-minute rule.*

### 2. Weekly Review (when: planning a week, recurring resets)
1. **Look back:** wins, misses, and the one recurring blocker (name it explicitly).
2. **Sweep:** calendar next 2 weeks, task list, inbox count, waiting-on list.
3. **Pick 3 outcomes** for the week — outcomes ("draft sent to reviewer"), not activities ("work on draft").
4. **Pre-place** the hard task first: one 90-minute deep block per outcome on the calendar before anything else lands.
5. Output: 3 outcomes · their calendar blocks · the blocker and one countermeasure.

### 3. Calendar Defense (when: meetings eating the week)
- Compute the user's actual free deep-work hours from their described week.
- Batch shallow work (email, admin) into two fixed daily windows; name the times.
- Propose decline/shorten/async scripts for low-value meetings — write the actual message.
- Protect one no-meeting morning; state the recurring block to create.

*Basis: Newport's deep work scheduling; maker vs. manager schedule (Graham).*

### 4. Energy-Based Routing (when: "I can't focus," inconsistent output)
Match task type to state instead of forcing willpower:
| State | Route to |
|---|---|
| Sharp, fresh | The one hard/creative task — nothing else first |
| Foggy, tired | Mechanical batch work: filing, formatting, replies |
| Anxious, avoidant | 10-minute starter version of the avoided task, timer on |
| Post-lunch dip | Calls, walking meetings, errands |

Never schedule the week's hardest task after 3 p.m. or after a meeting block.

### 5. Procrastination Breaker (when: one task stuck > 3 days)
1. Diagnose which it is: unclear next step · too big · fear of judgment · genuinely low value.
2. Unclear → write the literal first sentence/command/click for them. Too big → produce the 15-minute starter version. Fear → draft the "rough version, feedback welcome" framing. Low value → recommend deletion and say so plainly.
3. Schedule the starter: exact day, time, duration.

### 6. Project Shutdown (when: finishing or abandoning a project)
Checklist: deliverables archived where? · loose promises to people (list them, draft the closing messages) · lessons worth one paragraph · recurring tasks/subscriptions to cancel · the "done" declaration message.

## Output Standards
- Every plan item has: action verb, owner, date/time, first 15-minute step.
- Maximum 3 priorities per day; surplus goes to a visible "not this week" list.
- If inputs are missing (calendar, task list), ask for exactly the missing piece — one question, then proceed with stated assumptions.

## References
- Allen, *Getting Things Done* — capture, clarify, next-action discipline
- Newport, *Deep Work* — block scheduling, shallow-work batching
- Graham, "Maker's Schedule, Manager's Schedule"
- Implementation intentions research (Gollwitzer) — the when/where/how effect on follow-through
