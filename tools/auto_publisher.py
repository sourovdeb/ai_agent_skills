#!/usr/bin/env python3
"""
auto_publisher.py

Runs every 15 minutes (via cron). Watches a folder for new Markdown files
and publishes them to WordPress as drafts.

Setup:
    pip install requests
    
    Add to crontab (crontab -e):
    */15 * * * * /usr/bin/python3 /path/to/scripts/auto_publisher.py

Folder structure:
    ~/wordpress_queue/          <-- drop .md files here
    ~/wordpress_queue/archive/  <-- processed files moved here

Environment variables (set in ~/.bashrc or .env):
    WP_PLUGIN_KEY   your WordPress plugin secret key
    WP_API_URL      your WordPress API endpoint (optional, has default)
"""

import os
import time
import json
import logging
from pathlib import Path

try:
    import requests
except ImportError:
    print('Install requests: pip install requests')
    exit(1)

# ── Configuration ────────────────────────────────────────────────────────────────────
WATCH_DIR   = Path.home() / 'wordpress_queue'
ARCHIVE_DIR = WATCH_DIR / 'archive'
WP_URL      = os.environ.get('WP_API_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY      = os.environ.get('WP_PLUGIN_KEY', '')
LOG_FILE    = WATCH_DIR / 'publisher.log'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M'
)

CATEGORY_RULES = [
    (['grammar', 'tense', 'verb', 'noun', 'adjective', 'adverb'], 'Grammar'),
    (['listen', 'audio', 'phonetic', 'pronunciation', 'sound'], 'Listening & Phonology'),
    (['speak', 'fluency', 'conversation', 'oral', 'dialogue'], 'Speaking'),
    (['read', 'comprehension', 'text', 'passage'], 'Reading'),
    (['writ', 'essay', 'paragraph', 'composition', 'draft'], 'Writing'),
    (['celta', 'lesson plan', 'teaching', 'teacher', 'trainer'], 'CELTA'),
    (['vocabular', 'word', 'idiom', 'phrasal', 'collocation'], 'Vocabulary'),
]

KEYWORD_TAGS = [
    'grammar', 'listening', 'speaking', 'reading', 'writing',
    'vocabulary', 'pronunciation', 'CELTA', 'ELT', 'fluency',
    'comprehension', 'tense', 'idiom', 'phrasal verb', 'lesson plan',
    'English', 'language learning', 'teaching'
]


def guess_category(text):
    t = text.lower()
    for keywords, category in CATEGORY_RULES:
        if any(kw in t for kw in keywords):
            return category
    return 'ELT Masterclass'


def suggest_tags(text):
    t = text.lower()
    return [kw for kw in KEYWORD_TAGS if kw.lower() in t][:5]


def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.strip().split('\n')

    title = ''
    body_start = 0
    for i, line in enumerate(lines):
        stripped = line.lstrip('#').strip()
        if line.startswith('#') and stripped:
            title = stripped
            body_start = i + 1
            break

    if not title and lines:
        title = lines[0].strip()
        body_start = 1

    body = '\n'.join(lines[body_start:]).strip()

    html_lines = []
    for line in body.split('\n'):
        if line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('- '):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.strip():
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append('')
    html_body = '\n'.join(html_lines)

    meta = {}
    for line in lines:
        if '::' in line:
            key, _, val = line.partition('::')
            meta[key.strip().lower()] = val.strip()

    return title, html_body, meta


def process_file(filepath):
    logging.info(f'Processing: {filepath.name}')

    title, body, meta = parse_markdown(filepath)
    if not title:
        logging.warning(f'Skipping {filepath.name}: no title found')
        return

    combined = title + ' ' + body[:500]
    category = meta.get('category') or guess_category(combined)
    tags     = meta.get('tags') or ','.join(suggest_tags(combined))
    meta_desc = body[:157].replace('<p>', '').replace('</p>', '') + '...'

    payload = {
        'title':            title,
        'content':          body,
        'status':           'draft',
        'category':         category,
        'tags':             tags,
        'meta_description': meta_desc,
        'seo_title':        title[:60]
    }

    if not WP_KEY:
        logging.error('WP_PLUGIN_KEY not set. Export it as an environment variable.')
        return

    try:
        resp = requests.post(
            WP_URL,
            json=payload,
            headers={'X-Sourov-Key': WP_KEY},
            timeout=30
        )
        if resp.status_code in (200, 201):
            result = resp.json()
            post_id = result.get('post_id', result.get('id', '?'))
            logging.info(f'Published draft: "{title}" -> ID {post_id}')
            print(f'Published: {title} (ID: {post_id})')
            archive_path = ARCHIVE_DIR / filepath.name
            filepath.rename(archive_path)
        else:
            logging.error(f'Failed ({resp.status_code}): {resp.text[:200]}')
            print(f'Failed: {title} - HTTP {resp.status_code}')
    except requests.RequestException as e:
        logging.error(f'Request error: {e}')
        print(f'Error: {e}')


def main():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    WATCH_DIR.mkdir(parents=True, exist_ok=True)

    md_files = list(WATCH_DIR.glob('*.md'))

    if not md_files:
        print('No .md files found in queue folder.')
        return

    print(f'Found {len(md_files)} file(s) to process...')
    for f in md_files:
        process_file(f)
        time.sleep(1.5)

    print('Done.')


if __name__ == '__main__':
    main()
