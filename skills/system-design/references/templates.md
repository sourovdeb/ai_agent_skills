# Templates

## Contents
1. System Spec
2. SOP (Standard Operating Procedure)
3. Risk Register
4. System Design Dossier skeleton

---

## 1. System Spec

```
SYSTEM: <name>            VERSION: <x.y>       DATE: <YYYY-MM-DD>
PURPOSE: <one sentence — what outcome this system produces>
BOUNDARY: IN: <...>  OUT: <...>
OWNER: <one name>
FAILURE DEFINITION: <the outcome this system exists to prevent>

STAGES
| # | Stage | Trigger | Owner | Input | Output | Approval gate? |
|---|-------|---------|-------|-------|--------|----------------|

COMPONENTS
| Component | Type (tool/file/script/meeting) | Location | Maintenance cost |
|-----------|--------------------------------|----------|------------------|

ASSUMPTIONS (each marked CONFIRMED or OPEN)
- ...
```

## 2. SOP

```
SOP: <procedure name>     SYSTEM: <name>     VERSION: <x.y>
FREQUENCY: <cadence>      OWNER: <name>      DURATION: <estimate>
PRECONDITIONS: <what must be true before starting>
STEPS
1. <verb-first instruction, one action per line>
2. ...
COMPLETION CHECK: <observable condition that means "done">
FAILURE PATH: <what to do when a step fails; who is notified>
```

## 3. Risk Register

```
| ID | Risk (event, not theme) | L | I | Score | Band | Control (P/D/C) | Owner | Review date | Status |
|----|-------------------------|---|---|-------|------|-----------------|-------|-------------|--------|
```
Rules: one event per row ("supplier misses deadline", not "supplier
issues"); score = L × I per frameworks §4; every row has an owner and a
review date; closed risks are struck through, never deleted.

## 4. System Design Dossier skeleton

```
# <System name> — Design Dossier
DATE: <YYYY-MM-DD>   VERSION: 1.0   DESIGNER: <name>   GROUNDS: <sources>

1. Purpose
2. Boundary
3. Flow map (SIPOC + triggers + gates)
4. Components
5. Roles (RACI)
6. SOPs
7. Automation spec (if any: runtime, credentials, dry-run, failure path)
8. Risk register
9. Metrics (name · unit · source · target · reader)
10. Review cadence and kill criterion
11. Open assumptions
```
