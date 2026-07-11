# SKILL_regulatory_filing_tracker

**Trigger phrases:** regulatory filing tracker, track Ofqual EHRC Défenseur des droits CNIL deadlines, CELTA complaint evidence chain, multi-authority submission status, authority letters progress, regulatory appeal tracker

## Purpose

Maintains a living, auditable tracker for regulatory complaints, filings, and correspondence across multiple jurisdictions and authorities (UK: Ofqual, EHRC; France: Défenseur des droits, CNIL, and related). Logs deadlines, evidence submitted, responses, and next actions. Built specifically for complex, long-running cases such as disability discrimination in professional training/qualification recognition (e.g. CELTA appeals and related filings).

## When to Activate

- Managing or preparing submissions to one or more regulators
- Approaching deadline for any authority response or filing
- Need to audit full evidence chain or prepare follow-up letters
- Cross-referencing responses across UK/France authorities
- Updating job application or legal strategy documents with current regulatory status

## Core Structure (Embed in Every Relevant Response)

Master status table example:

| Authority | Deadline / Next Due | Current Status | Key Evidence Filed (IDs/Links) | Last Response Received | Next Action | Blocker? |
|-----------|---------------------|----------------|--------------------------------|------------------------|-------------|----------|
| Ofqual    | [date]              | [status]       | [Drive/GitHub refs]            | [summary + date]       | [action]    | YES/NO   |
| Défenseur des droits | [date]     | [status]       | ...                            | ...                    | ...         | ...      |
| CNIL      | ...                 | ...            | ...                            | ...                    | ...         | ...      |

## Key Features

- Evidence ID system: Link to specific Drive files, GitHub commits, or email threads
- Deadline monitoring with escalation flags
- Neutral, factual, rights-based language templates for all correspondence
- Integration with authority-letters skill for drafting submissions
- Change log: Record every update with date and actor

## Integration Points

- Works directly with authority-letters, legal-reasoning-agent, and email campaign validator (for sending filings or follow-ups)
- Update this tracker file or a dedicated case tracker.md after every significant action
- Feeds status into job application materials and motivation letters
- Cross-references with CELTA-specific memory (prohibited wording, appeal strategy)

## Prevention of Common Failures

- Never miss a deadline: Always surface the next due date and blocker status in tables
- Maintain full chain of custody for evidence (who filed what, when, proof)
- Use only approved neutral phrasing in all external communications
- Re-verify status with official portals before claiming "filed" or "responded"

## Recommended Activation Protocol

1. Pull latest from this skill + memory
2. Update table with verified facts only
3. Flag any approaching deadlines in red / high priority
4. Generate next action list with explicit blocker column
5. Commit updated tracker to GitHub for persistence across sessions