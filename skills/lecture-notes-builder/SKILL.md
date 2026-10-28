---
name: lecture-notes-builder
description: Produce complete lecture notes on a given topic for adult learners who have no prior education in that topic, with at least one concrete visual example per concept. Grounded in established methods (Mayer's multimedia principles, cognitive load theory, worked examples, dual coding, Knowles' andragogy, retrieval practice). Use when asked to create lecture notes, class notes, teaching handouts, or beginner explanations for non-specialist adults on any topic.
---

# Lecture Notes Builder

Produces lecture notes for adults who are new to a topic, heavy on visual examples, and built on well-established instructional methods. The full method grounding is in `references/methods.md`; the fill-in output structure is in `references/output-template.md`.

## When to use

The user asks for lecture notes, class notes, a teaching handout, or a beginner's explanation of a topic, and the audience is adults with no prior education in that topic. Do not use this for expert audiences, exam cram sheets, or scripts for live delivery; adapt the intake questions instead of refusing.

## Intake (ask only what materially changes the notes)

Record answers; mark anything assumed as ASSUMED.

| Input | Why it matters |
|---|---|
| Topic and the one thing the learner should be able to do afterwards | Fixes the observable outcome before writing |
| Audience context (workplace, daily life, general interest) | Adults need to know why it matters to them (Knowles: need to know, problem-centered orientation) |
| Delivery format (markdown, print, web page, slides text) | Constrains the visual types available |
| Length or session duration | Fixes the number of segments |
| Language and reading level | Plain-language rule for francophone or second-language readers |
| What the learner already knows | The novice rule assumes zero topic knowledge, but adults bring life and work experience to connect to |

Default when inputs are missing: adult professionals in Réunion (French L1), plain English at A2-B1 reading level, markdown delivery, workplace-relevant examples, five to eight segments.

## Non-negotiable rules

1. Novice rule. Assume zero prior knowledge of the topic. Define every term at first use in the words of the glossary. No term appears before its definition.
2. One concept, one visual. Every major concept gets at least one visual example from the visual menu below. Visuals are concrete first, abstract second (dual coding).
3. Visual next to words. Each visual sits immediately beside the sentence it explains, not in a separate figure dump (spatial contiguity; avoid split attention).
4. One idea per segment. Short segments, simple-to-complex order, each segment ends before the next begins (segmenting; manage intrinsic load).
5. Worked example before practice. Every procedure or calculation is shown fully worked, step by step, before any "you try" task (worked-example effect for novices).
6. Say why up front. The notes open with what the learner will be able to do and why an adult should care (andragogy: need to know, readiness, intrinsic motivation).
7. Connect to adult experience. Examples draw on workplace, money, household, health, or civic life the reader already knows (andragogy: experience).
8. Cut decoration. No stock-photo language, side stories, or decorative visuals that do not carry meaning (coherence principle).
9. Retrieval checks. Each segment ends with one small question with its answer hidden below it; a final quick review of five questions with answers closes the notes (retrieval practice).
10. Source discipline. No invented facts, statistics, or citations. Factual claims list a source or are labelled UNSOURCED. Analogies are labelled as analogies and must be dropped when they mislead.

## Method map

Established method grounding and its canonical sources live in `references/methods.md`. Summary of what each method forces into the notes:

| Method | Rule it forces |
|---|---|
| Cognitive load theory (Sweller) | Segment, sequence simple to complex, worked examples, no split attention |
| Worked-example effect (Sweller, Renkl) | Full worked example with self-explanation prompts; faded steps only later |
| Mayer's multimedia principles | Words plus visuals, visuals adjacent, signal structure with headings and arrows, cut extras, pre-teach key terms |
| Dual coding theory (Paivio) | Concrete visual example for every concept; pictures beat prose for novel material |
| Andragogy (Knowles) | Why-it-matters opening, problem-centered segments, links to learner experience |
| Retrieval practice (Roediger and Karpicke) | Question with answer after each segment and at the end |

## Visual menu

Pick the cheapest type that carries the meaning. Every visual must be reproducible by the reader with pencil and paper, or present in the notes as text.

| Type | Use it for |
|---|---|
| Analogy picture | First contact with an abstract idea (e.g. electrical current as water flow) |
| Before / after pair | Showing what a change or decision does |
| Step strip | Any procedure: numbered boxes left to right |
| Comparison table | Two things confused easily (this vs that) |
| Flow diagram | Causes, sequences, decision paths |
| Cycle diagram | Recurring processes |
| Quantity bar or proportion visual | Numbers, sizes, shares |
| Map or layout | Anything spatial |
| Worked example block | Applied rules, calculations, filled-in forms |

Each visual entry in the notes carries three parts: what it shows, how to build or draw it, and the one sentence it must make obvious.

## Output structure

Full fill-in template in `references/output-template.md`. Skeleton:

1. Title and one-sentence promise (why an adult cares)
2. Before-you-start box: observable outcome, three key terms pre-taught, what the learner needs
3. Segments (one concept each): plain explanation, visual, concrete adult example, mini-check with answer
4. Worked example section
5. Common mistakes box
6. Glossary
7. Quick review: five questions with answers
8. Sources and status labels

## Quality gates (check before delivering)

- [ ] Every term defined at first use and in the glossary
- [ ] Every major concept has a visual, adjacent to its explanation
- [ ] Segments hold one idea each, simple to complex
- [ ] At least one fully worked example precedes any practice task
- [ ] Every check question has an answer
- [ ] Opening states why it matters to this audience
- [ ] Factual claims sourced or labelled UNSOURCED; analogies labelled
- [ ] No decorative filler
- [ ] Reading level matches the audience (default plain English)

## Honesty limits

These notes follow established methods; that does not guarantee learning for every reader. Do not claim tested effectiveness, classroom validation, or expert review that did not happen. Notes are a learning aid, not evidence of competence.

## Support files

- `references/methods.md` — the established methods, their claims, boundaries, and canonical sources
- `references/output-template.md` — the fill-in template for the finished notes
