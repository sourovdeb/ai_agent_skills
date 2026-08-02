# /gmail-bulk-draft — Gmail Bulk Draft Automation Skill
**Version:** 1.1 | **Target:** Job seekers, outreach campaigns

---

## OVERVIEW

This skill automates the creation of personalized Gmail drafts at scale from CSV company data + sector-specific email templates. It generates a Google Apps Script that creates drafts directly in Gmail via `GmailApp.createDraft()`.

**Result:** 30+ Gmail drafts created per run in ~3-4 minutes.

---

## WHEN TO USE THIS SKILL

Trigger when the user:
- Pastes CSV data with company/email/sector columns
- Asks to "create Gmail drafts", "bulk email", or "apps script for Gmail"
- Wants to personalize emails by sector/industry

---

## WORKFLOW

### Step 1 — READ DATA
CSV columns required: `index | company | email | priority | sector | city | subject`

### Step 2 — SECTOR → TEMPLATE MAPPING

| Sector keyword | Template |
|---|---|
| Agences intérim | P1 — staffing/recruitment angle (French) |
| Hôtellerie & Tourisme | P2 — luxury hospitality angle (French) |
| Transport aérien | P3 — aviation English (French) |
| Multinationales | P4 — corporate English (English) |
| Santé | P5 — healthcare English (French) |
| Télécoms/Médias/Finance | P6 — business English (mixed) |
| Default | Generic CELTA trainer body (French) |

### Step 3 — GENERATE EMAIL BODIES

Structure for each email:
```
Salutation → Context/Value Prop → Credentials → Specific Offer → CTA → CV mention → Signature
```

### Step 4 — GENERATE APPS SCRIPT

Location: `script.google.com` → New Project → Name: `email_job`

```javascript
function createGmailDrafts() {
  const emails = [
    { to: "email@company.fr", subject: "Subject...", body: "Body..." },
    // ... more entries
  ];
  
  emails.forEach(e => {
    GmailApp.createDraft(e.to, e.subject, e.body);
  });
}
```

### Step 5 — AUTHORIZE & RUN

1. Click **Run** → Authorization dialog appears
2. Click "Review permissions"
3. OAuth popup opens (USER must approve — native browser window)
4. Script runs → creates all drafts
5. Verify: Gmail Draft count increases by N

**⚠ Auth popup is a native browser popup — cannot be automated. User must click manually.**

### Step 6 — VERIFY

Navigate to Gmail `#drafts` and confirm count increase. Open 2-3 drafts to spot-check.

---

## RULES

**NEVER:**
- Send emails automatically (drafts only)
- Skip verification step
- Mix up recipient + body

**ALWAYS:**
- Use `createDraft()` not `sendEmail()`
- Include company name in subject + body
- Match language (French for French companies, English for multinationals)
- Verify draft count after run
- Batch 20-30 per run if script times out

---

## PHASE 2 — RESEARCH NEW COMPANIES

After Phase 1 (30 drafts), research new target employers:

**New sectors to target:**
- BTP/Construction
- Grande Distribution
- Agriculture
- Services Publics
- Assurances
- Éducation (lycées)
- Sport & Loisirs
- Immobilier
- IT & Numérique

**Search sources:**
- Google Maps (search sector + "La Réunion")
- Pages Jaunes Réunion (pagesjaunes.fr)
- Kompass.fr (industrial directory)
- INSEE Réunion (official statistics)

---

## AI BEHAVIOR WHEN SKILL IS TRIGGERED

1. Ask for CSV data + any custom template preferences
2. Parse sectors and map to templates
3. Generate personalized email bodies for each entry
4. Build the complete Apps Script with `createGmailDrafts()` function
5. Present script in a code block for copy-paste
6. Guide user through OAuth authorization
7. Ask user to run and verify draft count
8. Report: X drafts created, breakdown by sector/priority
9. Offer Phase 2 research for more employers
