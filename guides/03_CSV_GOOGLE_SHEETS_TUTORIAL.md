# Understanding CSV + Google Apps Script: A Complete Beginner Tutorial

## The Question You Asked: "I Never Understood How CSV + Google JavaScript Works"

This guide answers exactly that. No assumed knowledge. By the end you will:
- Know what CSV is and why it exists
- Know what Google Apps Script is
- Understand how they connect to WordPress
- Have a working system set up

---

## Part 1: What Is CSV?

### The Simple Explanation

CSV stands for **Comma-Separated Values**. It is just a text file where each row is a line, and each column is separated by a comma.

Imagine you have a table like this:

| Title | Category | Tags | Status |
|-------|----------|------|--------|
| Day 32 Listening | ELT | listening,skills | draft |
| Grammar Rules | Grammar | grammar,tense | future |

As a CSV file that exact table looks like this:
```
Title,Category,Tags,Status
Day 32 Listening,ELT,"listening,skills",draft
Grammar Rules,Grammar,"grammar,tense",future
```

That is all CSV is. A spreadsheet saved as plain text. Any spreadsheet software (Google Sheets, Excel, LibreOffice) can open and save CSV files.

### Why Does CSV Exist?

Because it is **universal**. Every programming language, every database, every tool in the world can read a comma-separated text file. It is the simplest possible way to share tabular data.

### CSV vs Google Sheets

Google Sheets is a visual interface for data. CSV is the raw data format underneath. When you export a Google Sheet, you get a CSV. When you import a CSV, Google Sheets shows it as a table.

---

## Part 2: What Is Google Apps Script?

### The Simple Explanation

Google Apps Script is **JavaScript that runs inside Google**. It lives inside your Google Sheet, Google Doc, or Gmail — and it can control those products like a robot.

Think of it this way:
- You can click a button in Google Sheets manually
- OR you can write a script that clicks it automatically
- OR you can set a timer so the script runs every hour without you doing anything

Google Apps Script does all three.

### Why JavaScript?

JavaScript is the language of the web. Google chose it because it is widely known and it naturally handles web requests (HTTP calls) — which is exactly what we need to talk to WordPress.

### Where Does It Live?

Inside your Google Sheet:
1. Open your Google Sheet
2. Click **Extensions** in the top menu
3. Click **Apps Script**
4. A code editor opens — this is where your script lives

---

## Part 3: How They Connect to WordPress

Here is the complete picture of what happens:

```
[Your Google Sheet]  
       |  
       | You fill in: Title, Content, Category, Tags, Status  
       |  
[Apps Script trigger fires every hour]  
       |  
       | Script reads each row of your sheet  
       | For rows where Status = "queued", it builds a JSON object  
       | It sends that JSON to your WordPress site via HTTP POST  
       |  
[Your WordPress Plugin receives it]  
       |  
       | Plugin creates the post as draft or scheduled  
       | Returns a post ID  
       |  
[Apps Script marks the row as "published"]  
```

**The key concept: HTTP POST**  
When your browser opens a webpage, it sends an HTTP GET request. When a form submits data, it sends an HTTP POST request. Apps Script can send POST requests to any URL — including your WordPress REST API.

---

## Part 4: Step-by-Step Setup

### Step 1: Create Your Google Sheet

1. Go to **sheets.google.com** and create a new sheet
2. Name the first tab: **Queue**
3. In row 1, type these headers in columns A through H:

```
A: Title
B: Content  
C: Category
D: Tags
E: Status
F: ScheduleDate
G: SEO_Title
H: Meta_Description
```

4. In row 2, add a test post:
```
A: Day 32 – Listening Skills
B: <p>Listening is the foundation of language acquisition...</p>
C: ELT Masterclass
D: listening, CELTA, ELT
E: queued
F: (leave blank for draft, or: 2026-06-20T09:00)
G: Day 32: Improve Listening Skills
H: Discover practical listening strategies for ELT students.
```

### Step 2: Open Apps Script

1. In your sheet, click **Extensions → Apps Script**
2. Delete the empty `function myFunction() {}` that appears
3. Paste the complete script below

### Step 3: The Complete Script

```javascript
// =============================================
// WordPress Publisher from Google Sheets
// =============================================

// --- CONFIGURATION (edit these two lines) ---
const WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_API_KEY = 'your-plugin-key-here';  // Set via Script Properties instead
// --- END CONFIGURATION ---

function publishFromSheet() {
  // Get the sheet named 'Queue'
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  
  // Get all data (every row and column that has content)
  const data = sheet.getDataRange().getValues();
  
  // Loop through each row, skipping row 1 (the header)
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    
    // Read each column by position
    const title    = row[0];  // Column A
    const content  = row[1];  // Column B
    const category = row[2];  // Column C
    const tags     = row[3];  // Column D
    const status   = row[4];  // Column E
    const dateStr  = row[5];  // Column F
    const seoTitle = row[6];  // Column G
    const metaDesc = row[7];  // Column H
    
    // Skip rows with no title or already published
    if (!title || status === 'published') continue;
    
    // Only process rows marked as 'queued'
    if (status !== 'queued') continue;
    
    // Build the post object
    const post = {
      title:            String(title),
      content:          String(content),
      category:         category  || 'Uncategorized',
      tags:             tags      || '',
      status:           dateStr   ? 'future' : 'draft',
      seo_title:        seoTitle  || String(title),
      meta_description: metaDesc  || ''
    };
    
    // Add schedule date if provided
    if (dateStr) {
      post.date = String(dateStr);
    }
    
    // Send to WordPress
    const result = sendToWordPress(post);
    
    // If successful, mark the row as published
    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');       // Column E = 'published'
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());  // Log time
      Logger.log('Published: ' + title + ' → ID ' + result.post_id);
    } else {
      sheet.getRange(i + 1, 5).setValue('error');  // Mark as error so you can see it
      Logger.log('Failed: ' + title);
    }
    
    // Wait 1.5 seconds between posts to avoid overloading WordPress
    Utilities.sleep(1500);
  }
}

function sendToWordPress(postData) {
  // Get the API key from Script Properties (safer than hardcoding)
  const key = PropertiesService.getScriptProperties().getProperty('WP_KEY') || WP_API_KEY;
  
  const options = {
    method:           'POST',
    headers:          { 'X-Sourov-Key': key, 'Content-Type': 'application/json' },
    payload:          JSON.stringify(postData),
    muteHttpExceptions: true  // Don't crash on HTTP errors, return the error instead
  };
  
  try {
    const response = UrlFetchApp.fetch(WP_API_URL, options);
    const code     = response.getResponseCode();
    const body     = response.getContentText();
    
    if (code === 200 || code === 201) {
      return JSON.parse(body);
    } else {
      Logger.log('HTTP ' + code + ': ' + body);
      return null;
    }
  } catch (e) {
    Logger.log('Error: ' + e.message);
    return null;
  }
}

// Run this ONCE to save your API key securely
function saveApiKey() {
  PropertiesService.getScriptProperties().setProperty('WP_KEY', 'your-actual-plugin-key');
  Logger.log('Key saved!');
}
```

### Step 4: Save Your API Key Securely

Instead of putting your key in the code:
1. In Apps Script, temporarily edit `saveApiKey()` to include your real key
2. Click **Run → saveApiKey** (once only)
3. Remove the key from the code again
4. The key is now stored in Script Properties — not visible in your code

### Step 5: Test It

1. In Apps Script, click the **Run** button (triangle) while `publishFromSheet` is selected in the dropdown
2. It will ask for permissions — click **Review permissions → Allow**
3. Check your WordPress admin — a new draft should appear
4. Back in Apps Script, click **Execution log** to see what happened

### Step 6: Set Up Automatic Triggers

This makes it run every hour automatically:
1. In Apps Script, click the **clock icon** (Triggers) on the left
2. Click **+ Add Trigger** (bottom right)
3. Set:
   - **Function:** `publishFromSheet`
   - **Event source:** Time-driven
   - **Type:** Hour timer
   - **Interval:** Every hour
4. Click **Save**

Now every hour, the script checks for new `queued` rows and publishes them.

---

## Part 5: Understanding the Code Line by Line

### What is `SpreadsheetApp.getActiveSpreadsheet()`?

Apps Script has built-in objects that represent Google products:
- `SpreadsheetApp` = Google Sheets
- `GmailApp` = Gmail  
- `DriveApp` = Google Drive
- `UrlFetchApp` = HTTP requests (fetching URLs)

`getActiveSpreadsheet()` gets the spreadsheet that the script is attached to.

### What is `.getDataRange().getValues()`?

- `.getDataRange()` selects all cells that have content
- `.getValues()` converts them into a JavaScript array of arrays

Result looks like:
```javascript
[
  ['Title', 'Content', 'Category', ...],  // row 1 (header)
  ['Day 32', '<p>...</p>', 'ELT', ...],   // row 2
  ['Grammar', '<p>...</p>', 'Grammar', ...] // row 3
]
```

### What is `UrlFetchApp.fetch()`?

This is the most important function. It sends an HTTP request to any URL — just like your browser does when you visit a website, but from inside Google's servers.

```javascript
UrlFetchApp.fetch(URL, options)
// URL = where to send the request
// options = method (GET/POST), headers (auth), payload (the data)
```

### What is JSON?

JSON (JavaScript Object Notation) is how data is sent between systems on the web.

```javascript
// A JavaScript object:
const post = { title: 'Day 32', content: '<p>...</p>' };

// As JSON string (what gets sent over the internet):
JSON.stringify(post) 
// → '{"title":"Day 32","content":"<p>...</p>"}'
```

Your WordPress plugin receives this JSON string and turns it back into a post.

---

## Part 6: Common Errors and Fixes

| Error message | What it means | Fix |
|--------------|---------------|-----|
| `Authorization required` | Script needs permission | Click Allow when prompted |
| `HTTP 401` from WordPress | Wrong API key | Check WP_KEY in Script Properties |
| `HTTP 404` | Wrong WordPress URL | Check `WP_API_URL` matches exactly |
| `Cannot read property of undefined` | Empty row in sheet | Add a check: `if (!title) continue;` |
| `Exceeded maximum execution time` | Too many rows at once | Process 10 rows max per run |
| Tags appear as `listening skills` instead of two tags | Tags format wrong | Use comma separation: `listening,skills` |

---

## Part 7: Adding AI Auto-Tagging

Add this function to auto-suggest tags based on content:

```javascript
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (text.includes('grammar') || text.includes('tense') || text.includes('verb'))  return 'Grammar';
  if (text.includes('listen') || text.includes('audio') || text.includes('phonetic')) return 'Listening & Phonology';
  if (text.includes('speak') || text.includes('pronunciation') || text.includes('fluency')) return 'Speaking';
  if (text.includes('celta') || text.includes('lesson plan') || text.includes('teaching')) return 'CELTA';
  if (text.includes('reading') || text.includes('comprehension')) return 'Reading';
  if (text.includes('writing') || text.includes('essay') || text.includes('paragraph')) return 'Writing';
  return 'ELT Masterclass';
}

function suggestTags(title, content) {
  const keywords = ['grammar', 'listening', 'speaking', 'reading', 'writing',
    'vocabulary', 'pronunciation', 'CELTA', 'ELT', 'fluency', 'comprehension',
    'tense', 'present', 'past', 'future', 'idiom', 'phrasal verb'];
  const text = (title + ' ' + content).toLowerCase();
  return keywords.filter(kw => text.includes(kw.toLowerCase())).slice(0, 5).join(',');
}
```

In `publishFromSheet`, replace the tags line with:
```javascript
const tags = row[3] || suggestTags(String(title), String(content));
const category = row[2] || guessCategory(String(title), String(content));
```

Now the system auto-fills tags and categories when you leave those columns blank.
