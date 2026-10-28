---
name: lecture-notes-builder
description: Create clear, visual-first lecture notes for adults who are new to a topic. Use for class notes, lecture notes, video-lecture notes, teaching handouts, and beginner explanations across subjects. Adapt to the requested language, audience, format, and length.
---

# Lecture Notes Builder

Create notes that help a beginner understand, remember, and use an idea. Treat the reader as an intelligent adult. Do not confuse completeness with length.

## Workflow

1. Identify the topic and the useful action the learner should take afterwards.
2. Ask one concise question only when a missing detail would change the result. Otherwise proceed and state any important assumption briefly.
3. Build a concept sequence: familiar situation → core idea → how it works → practical use → limits or exceptions.
4. Choose the requested format. For speaking or video work, use speaker notes or a script when requested; keep the same learning design.
5. Draft the notes using `references/output-template.md`. Replace every placeholder and remove guidance text. Drop sections that do not apply.
6. Check the output against the quality gates below before delivering it.

### Defaults when details are missing

- Audience: adults with no prior knowledge of the subject.
- Language: the user's language; otherwise plain, professional English.
- Format: Markdown.
- Length: enough to teach the topic without padding; usually five to seven concepts for a 20–30 minute lesson.
- Examples: work, money, home, health, or civic life, chosen to fit the topic.
- Segment length: about 120–200 words. Go longer only when needed; never pad to hit a target.
- Status: `draft` unless review has actually occurred.

## Teaching rules

- Start with the outcome and why it matters in real life.
- Teach one main concept per segment. Order concepts from concrete to abstract and simple to complex.
- Define unfamiliar technical terms at first use. Keep useful technical vocabulary; explain it rather than replacing it with vague words.
- Use this vocabulary ladder: concrete situation → plain explanation → exact term → useful example → limit or counterexample.
- Start with a situation or example. Then explain the idea and name it.
- Put each visual beside the explanation it supports.
- Every major concept needs a **visible visual**, not just a description of one. Prefer an ASCII diagram, a small table, a step strip, a flow, a cycle, a comparison, or a quantity bar. Add a short caption explaining what the visual reveals.
- Use an analogy only when it clarifies the concept. Label it **Analogy** and explain where it stops being accurate.
- Give every concept a concrete adult example. Mark invented figures or scenarios as **Hypothetical**.
- Show a full worked example before asking beginners to solve a similar procedure, calculation, or decision task.
- Add one short retrieval question per segment. Put its answer in a collapsible block for web/Markdown, or in an answer key for print.
- End with a short review and answers. Ask for recall, explanation, and transfer—not only definition recall.
- Include common mistakes only when they are likely. Explain both the cause and the correction.

## Human voice and vocabulary

Write like a teacher explaining an idea to a capable adult. Be direct, grounded, and respectful.

Humanise the topic through a recognisable decision, constraint, consequence, or trade-off. Do not add fake personal stories, forced empathy, jokes, or motivational slogans.

- Use precise nouns and verbs. Prefer `estimate`, `compare`, `allocate`, or `influence` when those are the right words; explain unfamiliar words in context.
- Use everyday language around key technical terms. Keep distinctions that matter.
- Mix short sentences with fuller explanations. Avoid choppy, repetitive sentence patterns.
- Use concrete details that serve the lesson. Do not invent personal stories or claim to know how the reader feels.
- Explain why an idea matters without marketing language.
- Avoid filler openings, repeated summaries, fake quotations, decorative anecdotes, and phrases such as “in today's world,” “let's dive in,” or “it is important to note.”
- Do not add synonyms just to sound sophisticated. Good vocabulary means exact meaning, not ornament.
- Do not oversimplify, talk down to adults, or remove necessary complexity. Explain complexity in stages.
- State uncertainty and competing explanations when the evidence requires them.

## Research and source discipline

- Browse when facts may have changed, the user requests sources, or the topic is legal, medical, financial, scientific, or otherwise consequential.
- Prefer primary research, official guidance, recognised academic publishers, and authoritative institutions. Use sources that directly support the claims made.
- Attach citations to the claim or paragraph they support. Avoid unsupported statistics and invented references.
- If a substantive claim cannot be checked, label it `UNSOURCED` or remove it. Do not label hypothetical teaching examples as facts.
- Date time-sensitive guidance. Separate facts, interpretations, and recommendations.
- Do not present an analogy as proof. State its limits.
- The notes are a learning aid. Never claim that a learner has mastered the topic, or that the notes were tested or reviewed, unless that actually happened.

## Methods to apply

Use methods when they serve the topic; do not name-drop them in learner-facing notes. The full grounding, sources, and boundary conditions for each method are in `references/methods.md`.

- **Cognitive load:** one main idea per segment; remove material that does not help.
- **Multimedia and dual coding:** pair words with relevant diagrams; keep them together.
- **Pre-training:** define a few essential terms before the main explanation.
- **Worked examples:** model each unfamiliar procedure before independent practice.
- **Retrieval practice:** ask learners to recall before showing answers.
- **Spacing and transfer:** where useful, add a brief practice plan for later review and a new-context question.
- **Adult learning:** explain the purpose and connect ideas to situations adults recognise.
- **Feedback and contrast:** show why a correct example works; use a non-example when it exposes a common misconception.

## Quality gates

Before delivery, confirm:

1. The opening names a useful outcome and its relevance.
2. Technical terms are defined at first use.
3. Each major concept has one visible, relevant visual beside the explanation.
4. Every segment has a concrete example and a retrieval check with an answer.
5. Procedures include a complete worked example before practice.
6. The sequence moves from basic ideas to harder ones.
7. The prose sounds natural and contains no padding or repeated explanations.
8. Important factual claims are sourced or marked `UNSOURCED`.
9. The glossary contains only terms actually used.
10. The status is honest: `draft` or `ready_for_review`.

If a requested format cannot display a visual well, use a text diagram or an integrated table. Never replace the visual with decorative imagery or a separate figure dump.
