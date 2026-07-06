---
name: universal-upgrade
description: Source-anchored upgrade methodology for ANY artifact — script, codebase, book, research paper, blog post, YouTube script, course, recipe, product, config, prompt, email template, or workflow. Trigger whenever the user asks to "upgrade," "improve," "enhance," "refine," "modernize," "optimize," "polish," "make better," "level up," "rework," or produce a "v2" of anything — even when the artifact type is unusual or the word "upgrade" is absent. The pass — audit the current version fully, pull the best available tried-and-tested sources (official docs, standards, peer-reviewed work, widely adopted maintained references), build a severity-ranked gap table, then rewrite so the result is easy to use, easy to navigate, easy to read, easy to understand, and demonstrably higher quality — every substantive change justified by a named source or explicitly labeled. Never upgrade from opinion alone.
---

# Universal Upgrade

Turn an existing artifact into a measurably better version, with every change traceable to a concrete, tried-and-tested source.

## Core rule

no source, no change

Every substantive change cites a source or carries a label — DOCUMENTED / RECOLLECTION-ONLY / INFERRED. Cosmetic edits (typos, spacing) are exempt. Preference presented as fact is fabrication.

## The pass

### 0. Frame

One table before touching the artifact: artifact type · intended user · what "better" means here (3–5 measurable criteria) · constraints that must survive (working behavior, mandatory wording, voice, dependencies, runtime). If the user has standing compliance gates, list them here — a gate failure is blocking regardless of other quality.

### 1. Baseline audit

Read the whole artifact. Inventory four buckets: works (preserve), broken (fix), missing (add), dead weight (cut). Never upgrade blind or partially read.

### 2. Source hunt

Gather 3–7 sources per improvement area, best tier available:

| Tier | Source type | "Tried and tested" test |
|------|-------------|-------------------------|
| 1 | Official docs, standards bodies, primary law/specs | Current version, publisher-maintained |
| 2 | Peer-reviewed papers, official style guides | Cited, not retracted, recent for the domain |
| 3 | Widely adopted maintained references (canonical textbooks, major active repos) | Active maintenance, broad adoption, version-pinned |
| 4 | Named-expert practitioner guides | Track record, cross-confirmed by ≥2 independent sources |

**Reject:** single-source folk claims, abandoned projects, undated advice, marketing copy.

Verify live when tools allow; otherwise label RECOLLECTION-ONLY and say so in the deliverable.

### 3. Gap table

Current state vs sourced best practice. Columns: # · issue · severity (blocking / material / minor) · evidence in artifact · source for the fix.

- **Blocking** = broken, unsafe, non-compliant, or fails a Step 0 criterion.

### 4. Execute

Fix blocking, then material, then minor. Preserve everything inventoried as working. Apply the usability standard and the matching artifact hooks below.

### 5. Verify

- **Code:** dry-run or lint before delivery; never claim "tested" what was not run.
- **Citations:** every referenced source resolvable, or labeled.
- **High-stakes output** (publishes, sends, pays, legal, deadline-bound): chain into socratic-self-review before delivery.

### 6. Deliver

Upgraded artifact + changelog table: # · change · why · source. State residual uncertainties plainly. Remind the user to persist the output (repo/Drive) — session files do not survive the session.

## Usability standard (every artifact)

- **Use:** works first try for the intended user; safe defaults (dry-run/test-mode wherever an action is irreversible); one obvious entry point.
- **Navigate:** TOC or section map if longer than ~2 pages/screens; consistent descriptive headings and names; numbered steps for procedures.
- **Read:** short sentences, concrete words, one idea per paragraph; jargon defined at first use or cut; tables for data, prose for reasoning.
- **Understand:** one worked example per non-obvious concept; what → why → how, in that order; no unexplained magic values.

## Artifact hooks

### Script/code
- runtime and versions pinned and stated in a header
- secrets never inline (env vars / PropertiesService only)
- errors handled and logged
- irreversible actions gated behind confirmation with dry-run defaulting to true
- comments explain why, not what

### Book / long document / course
- structure map first
- consistent unit template
- progressive difficulty
- each unit self-contained: objective → content → example → check

### Research paper
- claims-to-citations 1:1
- method reproducible from the text alone
- limitations explicit
- target journal's template and word limit obeyed
- similarity check before submission

### Blog / YouTube script
- hook in the first two lines / fifteen seconds
- one core claim per piece
- sources linked or on-screen
- single CTA

### Recipe
- exact quantities and units
- steps in execution order
- times and temperatures stated
- substitutions and failure points named

### Product / config / workflow
- every setting justified
- rollback path documented
- before/after states shown

## Stop criterion

Stop when all Step 0 criteria pass, no blocking or material gap remains open, and one re-read surfaces no new concrete issue. Do not gold-plate; upgrading past the criteria is its own failure mode.

## Anti-patterns

- Rewriting working parts to taste.
- "Best practice" with no named source.
- Polishing form while a blocking substance issue stands.
- Citing sources not actually consulted.
- Deleting user constraints (voice, mandatory wording, structure) in the name of quality.
