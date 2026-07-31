// =============================================
// WordPress Batch Publisher from Google Sheets
// =============================================
// 
// Setup:
//   1. Open your Google Sheet
//   2. Extensions -> Apps Script
//   3. Paste this code, save
//   4. Run saveApiKey() once (paste your key there, run, then remove it)
//   5. Run publishFromSheet() to test
//   6. Set a trigger: clock icon -> Add Trigger -> publishFromSheet -> hourly
//
// Sheet structure (tab named 'Queue'):
//   A: Title  B: Content  C: Category  D: Tags
//   E: Status  F: ScheduleDate  G: SEO_Title  H: Meta_Description
//
// Credentials: stored in GAS PropertiesService (never hardcoded)

const WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';

function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) {
    Logger.log('Sheet named "Queue" not found. Create it first.');
    return;
  }
  const data = sheet.getDataRange().getValues();
  let published = 0;
  
  for (let i = 1; i < data.length; i++) {
    const row      = data[i];
    const title    = String(row[0] || '').trim();
    const content  = String(row[1] || '').trim();
    const category = String(row[2] || '').trim();
    const tags     = String(row[3] || '').trim();
    const status   = String(row[4] || '').trim().toLowerCase();
    const dateStr  = String(row[5] || '').trim();
    const seoTitle = String(row[6] || '').trim();
    const metaDesc = String(row[7] || '').trim();
    
    if (!title || status === 'published' || status === 'error') continue;
    if (status !== 'queued') continue;
    
    const resolvedCategory = category || guessCategory(title, content);
    const resolvedTags     = tags     || suggestTags(title, content);
    
    const post = {
      title:            title,
      content:          content,
      category:         resolvedCategory,
      tags:             resolvedTags,
      status:           dateStr ? 'future' : 'draft',
      seo_title:        (seoTitle || title).substring(0, 60),
      meta_description: (metaDesc || content.replace(/<[^>]+>/g, '').substring(0, 155))
    };
    if (dateStr) post.date = dateStr;
    
    const result = sendToWordPress(post);
    
    if (result && (result.post_id || result.id)) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());
      Logger.log('OK: ' + title + ' -> ID ' + (result.post_id || result.id));
      published++;
    } else {
      sheet.getRange(i + 1, 5).setValue('error');
      Logger.log('FAIL: ' + title);
    }
    
    Utilities.sleep(1500);
  }
  
  Logger.log('Done. Published ' + published + ' post(s).');
}

function sendToWordPress(postData) {
  const key = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  if (!key) {
    Logger.log('WP_KEY not set. Run saveApiKey() first.');
    return null;
  }
  const options = {
    method:             'POST',
    headers:            { 'X-Sourov-Key': key, 'Content-Type': 'application/json' },
    payload:            JSON.stringify(postData),
    muteHttpExceptions: true
  };
  try {
    const resp = UrlFetchApp.fetch(WP_API_URL, options);
    const code = resp.getResponseCode();
    if (code === 200 || code === 201) {
      return JSON.parse(resp.getContentText());
    }
    Logger.log('HTTP ' + code + ': ' + resp.getContentText());
    return null;
  } catch(e) {
    Logger.log('Error: ' + e.message);
    return null;
  }
}

function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (/grammar|tense|verb|noun|adjective|adverb/.test(text))    return 'Grammar';
  if (/listen|audio|phonetic|pronunciation|sound/.test(text))  return 'Listening & Phonology';
  if (/speak|fluency|conversation|oral|dialogue/.test(text))   return 'Speaking';
  if (/read|comprehension|text|passage/.test(text))            return 'Reading';
  if (/writ|essay|paragraph|composition/.test(text))           return 'Writing';
  if (/celta|lesson plan|teaching|trainer/.test(text))         return 'CELTA';
  if (/vocabular|word|idiom|phrasal/.test(text))               return 'Vocabulary';
  return 'ELT Masterclass';
}

function suggestTags(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  const keywords = [
    'grammar', 'listening', 'speaking', 'reading', 'writing',
    'vocabulary', 'pronunciation', 'CELTA', 'ELT', 'fluency',
    'comprehension', 'tense', 'idiom', 'phrasal verb', 'lesson plan'
  ];
  return keywords.filter(kw => text.includes(kw.toLowerCase())).slice(0, 5).join(',');
}

function saveApiKey() {
  const key = 'PASTE_YOUR_PLUGIN_KEY_HERE';  // Replace, run once, then delete
  PropertiesService.getScriptProperties().setProperty('WP_KEY', key);
  Logger.log('Key saved to Script Properties.');
}

function enrichWithDeepSeek(title, content) {
  const dsKey = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  if (!dsKey) return null;
  
  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + dsKey, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user',
        content: 'Given blog title: "' + title + '" return JSON only: {"tags":["t1","t2","t3"],"meta_description":"under 160 chars","category":"ELT Masterclass"}'
      }]
    }),
    muteHttpExceptions: true
  });
  try {
    const raw = JSON.parse(response.getContentText()).choices[0].message.content
      .replace(/```json/g,'').replace(/```/g,'').trim();
    return JSON.parse(raw);
  } catch(e) {
    return null;
  }
}
