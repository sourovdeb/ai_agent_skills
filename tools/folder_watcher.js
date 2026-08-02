/**
 * folder_watcher.js
 * 
 * Watches a folder for new Markdown files and publishes them to WordPress.
 * 
 * Install:  npm install chokidar node-fetch
 * Run:      node scripts/folder_watcher.js
 * 
 * Drop .md files into ~/wordpress_queue/ and they become WordPress drafts.
 * Credentials via environment variables: WP_API_URL, WP_PLUGIN_KEY
 */

const path     = require('path');
const fs       = require('fs');
const os       = require('os');
const chokidar = require('chokidar');

const WATCH_DIR   = path.join(os.homedir(), 'wordpress_queue');
const ARCHIVE_DIR = path.join(WATCH_DIR, 'archive');
const WP_URL      = process.env.WP_API_URL || 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_KEY      = process.env.WP_PLUGIN_KEY || '';

[WATCH_DIR, ARCHIVE_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

const CATEGORY_RULES = [
  [/grammar|tense|verb|noun|adjective/i,      'Grammar'],
  [/listen|audio|phonetic|pronunciation/i,    'Listening & Phonology'],
  [/speak|fluency|conversation|oral/i,        'Speaking'],
  [/read|comprehension|passage/i,             'Reading'],
  [/writ|essay|paragraph|composition/i,       'Writing'],
  [/celta|lesson plan|teaching|trainer/i,     'CELTA'],
  [/vocabular|idiom|phrasal|collocation/i,    'Vocabulary'],
];

const TAG_KEYWORDS = [
  'grammar','listening','speaking','reading','writing','vocabulary',
  'pronunciation','CELTA','ELT','fluency','comprehension','tense',
  'idiom','phrasal verb','lesson plan'
];

function guessCategory(text) {
  for (const [regex, cat] of CATEGORY_RULES) {
    if (regex.test(text)) return cat;
  }
  return 'ELT Masterclass';
}

function suggestTags(text) {
  const t = text.toLowerCase();
  return TAG_KEYWORDS.filter(kw => t.includes(kw.toLowerCase())).slice(0, 5).join(',');
}

function mdToHtml(markdown) {
  return markdown
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[\[(.+?)\]\]/g, '$1')
    .replace(/^(?!<[hli]).+$/gm, line => line.trim() ? `<p>${line}</p>` : '')
    .trim();
}

async function processFile(filePath) {
  const filename = path.basename(filePath);
  console.log(`Processing: ${filename}`);

  await new Promise(r => setTimeout(r, 500));

  const raw = fs.readFileSync(filePath, 'utf8');
  const lines = raw.trim().split('\n');

  let title = '';
  let bodyStart = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('#')) {
      title = lines[i].replace(/^#+\s*/, '').trim();
      bodyStart = i + 1;
      break;
    }
  }
  if (!title) {
    title = filename.replace('.md', '').replace(/-/g, ' ');
    bodyStart = 0;
  }

  const bodyMd   = lines.slice(bodyStart).join('\n');
  const bodyHtml = mdToHtml(bodyMd);
  const combined = title + ' ' + bodyMd;
  const category = guessCategory(combined);
  const tags     = suggestTags(combined);
  const metaDesc = bodyMd.replace(/[#*\[\]]/g, '').substring(0, 155).trim() + '...';

  const payload = {
    title,
    content:          bodyHtml,
    status:           'draft',
    category,
    tags,
    meta_description: metaDesc,
    seo_title:        title.substring(0, 60)
  };

  if (!WP_KEY) {
    console.error('WP_PLUGIN_KEY environment variable not set.');
    return;
  }

  try {
    const { default: fetch } = await import('node-fetch');
    const resp = await fetch(WP_URL, {
      method:  'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    if (resp.ok) {
      const data = await resp.json();
      const id = data.post_id || data.id;
      console.log(`Published: "${title}" -> Draft ID: ${id}`);
      fs.renameSync(filePath, path.join(ARCHIVE_DIR, filename));
    } else {
      const err = await resp.text();
      console.error(`Failed (${resp.status}): ${err.substring(0, 200)}`);
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
  }
}

console.log(`Watching: ${WATCH_DIR}`);
console.log('Drop .md files into that folder to auto-publish to WordPress.');
console.log('Press Ctrl+C to stop.\n');

const watcher = chokidar.watch(path.join(WATCH_DIR, '*.md'), {
  persistent: true,
  ignoreInitial: false,
  awaitWriteFinish: { stabilityThreshold: 1000, pollInterval: 200 }
});

watcher.on('add', filePath => processFile(filePath));
watcher.on('error', err => console.error(`Watcher error: ${err}`));
