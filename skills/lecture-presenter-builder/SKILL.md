---
name: lecture-presenter-builder
description: Build presenter-ready lectures for adult beginners. Produces a spoken script for the instructor plus a separate sequence of visuals and on-screen material for learners. Use for lectures, live teaching, narrated videos, presentations, and screen/board explanations. Do not use to create student handouts unless explicitly requested.
---

# Lecture Presenter Builder

Create a lecture the presenter can read aloud while showing the audience what matters. Assume learners are adults with no prior subject knowledge. Keep the explanation human, exact, and useful.

## Workflow

1. Identify the topic and the change the audience should leave with: explain, distinguish, decide, or do.
2. Check for available material. Read attached files and user-provided links when accessible. If a named chapter, course, book, or document is essential but missing, ask for it rather than inventing its contents. Otherwise offer one short choice: **“Do you have documents or links I should use, or should I research suitable sources?”** If the user already said to research, do not ask again. If the request can proceed, do not block on optional materials.
3. Set only the missing production details that affect the result. Defaults: adult beginners, plain professional language, 15-minute lecture, Markdown storyboard, presenter script plus screen/board visuals. State assumptions briefly.
4. Research when required. Use primary documents, official guidance, original research, academic publishers, and specialist institutions. See `references/source-workflow.md`.
5. Build one teaching arc: a real question or problem → a concrete case → the governing idea → a visual model → application → limits → recall.
6. Write the presenter script and audience-facing material as separate layers. Use `references/presenter-template.md`.
7. Run the quality checks before delivery. Do not expose private answer keys or presenter-only notes as slide content.

## The two-layer rule

Every lecture has two clearly labelled layers:

- **PRESENTER ONLY — say / do:** the words to read aloud, questions to ask, pauses, reveal instructions, transitions, and source notes. The spoken script should sound natural when read. Do not write an essay and call it a script.
- **SHOW THE AUDIENCE — display:** the actual slide text, diagram, table, sequence, image brief, or board drawing. Keep this layer sparse. It is not a transcript and must not give away every explanation or answer.

Never create a student handout, full learner notes, or a slide deck full of paragraphs by default. Create those only when requested. Keep answers and teaching prompts in the presenter layer until the planned reveal.

## Lecture design

- Start with a question, decision, puzzle, or situation that matters to adults. State the practical outcome without hype.
- Organise by questions the audience needs answered, not by a list of textbook headings.
- Teach one core idea per beat. Move from familiar examples to formal terms and then to abstraction.
- Define each essential term before relying on it. Preserve accurate technical vocabulary; explain it in context instead of replacing it with vague words.
- Use this vocabulary ladder: **concrete scene → plain meaning → exact term → useful contrast → implication**.
- Humanise through human choices, constraints, stakes, consequences, and trade-offs. Never invent a personal story, quote, or emotional reaction. Label a constructed scenario **Hypothetical**.
- Add a real visual for every main concept. Prefer a clean comparison, causal chain, timeline, map, cycle, scale, quantity bar, step sequence, or annotated example. Show the diagram itself in the output; do not merely describe what a visual might contain.
- Put labels beside the parts they explain. Reveal complex visuals in stages. Use images only when they carry information; avoid stock-photo filler.
- For a procedure, calculation, or decision rule, model one full worked example before asking learners to try. Show the reasoning, not only the answer.
- Ask one or two purposeful audience questions. Put expected answers and likely misconceptions in the presenter-only layer. Give time to think before revealing an answer.
- Use a contrast or counterexample when it clarifies a boundary. State where an analogy breaks.
- End with a short synthesis and a retrieval prompt. Do not repeat the whole lecture in the conclusion.

## Spoken voice and vocabulary

Write for the ear. Use contractions when they sound natural. Vary sentence length. Keep each paragraph to one spoken move. Prefer active verbs and concrete nouns. Include pauses and transitions only where they guide attention.

Use precise vocabulary, not ornament. Words such as *influence*, *allocate*, *infer*, *correlate*, *justify*, and *trade-off* are useful when they say exactly what is meant. Define a technical term at first use. Avoid both fake simplicity and needless jargon.

Avoid filler such as “Today we are going to dive into,” “in today's world,” “it is important to note,” repeated previews, repeated summaries, over-signposting, motivational slogans, and fake audience banter. Do not add a story merely to make a point feel human. Use real source-backed cases or label invented ones as hypothetical.

## Visual and screen rules

- One main idea per slide/board state. Aim for one focal point, not an entire page of notes.
- Screen content should support the spoken explanation, not duplicate it word for word. Use short labels, one sentence at most when useful, and a diagram that carries the relationship.
- Show worked examples in steps. Do not show the final answer before the planned reveal.
- If a visual cannot be rendered in Markdown, give a build-ready layout: title, exact labels, relationships, sequence, and what is revealed when. Avoid vague directions such as “add an engaging image.”
- For video, add rough timecodes and cues for cut, zoom, diagram build, or on-screen text only where they improve comprehension.
- If a requested output requires actual slide files or images, create them only when the available tools support it. Otherwise provide a clear storyboard and identify that it is not a finished deck.

## Source and honesty rules

- Do not invent citations, facts, quotations, data, or details from unseen documents.
- Cite material claims in the script with compact source markers such as `[S1]`. Include full source details and URLs in a presenter-only source list.
- Distinguish established findings, interpretation, and illustrative examples. Mark important unsupported claims `UNVERIFIED` or omit them.
- Browse for changing facts and consequential topics such as health, law, finance, public policy, and current science. Give relevant dates and jurisdiction.
- If sources disagree, show the disagreement and its consequence. Do not force false certainty.
- Ask for user material when the lecture is supposed to follow a specific source or syllabus that is not available. Explain what is missing, and do not imply access to private drives or inaccessible links.
- Supplement user material with complementary sources where that improves clarity or verification. Explain which sources are core and which are supplementary.

## Length defaults

Plan spoken time at roughly 110–140 words per minute, including pauses and audience interaction. Treat this as an estimate, not a guarantee. For a 15-minute lecture, usually write about 1,500–1,900 spoken words. Reduce words when the visual carries the explanation; do not pad to meet a number. Break longer talks into beats of about 2–4 minutes.

## Output order

1. **Brief** — audience, outcome, duration, format, source basis, and assumptions; only a few lines.
2. **Run of show** — sequence and approximate time per beat.
3. **Lecture script + screen cues** — each beat contains presenter-only script, audience-facing visual/content, and the reveal or interaction cue.
4. **Presenter-only close** — anticipated questions, likely misunderstanding, and a short answer key where needed.
5. **Sources** — claim-linked source list with dates and access links.
6. **Production status** — `draft` or `ready_for_review`. Never claim testing or approval that did not occur.

## Quality gate

Before delivery, confirm:

- The outcome is observable and audience-relevant.
- The script can be read aloud without sounding like an essay or instruction manual.
- Every major concept has a visible, relevant visual next to its explanation.
- The screen layer contains less text than the spoken layer.
- There are no student notes or answer keys in the audience-facing layer unless requested.
- Technical vocabulary is accurate and explained.
- Procedures have a worked example before practice.
- Every audience question includes private answer guidance.
- Material claims are traceable to sources or marked uncertain.
- The ending synthesises rather than repeats.
- The script fits the stated duration within a reasonable range and contains no filler.
