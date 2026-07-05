---
name: biography-memoir-system
description: Orchestrate the full biography/memoir workflow — deciding which interview variant to run and how the interview material flows into a written memoir. Use this when a user wants to start a biography, memoir, or family-history project from scratch and isn't sure which specific tool they need, or when a project spans multiple stages (interviewing, then writing) and needs a coordinator rather than a single-purpose skill.
---

# Biography & Memoir System

This is the entry point for a family of skills that handle biography and memoir work end to end. If someone says "I want to interview my grandmother and turn it into a memoir," start here to route them to the right combination — don't try to do everything in one undifferentiated conversation.

## The family of skills, and when each applies

| Skill | Use when |
|---|---|
| `biography-interview-kit-private-master` | The subject wants a complete, unfiltered personal archive — everything, including material too sensitive or unresolved to ever publish. This is the default starting point for most projects, since you can always redact down from a complete record, but can't recover detail from a pre-filtered one. |
| `biography-interview-kit-public` | The output is meant to be shared or published from the start (a family history book, a tribute, a public memoir) and the subject wants interview questions and framing that already respect what will and won't be shared. |
| `dual-biography-interview-skill-v2` | The project needs both a complete private archive *and* a publishable version, produced from the same interview sessions rather than interviewing twice. |
| `memory-elicitation-interview-skill` | The goal is a single memory or a short set of memories (a specific event, a person, an era) rather than a full-life interview arc — e.g., capturing one grandparent's account of emigrating, not their whole biography. |
| `family-memory-deep-probe-reliability` | The narrator is elderly, has some memory impairment, or the family needs to reconcile conflicting accounts across multiple relatives — this variant adds reliability coding and dementia-aware adaptations on top of the base method. |

All five draw on the same underlying technique in `references/interview-methodology.md` — memory elicitation, reliability coding, and sensitive-material handling — so read that once regardless of which variant you end up running.

## Once interviews exist: writing the memoir

Turning interview transcripts into readable memoir prose is a distinct skill from conducting the interview — see the companion agent persona for the writing voice (`agents/Biography_Memoir_Writer_Agent.md`), and `skills/content-research-writer` if the project needs citation-grade sourcing (e.g., corroborating a family story against historical records). Don't collapse interviewing and writing into one pass — a good interview optimizes for eliciting real material in the moment; good memoir writing optimizes for what reads well afterward, and trying to do both simultaneously tends to produce an interview that's really a writing session in disguise, with the narrator performing for the page instead of just remembering.

## Deciding the shape of a new project

Ask, before picking a skill:
1. **Who is the subject, and are they the one being interviewed, or is someone interviewing on their behalf** (e.g., interviewing an aunt about a grandparent who has since died)? This changes what memory-reliability tagging applies.
2. **Is there any cognitive impairment or significant age-related fragility to plan around?** If yes, route to `family-memory-deep-probe-reliability` from the start rather than defaulting to the standard kit and adapting mid-project.
3. **Does anything ever get published or shared beyond the immediate family?** If genuinely unsure, default to the private-master kit — it's far easier to selectively publish from a complete private record later than to reconstruct detail that was never captured because the interview was filtered from the start.
4. **Is this a full-life project or a single memory/topic?** Don't run a multi-session full-biography kit when what's wanted is one grandparent's account of a single event — `memory-elicitation-interview-skill` is the leaner, right-sized tool for that.

## A note on scope

This system produces raw material and drafts for a family or individual's own use. It is not a substitute for a professional ghostwriter, oral historian, or archivist when the project is large-scale, commercial, or needs archival-grade preservation standards (e.g., a museum oral-history collection) — flag that distinction if a project's ambitions clearly exceed what a conversational interview process can responsibly deliver.
