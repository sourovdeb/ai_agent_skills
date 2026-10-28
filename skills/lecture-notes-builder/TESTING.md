# Test the skill

Test two separate things:

1. **Structure:** front matter, references, and package files are valid.
2. **Behaviour:** the skill creates useful notes without adding filler.

The cases live in `evals/<case-name>/`. Each case has a `prompt.md` and at least one grader under `graders/`. Do not replace these with the legacy `evals.json` format if your skill-creator version expects case folders.

## 1. Validate structure

Run this in the environment that contains your skill-creator installation:

```bash
python /mnt/skills/examples/skill-creator/scripts/quick_validate.py /path/to/lecture-notes-builder
```

Adjust the path if your installation differs.

## 2. Run the output cases

Use `/skill-creator` with this instruction, replacing the path with the extracted folder's path:

> Evaluate the skill at `/path/to/lecture-notes-builder`. Run all five case folders under `evals/`. For each case, use a fresh context, run once with the skill and once without it, and grade the output using the grader file in that case. Save outputs and grades to a sibling workspace. Report critical failures and pass rates. Do not run only a description-trigger test.

Start with these cases:

- `compound-interest` — visuals and worked calculation.
- `confirmation-bias` — human voice and abstract concepts.
- `discount-calculation` — procedural accuracy.
- `current-french-benefits` — current sources and caveats.
- `not-a-lecture-request` — negative control against over-triggering.

Run each case in a fresh context. Compare a run with the skill against a baseline without the skill. Inspect both outputs. Keep the grader's pass/fail evidence with the run results. Start with one run per case; repeat changed or unstable cases three times.

The `scripts/run_eval.py` found in some skill-creator releases tests **whether a description triggers a skill**. It is not necessarily the output-quality runner. Check its local help before using it:

```bash
python /mnt/skills/examples/skill-creator/scripts/run_eval.py --help
```

Do not treat a trigger pass as proof of output quality.

## 3. Manual acceptance gates

Reject an output if any of these occur:

- It describes a visual but does not show one.
- A procedure lacks a complete worked example.
- A calculation is incorrect.
- A key factual claim has no source and is not labelled `UNSOURCED`.
- Review questions or answers are missing.
- The notes repeat themselves or pad sections to hit a word count.
- An unrelated direct question gets turned into lecture notes.

## 4. Package

```bash
python /mnt/skills/examples/skill-creator/scripts/package_skill.py \
  /path/to/lecture-notes-builder \
  /path/to/dist
```

Packaging checks file structure. Behaviour testing checks usefulness. They are separate checks.
