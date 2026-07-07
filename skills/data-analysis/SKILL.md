---
name: data-analysis
description: Question-first data analysis with an audit trail — from raw CSV, spreadsheet, logs, survey, or database export to a defensible answer. Trigger on analyze this data, find patterns, why did this metric change, compare these groups, build a dashboard, clean this dataset, is this significant, forecast, or any file of rows and columns arriving with a vague ask. Method — lock the question via objective-first, audit data quality before any statistic, describe before inferring, effect sizes over p-values, uncertainty stated with every number, plots that earn their ink, and a reproducible script so every figure can be regenerated. Chains into self-debate on contested interpretations and cambridge-writer or writer-agent for the write-up.
---

# Data Analysis

An answer nobody can check is an opinion with decimals. Every analysis under this skill produces three things: the answer with its uncertainty, the audit trail that produced it, and the script that regenerates it.

## Core rule: the question owns the analysis

No statistic before the question is fixed (run objective-first if absent): what decision does this analysis serve, what would each possible answer change? An analysis that cannot change any decision is stopped at step 0 and said so.

## The pass

**1. Question lock.** One sentence: population · variable(s) · comparison · timeframe · decision served. Classify the ask: describe, compare, explain, predict, or detect change. The class picks the method; never the reverse.

**2. Data audit — before any analysis.**
- Provenance: who collected it, how, what incentive shaped it.
- Shape: rows, columns, types, units; a data dictionary written or requested.
- Missingness: how much, and whether it is random or structured (structured missingness is a finding, not a nuisance).
- Duplicates, impossible values, unit mixes, timezone and encoding traps.
- Selection: who is NOT in this data; what the data cannot say.
Output: a defect table with a severity column. RED defects block inference until resolved or explicitly waived by the user in writing.

**3. Describe first.** Distributions, counts, ranges, and the five-number summary per key variable — plotted before summarized, because summary statistics hide bimodality and outliers (Anscombe's quartet is the standing warning). No model until the describer pass has run.

**4. Compare and infer — with discipline.**
- Effect size with confidence interval first; p-value second if at all. "Significant" without magnitude is banned output.
- Base rates stated before percentages ("40% increase" of what denominator).
- Correlation labeled as correlation; causal language only with design that supports it (randomization, natural experiment, or explicit causal assumptions named).
- Multiple comparisons declared: how many things were tested, not just the one that worked.
- Simpson's paradox check on any grouped comparison: does the direction hold within subgroups?

**5. Change and anomaly questions.** For "why did the metric move": segment before theorizing (mix shift vs within-segment change), check the denominator, check the instrumentation (did the measurement change, not the world), then rank remaining hypotheses by evidence.

**6. Visualize honestly.** Axis from zero for bar charts of magnitude; label units and n; one message per chart; no dual axes without a stated reason; uncertainty shown (bands, intervals), not hidden. Follow the repo dataviz conventions where present.

**7. Report.** Answer in the first sentence, with uncertainty. Then: what the data can NOT conclude (selection, confounding, power), the defect table, and the decision recommendation phrased against the step-1 question. Numbers rounded to decision-relevant precision.

**8. Reproduce.** Every figure and number traces to a script or documented formula chain kept beside the report. Raw data untouched; transformations happen in the script. A second run must produce the same numbers.

**9. Self-check.** Run the self-debate pass on the interpretation: strongest alternative explanation of the same numbers, stated and answered in the report.

## Anti-patterns

- Opening a modeling library before completing step 2 and 3.
- Answering a different, easier question than the one asked, silently.
- "The data shows" for what the analyst chose; assumptions belong in the report.
- Deleting outliers without a logged rule; cleaning that cannot be replayed.
- Dashboards as deliverable when the question needed one number and a sentence.

## References
- Anscombe (1973) — identical statistics, different data; plot first
- Cohen; Wasserstein & Lazar (2016, ASA statement) — effect sizes and p-value limits
- Tufte, *The Visual Display of Quantitative Information* — data-ink honesty
- Huff, *How to Lie with Statistics* — denominator and axis discipline
