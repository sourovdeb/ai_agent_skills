---
name: cambridge-writer
description: Build or revise essays, articles, speeches, applications, statements, and long-form arguments using explicit thesis, paragraph-function, counterargument, evidence, register, and multi-pass editing checks. Use when the user needs structured persuasive or academic prose, substantive editing, word-count reduction, argument diagnosis, or a high-standard rewrite that preserves meaning and source boundaries.
metadata:
  version: "1.1.0"
  source-path: "skills/cambridge-writer/SKILL.md"
  source-commit: "02602051fcbbcc38b0ae3e7a18a6a9c83ec0e958"
---

# Cambridge Writer

## Aim

Produce defensible prose.
Preserve the user's purpose.
Preserve supplied meaning.
Expose unsupported reasoning.

The name is internal.
It implies no affiliation.
It is not certification.

## Use this skill

Use it for:
- essays;
- articles;
- op-eds;
- speeches;
- applications;
- statements;
- long-form arguments;
- substantive editing;
- argument diagnosis;
- word-count reduction.

Do not use it for:
- factual research alone;
- citation invention;
- legal conclusions;
- medical conclusions;
- live submission;
- document upload;
- source rewriting without permission.

Use domain skills first.
Then use this skill.

## Inputs

### Required

Establish these first:
1. the writing task;
2. the intended reader;
3. the output length;
4. the supplied source material;
5. the permission boundary.

For revision tasks, also establish:
- text to preserve;
- facts to preserve;
- citations to preserve;
- voice to preserve.

### Optional

Useful inputs include:
- marking rubric;
- publication venue;
- citation style;
- preferred spelling;
- personal voice sample;
- banned wording;
- deadline;
- audience knowledge;
- prior feedback.

### Missing inputs

IF a missing detail is harmless:
- state the assumption;
- proceed.

IF it changes correctness:
- preserve partial work;
- identify the gap;
- stop that branch.

Examples:
- missing audience;
- missing source;
- missing word limit;
- missing citation evidence.

## Output contract

### New writing

Return:
1. task interpretation;
2. one-sentence thesis;
3. argument skeleton;
4. draft;
5. counterargument handling;
6. evidence notes;
7. edit-pass findings;
8. final text;
9. limits.

### Revision

Return:
1. diagnosis;
2. preservation notes;
3. revised text;
4. three leverage changes;
5. unresolved factual gaps.

Do not silently change:
- facts;
- dates;
- names;
- quotations;
- citations;
- legal claims;
- medical claims;
- personal-history details.

## Completion test

The output is complete when:
- task purpose is satisfied;
- thesis is contestable;
- structure is coherent;
- each paragraph has function;
- evidence status is visible;
- counterargument is fair;
- register stays controlled;
- requested length is met;
- supplied meaning is preserved;
- unresolved gaps are named.

Do not claim completion when:
- essential sources are missing;
- citations remain invented;
- quotations are unverified;
- required facts conflict;
- user approval is needed;
- live submission remains pending.

## Evidence labels

Use these labels internally.
Expose them when useful.

- `SOURCE`: supported directly.
- `USER`: supplied by user.
- `INFERENCE`: reasoned conclusion.
- `JUDGMENT`: rhetorical choice.
- `UNKNOWN`: not verified.

Never convert `UNKNOWN` silently.

## Method

### Phase 1 — Task frame

Write five lines:
- purpose;
- audience;
- genre;
- length;
- evidence boundary.

Set three dials:
- distance;
- temperature;
- convention.

Examples:
- first-person / impersonal;
- cool / persuasive;
- British / American.

Do not invent venue rules.

### Phase 2 — Thesis

Draft one sentence.

Test it:
- contestable?
- specific?
- supportable?
- answerable here?

A topic is insufficient.
A slogan is insufficient.

### Phase 3 — Skeleton

Write one sentence per paragraph.

Each sentence states:
- the paragraph claim;
- its function;
- its evidence need.

Read only skeleton lines.

They must connect logically.

If they do not:
- repair structure first.

### Phase 4 — Objection

State the strongest objection.

Do not weaken it.

Then choose:
- answer;
- concede;
- narrow thesis;
- defer unsupported point.

Never fabricate rebuttal evidence.

### Phase 5 — Draft

Prefer openings that enter:
- the problem;
- a tension;
- a case;
- a stake.

Avoid generic throat-clearing.

For each paragraph:
1. claim;
2. evidence;
3. analysis;
4. link.

Evidence never self-interprets.

State what it proves.
State what it cannot prove.

Use transitions for logic.
Avoid transition filler.

Conclusions should answer:
- what follows?
- what changes?
- where is the boundary?

### Phase 6 — Three passes

Run in this order.

#### Pass A — Argument

Check:
- relevance;
- sequence;
- redundancy;
- objection fairness;
- evidence coverage.

Cut only when useful.

Do not force percentages.

#### Pass B — Sentences

Check:
- clear actors;
- active verbs;
- nominalizations;
- empty openers;
- avoidable passive voice;
- filler;
- ambiguity.

Passive voice is allowed.
Use it when functional.

Precision beats brevity.

#### Pass C — Ear

Read or simulate aloud.

Check:
- sentence rhythm;
- repetition;
- overload;
- awkward cadence;
- unintended ambiguity.

Do not optimize cadence
against factual meaning.

## Register control

Lock these before drafting:
- audience;
- distance;
- temperature;
- spelling convention;
- citation convention.

Change them only deliberately.

## Genre routes

### Academic essay

Require:
- argument skeleton;
- source traceability;
- citation consistency;
- precise hedging;
- counterargument.

Never create citations.

If sources are missing:
- mark citation gaps;
- do not invent them.

### Personal statement

Prefer:
- specific experience;
- demonstrated curiosity;
- concrete action;
- reflection;
- fit grounded in evidence.

Never invent achievements.

### Op-ed

Prefer:
- early thesis;
- one central argument;
- concrete stakes;
- explicit objection;
- defined boundary.

Verify current facts.

### Speech

Prefer:
- shorter sentences;
- spoken rhythm;
- deliberate repetition;
- audience cues;
- breath-friendly phrasing.

Written delivery differs.
Do not claim performance testing.

## Editing supplied drafts

Diagnose before rewriting.

Order of repair:
1. argument;
2. structure;
3. paragraph function;
4. sentence clarity;
5. surface polish.

Preserve author voice.

Do not replace voice
with generic formality.

When rewriting materially:
- explain major changes;
- preserve factual content;
- flag factual conflicts.

## Style requests

If asked for style:
- extract high-level traits;
- preserve user meaning;
- avoid copying passages;
- avoid invented quotations.

Prefer traits such as:
- compressed sentences;
- dry irony;
- concrete imagery;
- periodic structure;
- analytic distance.

## Illumination

For complex arguments, add one:
- claim map;
- paragraph map;
- objection map;
- evidence ladder;
- before/after annotation.

Use Markdown first.

Use HTML/SVG when useful.

Every visual needs:
- caption;
- labels;
- alt text;
- prose equivalent.

Visuals explain structure.
They do not prove claims.

## Verification

### Source fidelity

For supplied documents:
- preserve quotations exactly;
- preserve citation identity;
- preserve factual chronology;
- preserve requested ordering;
- record material changes.

### Current facts

If a claim is current:
- verify when tools exist;
- prefer primary sources;
- cite the actual source.

If tools are unavailable:
- mark `UNKNOWN`;
- avoid firm wording.

### Claims in prose

Check each consequential claim.

It must be:
- sourced;
- user-provided;
- clearly inferential;
- clearly judgmental;
- or removed.

## No-install route

Recommended route:
- browser chat;
- supplied text;
- Markdown output.

No software is required.

Optional HTML needs:
- any modern browser.

Do not require:
- Python;
- Docker;
- n8n;
- paid APIs;
- local models.

## Small-model route

For smaller models:
1. frame task;
2. build thesis;
3. build skeleton;
4. draft one section;
5. validate section;
6. continue;
7. run final passes.

Limit choices per stage.

Do not claim parity.

## Failure handling

### Missing evidence

IF support is missing:
- mark the claim;
- narrow wording;
- request source later;
- continue safe sections.

### Conflicting sources

IF sources conflict:
- show the conflict;
- do not resolve silently;
- separate interpretations.

### Unsupported citation

IF citation cannot verify:
- remove the claim;
- or mark citation needed.

Do not invent metadata.

### Tool unavailable

IF browsing fails:
- preserve draft work;
- mark verification gaps;
- do not install substitutes.

### Long input

IF context becomes limited:
- preserve source coverage;
- chunk by section;
- checkpoint completed ranges;
- never truncate silently.

### Live submission

IF submission is requested:
- prepare final text;
- request authorization;
- submit separately.

### Retry rule

Retry once only.

Retry for:
- malformed extraction;
- transient retrieval failure;
- broken optional rendering.

Then use another route.

## Stop conditions

Stop when:
- acceptance checks pass;
- user approval is required;
- essential evidence is unavailable;
- requested scope is complete.

Return partial work honestly.

## Supporting files

Use when needed:
- `START_HERE.md`
- `HOST_PROMPT.md`
- `TASK_PROMPT_TEMPLATE.md`
- `EXAMPLES.md`
- `DEPENDENCIES_AND_FALLBACKS.md`
- `references/CRAFT_NOTES.md`
- `examples/argument_map.html`
- `TEST_PLAN.md`
- `TEST_RESULTS.md`

## Lineage

Source:
`skills/cambridge-writer/SKILL.md`

Source commit:
`02602051fcbbcc38b0ae3e7a18a6a9c83ec0e958`

Upgrade type:
`RESTRUCTURE`

Validation status:
`STATIC_ONLY`
