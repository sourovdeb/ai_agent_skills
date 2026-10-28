# Test the skill

Test structure and behaviour separately. A successful load or trigger test does not prove the lectures are good.

## 1. Validate structure

Run the included lightweight check first:

```bash
python scripts/check_skill.py .
```

Then, in the environment that contains `skill-creator`, run its validator and packager. The path below matches one common installation; adjust it if yours differs:

```bash
python /mnt/skills/examples/skill-creator/scripts/quick_validate.py /path/to/lecture-presenter-builder
python /mnt/skills/examples/skill-creator/scripts/package_skill.py /path/to/lecture-presenter-builder /path/to/dist
```

Do not treat the lightweight checker as a replacement for the skill-creator validator.

## 2. Run behavioural evaluations

Use `/skill-creator` and give it the extracted source-folder path. Suggested instruction:

> Evaluate `/path/to/lecture-presenter-builder`. Run each case under `evals/` in a fresh context. For every case, produce one response using the skill and one baseline response without it. Grade each response against the criteria in that case's `graders/` folder. Save both outputs, grades, and pass/fail evidence to a separate results folder. Report critical failures and pass rates. Do not treat a trigger check as an output-quality test.

Cases:

- `compound-interest-live` — separate script and display; correct worked calculation.
- `correlation-causation-live` — accurate concepts, visible model, spoken voice.
- `source-required` — requests missing required material; invents no chapter content.
- `current-policy-live` — current official sources, dates, and scope.
- `not-a-lecture-request` — direct definition; no unnecessary lecture.

Run each case once first. Fix failures, then rerun changed cases. Repeat inconsistent cases three times. Inspect actual text, not only scores.

## 3. Manual rejection criteria

Reject outputs that:

- create student handouts or paragraph-heavy slides by default;
- merge presenter-only notes, audience content, citations, and answer keys into one layer;
- describe a visual without showing it or specifying a build-ready layout;
- invent contents of missing source material;
- make unsupported claims without uncertainty labels;
- reveal answers before the planned audience response;
- use fake stories, filler, repeated summaries, or unexplained jargon;
- omit a worked example for a procedure or calculation;
- claim testing or approval that did not occur.

## 4. Package

The distributable `.skill` package contains `SKILL.md` and references. The source ZIP retains evaluation cases and the checker. Behavioural testing is still required; packaging alone cannot establish quality.
