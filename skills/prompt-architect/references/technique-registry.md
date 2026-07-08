# Technique Registry

All rows LIVE-VERIFIED 2026-07-08 unless labeled.

| # | Technique | What to write | Source |
|---|---|---|---|
| 1 | Clarity and specificity | Task verb, audience, output form, length, constraints, success criteria | Anthropic docs, be-clear-and-direct |
| 2 | Multishot examples | 1–3 input-to-output pairs of the wanted result | Brown et al. 2020; Anthropic docs |
| 3 | Structural separation | Labeled tags around instructions, context, data, examples | Anthropic docs, XML tags |
| 4 | Reasoning-then-answer | Request stepwise work in one block, final answer in another | Wei et al. 2022; Kojima et al. 2022; Anthropic docs |
| 5 | Decomposition and chaining | One question per prompt; feed each output into the next; easy sub-problems first | Zhou et al. 2022; Anthropic docs, chaining |
| 6 | Role and context | One sentence of who the answerer is and why the task exists | Anthropic docs, role prompting |
| 7 | Escape hatch | Explicit permission to answer "insufficient information" | Anthropic docs; reduces invented answers |
| 8 | Output specification | Exact format: table columns, JSON keys, word limit, language | Anthropic docs |
| 9 | Placement | Long material first, instructions and question last | Anthropic docs, long-context |
| 10 | Self-check line | "Before finishing, verify the answer against [criteria]" | Anthropic docs, best practices |
| 11 | One-variable iteration | Change one element per test run; keep a log | Anthropic docs, empirical development |
| 12 | Prefill or opening constraint | Begin the answer format for the model where the platform allows | Anthropic docs |

Survey ground for the field's terminology: Schulhoff et al. 2024, The Prompt Report (arXiv:2406.06608).

## Master template (rebuild target)

```
<role>You are [one-line role]. The task exists because [one-line purpose].</role>
<goal>[User's intent, verbatim.]</goal>
<context>[Facts the answerer cannot know. Placeholders for unknowns: {LIKE_THIS}.]</context>
<data>[Material to work on, if any. Long material goes here, before everything below.]</data>
<task>[One task verb and one deliverable.]</task>
<example>[One input-to-output pair, only when the format is non-obvious.]</example>
<format>[Exact output form, length, language.]</format>
<rules>Reason step by step in a separate block before the answer. If information is insufficient, say so instead of guessing. Before finishing, verify the answer against: [success criteria].</rules>
```

## Compact small-model variant (under 1,500 characters)

Role sentence · goal verbatim · three context facts maximum · one task verb · format in one line · escape hatch line. Drop the example and the self-check when space forces the choice; keep the escape hatch always.

## Diagnosis checklist (Step 1)

- Task verb present? Absent → technique 1.
- Output form and length stated? Absent → techniques 1, 8.
- Context the answerer cannot know supplied? Absent → technique 6 plus context block.
- Parts mixed in one paragraph? Yes → technique 3.
- Two or more questions in one ask? Yes → technique 5.
- Multi-step reasoning required? Yes → technique 4.
- Invention risk on missing facts? Yes → technique 7.
- Long pasted material? Yes → technique 9.

## Worked pairs

Raw: "Write about my CELTA dispute."
Rebuilt (abridged): role — administrative-writing assistant; goal verbatim; context — dispute stage, addressee authority, three documented facts with dates; task — draft one two-paragraph status summary; format — formal register, no emotional language, every claim cited to document and date; rules — reasoning block first, insufficient-information escape hatch. Changes: techniques 1, 3, 6, 7, 8.

Raw: "Why is my code slow, fix it."
Rebuilt (abridged): data — the code, first; context — language, input size, runtime observed versus expected; task 1 — identify the dominant cost with reasoning shown; task 2 (chained) — propose the smallest change and predicted effect; format — diff plus one-line rationale; rules — verify against the stated input size. Changes: techniques 4, 5, 8, 9, 10.

## Explain-mode order (context handoff)

What it is → current state → wanted end state → hard constraints → one example of done → the question, last.
