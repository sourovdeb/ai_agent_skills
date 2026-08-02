# SKILL: Google Apps Script for Job Search Automation
## Pure JavaScript Implementation (No Google Sheets)
**Version:** 1.0 | **Date:** 29 May 2026 | **Target:** Job seekers, career changers

---

## OVERVIEW

This skill teaches you to **automate repetitive job search tasks** using Google Apps Script (JavaScript runtime in Google Suite) **without relying on Google Sheets**. Instead, we use:
- **Google Drive** (file storage)
- **Gmail** (email sending)
- **Google Docs** (templates, tracking)
- **Apps Script Triggers** (scheduled runs)

**What you'll automate:**
- Send batches of customised CVs + cover letters
- Track application status (in a Google Doc or JSON structure)
- Schedule follow-up reminders
- Scrape job listings (optional)
- Auto-generate cover letters from templates

---

## ARCHITECTURE: NO SHEETS, PURE APPS SCRIPT

### Why avoid Google Sheets?
- Sheets can be slow for complex automation
- Not ideal for tracking sensitive data (CVs with personal info)
- Easier to accidentally expose data through sharing
- JavaScript in Apps Script is more flexible

### Alternative data storage:
- **Google Drive JSON files** (lightweight, scriptable)
- **Google Docs with structured content** (human-readable + programmatic)
- **Email archives** (Gmail API pulls your sent mail)
- **Script properties** (small settings, not ideal for large datasets)

---

## STRUCTURE 1: BATCH EMAIL SENDER (NO SHEETS)

### File Structure:
```
Google Drive
├── 📁 Job Applications
│   ├── 📄 CV_[Name]_2026.pdf
│   ├── 📄 CoverLetterTemplate.docx
│   └── 📄 JobApplications_Tracker.txt
├── 📁 Email Templates
│   ├── 📄 EmailTemplate_LanguageCentre.txt
│   ├── 📄 EmailTemplate_Corporate.txt
│   └── 📄 EmailTemplate_Government.txt
└── 📁 Contact Lists
    └── 📄 JobTargets_20260529.txt
```

### Code: Batch Email Sender

```javascript
/**
 * BATCH EMAIL SENDER — No Sheets, Pure Apps Script
 * Sends customized emails with CV/cover letter attachments
 * Tracks in Google Doc, not Sheets
 * VERSION: 1.0
 */

const CONFIG = {
  CV_FILE_ID: 'PASTE_YOUR_CV_FILE_ID',
  COVER_LETTER_FILE_ID: 'PASTE_YOUR_COVER_LETTER_FILE_ID',
  TRACKER_DOC_ID: 'PASTE_YOUR_TRACKER_DOC_ID',
  SENDER_NAME: 'Your Name',
  SENDER_EMAIL: 'your.email@gmail.com',
  BATCH_SIZE: 10,
  RATE_LIMIT_MS: 2000,
};

const ORGANISATIONS = [
  {
    name: 'Organisation A',
    email: 'contact@orga.com',
    role: 'English Teacher',
    context: 'language centre',
    template: 'generic',
    applied: false,
    appliedDate: null,
  },
  // Add more organisations...
];

function loadAttachments() {
  try {
    const cvBlob = DriveApp.getFileById(CONFIG.CV_FILE_ID).getBlob();
    const clBlob = DriveApp.getFileById(CONFIG.COVER_LETTER_FILE_ID).getBlob();
    Logger.log('✅ Attachments loaded');
    return { cv: cvBlob, coverLetter: clBlob };
  } catch (err) {
    Logger.log('❌ Error loading attachments: ' + err.message);
    return null;
  }
}

function generateEmailBody(org, template) {
  const templates = {
    generic: `Dear Hiring Manager,

I am writing to express my interest in the {{ROLE}} position at {{ORG_NAME}}.

As an English educator with {{YEARS}} years of professional experience,
I am confident I can contribute effectively to {{ORG_CONTEXT}}.

Specialisms: IELTS/TOEIC, Business English, Conversation Coaching
Availability: Immediate | Funding: CPF/OPCO eligible

I would welcome the opportunity to discuss how my skills align with your needs.

Best regards,
[Your Name]`,

    corporate: `Dear {{ORG_NAME}} Team,

I am a qualified English trainer seeking to partner with {{ORG_CONTEXT}} to enhance team communications.

With {{YEARS}} years professional experience in international environments,
I design customised training programs that deliver measurable results.

Modules available:
  • Business English & negotiation skills
  • Cross-cultural communication
  • English for specific contexts (meetings, presentations, email)

I'd appreciate a brief meeting to explore potential collaboration.

Regards,
[Your Name]`,
  };

  let body = templates[template] || templates['generic'];
  body = body.replace('{{ORG_NAME}}', org.name);
  body = body.replace('{{ORG_CONTEXT}}', org.context);
  body = body.replace('{{ROLE}}', org.role);
  body = body.replace('{{YEARS}}', '18');
  return body;
}

function sendBatch(startIndex = 0, batchSize = 10, testMode = true) {
  Logger.log(`🚀 Starting batch: START=${startIndex}, SIZE=${batchSize}, TEST=${testMode}`);

  const attachments = loadAttachments();
  if (!attachments) return;

  const endIndex = Math.min(startIndex + batchSize, ORGANISATIONS.length);
  let successCount = 0, failureCount = 0;

  for (let i = startIndex; i < endIndex; i++) {
    const org = ORGANISATIONS[i];
    if (org.applied) { Logger.log(`⏭️  Skipped ${org.name} (already applied)`); continue; }

    const subject = `English Trainer — ${org.name}`;
    const body = generateEmailBody(org, org.template);
    const recipient = testMode ? CONFIG.SENDER_EMAIL : org.email;

    try {
      GmailApp.sendEmail(recipient, subject, body, {
        attachments: [attachments.cv, attachments.coverLetter],
        name: CONFIG.SENDER_NAME,
      });
      Logger.log(`✅ Sent ${i + 1}/${ORGANISATIONS.length} to ${org.name}`);
      org.applied = true;
      org.appliedDate = new Date().toISOString();
      successCount++;
    } catch (err) {
      Logger.log(`❌ Failed ${org.name}: ${err.message}`);
      failureCount++;
    }
    Utilities.sleep(CONFIG.RATE_LIMIT_MS);
  }

  logResults(startIndex, endIndex, successCount, failureCount);
  Logger.log(`🎉 Batch complete. Sent: ${successCount}, Failed: ${failureCount}`);
}

function logResults(startIndex, endIndex, successCount, failureCount) {
  try {
    const doc = DocumentApp.openById(CONFIG.TRACKER_DOC_ID);
    const body = doc.getBody();
    const timestamp = new Date().toLocaleString();
    body.appendParagraph(`[${timestamp}] Batch ${startIndex}–${endIndex}: ${successCount} sent, ${failureCount} failed`)
      .setHeading(HeadingType.HEADING3);
  } catch (err) {
    Logger.log('⚠️  Could not log to doc: ' + err.message);
  }
}

function testPreview() {
  const org = ORGANISATIONS[0];
  const body = generateEmailBody(org, org.template);
  Logger.log(`\n===== PREVIEW: ${org.name} =====`);
  Logger.log(`TO: ${org.email}`);
  Logger.log(body);
}

function dailyAutoBatch() {
  const unapplied = ORGANISATIONS.filter(org => !org.applied);
  if (unapplied.length === 0) { Logger.log('✅ All organisations contacted.'); return; }
  const startIndex = ORGANISATIONS.findIndex(org => !org.applied);
  sendBatch(startIndex, 10, false);
}
```

---

## STRUCTURE 3: SCHEDULED TRIGGERS (Auto-Run)

1. Go to Apps Script > Triggers (⏰ icon)
2. Create new trigger:
   - Function: `dailyAutoBatch`
   - Event source: Time-driven
   - Type: Day timer
   - Time: 14:00

---

## BEST PRACTICES

**DO:**
✅ Test mode first — `sendBatch(..., true)` before real sends  
✅ Rate limiting — 2–3 seconds between emails  
✅ Track everything (timestamps, failures, responses)  

**DON'T:**
❌ Send >100 emails/day (Google will throttle)  
❌ Use identical subjects/bodies for all emails  
❌ Store sensitive data hardcoded in scripts  

---

## REUSABILITY

Use this skill for:
- Job applications (60+ parallel outreach)
- Freelance client prospecting
- Research invitations
- Networking campaigns
- Meeting scheduling automation
