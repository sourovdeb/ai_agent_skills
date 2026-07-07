---
name: system-design
description: Design a complete, documented operating system of any kind — productivity systems, execution and workflow systems, automation pipelines, administrative pipelines, time-management systems, and risk management and assessment frameworks. Trigger whenever the user asks to "design a system," "build a workflow," "create a pipeline," "organise my process," "set up a routine," "automate this process," "build a risk register," "assess the risks," "create an SOP," or describes recurring work that needs structure, even if the word "system" is absent. Also trigger for requests to improve, audit, or stress-test an existing system. Output is a System Design Dossier: components, flows, roles, procedures, metrics, risk register, and review cadence — every claim grounded, no speculation.
---

# System Design

Turn a goal plus constraints into a documented, operable system. A system
here means: defined inputs, defined transformations, defined outputs,
named owners, written procedures, measurable checkpoints, and a maintained
risk register. If any of those is missing, the design is not finished.

## Operating doctrine

1. Zero hypothesis. Every design decision cites its ground: a user
   statement, a document, an official source, or a stated assumption
   marked ASSUMPTION and confirmed before build.
2. Documentary precision. Name concrete tools, files, fields, and dates.
   "A tracking sheet" is not a component; "RISK_REGISTER.md, columns per
   references/templates.md §3, reviewed Mondays" is.
3. The user retains control. Irreversible or externally visible steps
   (send, pay, publish, file, delete) always terminate in a human
   approval gate. Automation prepares; the owner executes.
4. Simplest structure that satisfies the requirement. Every component
   must earn its maintenance cost; state the cost when proposing it.
5. If the user's own decision framework (for example a Net Decision
   Value rule set) is present in context or memory, apply it as supplied.
   Never reconstruct such a framework from memory of its name alone.

## Workflow

### Step 1 — Frame
Capture: purpose (one sentence), boundary (inside / outside scope),
actors, constraints (time, budget, tools, legal), and the failure
definition — what outcome the system exists to prevent. Ask only for
what is missing; pull the rest from the conversation.

### Step 2 — Classify
Identify the system family and read the matching section of
`references/frameworks.md` before designing:
productivity · execution/workflow · automation pipeline ·
administrative pipeline · time management · risk management.
Hybrid requests combine sections.

### Step 3 — Map
Draw the flow: inputs → stages → outputs, with an owner and a trigger per
stage (SIPOC form, frameworks §1). Mark every human approval gate.
Assign roles with RACI (frameworks §2) when more than one actor exists.

### Step 4 — Specify
Fill the System Spec template (`references/templates.md` §1). Write one
SOP (§2) per recurring procedure. For automation: name the runtime,
credential store, failure path, and dry-run default — no secrets in
source, no silent error swallowing.

### Step 5 — Risk pass
Build the risk register (templates §3) using the 5×5 likelihood–impact
matrix (frameworks §4). Every risk gets an owner, a control type
(prevent / detect / correct), and a review date. A system without a
risk register is returned to Step 4.

### Step 6 — Instrument and schedule
Define 2–5 metrics with unit, source, target, and reader. Set the review
cadence (frameworks §5): daily signal, weekly operation, monthly design
review. State the kill criterion — the observable condition under which
the system is retired or redesigned.

### Step 7 — Deliver
Output the System Design Dossier in this order: Purpose · Boundary ·
Flow map · Components · Roles (RACI) · SOPs · Automation spec (if any) ·
Risk register · Metrics · Review cadence and kill criterion · Open
assumptions. Close with the assumptions list; never bury them.

## Quality bar

Reject your own draft if: any stage lacks an owner or trigger; any
automation lacks a failure path; any risk lacks a control and owner; any
metric lacks a unit and source; or any claim lacks a ground. Fix, then
deliver.

## References

- `references/frameworks.md` — SIPOC, RACI, control types, 5×5 risk
  matrix with scoring bands, review cadences, automation decision checks.
- `references/templates.md` — System Spec, SOP, Risk Register, and
  Dossier skeletons, copy-ready.
