# Hourly continuation policy

Policy version: 2.1.0
Campaign: skill-library-2026-09-26
Authorization: user's continuation request, 26 September 2026.

## What changes

Keep the existing hourly schedule. Target one completed, usable skill candidate per run, working on at most one logical skill. Quality, evidence, and source preservation remain required. A checkpoint or a delivery retry is not a completed skill.

Save each complete candidate to at least ONE authorized destination: GitHub, private Google Drive, or a Gmail draft. All three remain preferred, not mandatory. A verified candidate on a dedicated GitHub branch counts as saved; merging to main is not required. A Drive document must contain the actual package or provide working links to every required companion. A Gmail-only save must contain the complete readable package in its body or permitted attachments; a status-only message does not count.

Once the complete candidate and resumable checkpoint are verified in one destination, move to the next eligible skill on the next run. Record missing mirrors without allowing synchronization to monopolize future runs. Attempt optional mirroring after substantive work, within a bounded delivery budget. Do not rebuild or reread an already completed candidate merely because a mirror failed.

## Failure and recovery

Remove the three-failed-runs automatic pause. Keep the schedule enabled through destination failures. Bound each run's troubleshooting: one targeted diagnostic and one materially different authorized fallback. Respect permissions, rate limits, and explicit denials. Continued scheduling does not authorize bypassing controls.

Use a working destination for progress when another is unavailable. Prefer GitHub's fresh-SHA reservation; otherwise use revision-controlled private Drive state when supported. Do not treat a Gmail draft as an atomic lock. Without atomic state, use immutable run-specific checkpoints, a fresh read before saving, and reconcile records before selecting work. If overlap cannot be resolved, do not overwrite or duplicate an active candidate; report that run's limit and keep the schedule enabled.

When no destination can accept writes, preserve the actual artifact and checkpoint in the task response or a confirmed local download. Mark remote delivery failed. Resume that unsaved artifact when recoverable; never claim a remote upload or durable file that does not exist. Do not accumulate an unlimited unsaved backlog. A blocked source or target-model test need not stop work on other eligible skills, but must not be represented as a passed test or completed original capability.

## Preserved requirements

Preserve originals, package identity, specialist methods, and meaningful examples. Use the actual Master Skill Standard: A1-A4, Q01-Q60, X01-X10. Audit IDs must match their real questions; a grouped claim of coverage is not an audit result. Keep review, tests, approval, deployment, and delivery separate.

Assume a nontechnical user and no installed software. Provide a usable prompt, setup guide, one recommended route, bounded alternatives, and actual test evidence. Prefer adequate existing tools and lightweight solutions. Never invent providers, accounts, credentials, model capabilities, measurements, or completed actions.

For creative work and storytelling, integrate explanatory images or diagrams beside the passages they illuminate. Preserve supplied words and order unless rewriting was requested. Distinguish fiction, recollection, evidence, and visual reconstruction. A prompt is not a rendered image.

Gmail remains draft-only. No sending, live workflow execution, website deployment, purchasing, deletion, or permission changes are authorized by this policy. Public GitHub files must exclude private source references and delivery receipts.

## Finite completion

Keep the existing membership cutoff: 2026-09-26T08:27:08Z. Do not extend the queue with endless new skills. Stop only after the reconciled library's candidate work has a documented disposition and each completed package plus the final index is verified in at least one destination, or the user asks to stop. Report blocked, alternative-only, and untested items separately; do not call them fully validated upgrades. Missing optional mirrors alone must not keep the campaign running or prevent closeout. Unresolved essential sources or work mean the library is not complete.

This policy replaces conflicting all-three delivery gates, GitHub-only state dependency, mandatory main-branch synchronization, mirror-first selection, and automatic pausing after three failed runs. Other quality and permission rules remain unchanged.
