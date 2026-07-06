# Frameworks

## Contents
1. SIPOC flow mapping
2. RACI role assignment
3. Control types
4. 5×5 risk matrix and scoring
5. Review cadences
6. Automation decision checks
7. Family-specific guidance

---

## 1. SIPOC flow mapping

Per stage, record: Supplier (who or what provides the input) → Input →
Process (the transformation, one verb phrase) → Output → Customer (who
consumes it). Add two fields SIPOC omits: Trigger (what starts the stage:
schedule, event, or manual) and Owner (one name, never a group).
Documented origin: process-improvement practice popularised within Six
Sigma programmes; used here as a recording format, not a certification
claim.

## 2. RACI role assignment

Responsible (does the work) · Accountable (one per task, answers for it) ·
Consulted (input before) · Informed (told after). Rules: exactly one A per
task; an R without an A is unowned work; more than two C per task signals
an over-consulted design.

## 3. Control types

- Preventive — stops the failure before it occurs (validation, checklist,
  access restriction, template).
- Detective — reveals the failure after it occurs (reconciliation, alert,
  audit log, review meeting).
- Corrective — restores operation after detection (rollback, backup
  restore, escalation path).
A material risk needs at least one preventive and one detective control.

## 4. 5×5 risk matrix and scoring

Score = Likelihood (1–5) × Impact (1–5).

| Likelihood | Meaning (working definition) |
|---|---|
| 1 | Not expected within a year |
| 2 | Possible within a year |
| 3 | Expected within a quarter |
| 4 | Expected within a month |
| 5 | Expected within a week or already occurring |

| Impact | Meaning |
|---|---|
| 1 | Absorbed without schedule or cost effect |
| 2 | Hours lost, no external effect |
| 3 | Days lost or minor external effect |
| 4 | Deadline, financial, or reputational damage |
| 5 | Legal exposure, irreversible loss, or system failure |

Bands: 1–4 accept and log · 5–9 monitor with detective control ·
10–14 mitigate with preventive control and owner · 15–25 stop the
activity until mitigated. Bands are the skill's working defaults; adjust
only with the user's stated tolerance.

## 5. Review cadences

- Daily signal: one glance-level indicator per active system (queue
  length, inbox zero state, red/green run status).
- Weekly operation: metrics against targets; SOP deviations logged.
- Monthly design review: risk register re-scored; kill criterion checked;
  one simplification considered.
Calendar entries are part of the deliverable: a cadence without a
scheduled slot does not exist.

## 6. Automation decision checks

Automate a step only when all hold: (a) executed ≥ weekly or ≥ 10 times
ahead; (b) inputs and outputs are fully specifiable; (c) failure is
detectable and reversible, or gated by human approval; (d) maintenance
cost stated and accepted. If the user supplies a quantitative decision
rule (for example a Net Decision Value framework), apply it as written in
their document; do not reconstruct it from its name.

Hard rules for automated steps: credentials in an environment or
properties store, never in source; a dry-run mode defaulting on; explicit
human confirmation before send, pay, publish, file, or delete; no silent
catch blocks; a written failure path.

## 7. Family-specific guidance

- Productivity: one capture point, one list of record, one weekly review.
  More than three lists is a design smell.
- Execution / workflow: define "done" per stage in observable terms;
  work-in-progress limits before adding stages.
- Automation pipeline: version every script; log every run with
  timestamp and outcome; test path separated from live path.
- Administrative pipeline: deadline-driven sequencing — the nearest
  binding date governs; every submission mirrored to an archive with
  filename convention and date; parallel filings tracked in one register.
- Time management: time is allocated by calendar block, not by list
  order; protect one deep-work block before scheduling anything else;
  review actual versus planned weekly.
- Risk management: the register is a living document with a review date
  per entry; risks without owners are unmanaged by definition; record
  near-misses, not only occurrences.
