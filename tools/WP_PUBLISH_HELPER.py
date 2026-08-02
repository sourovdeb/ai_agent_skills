#!/usr/bin/env python3

"""
WORDPRESS PUBLISHING HELPER

Generates WordPress-ready markdown for your posts.
Validates metadata, checks word count, and prepares for publishing.

Usage:
    python3 WP_PUBLISH_HELPER.py path/to/draft.md

Output:
    - Validates against template
    - Generates excerpt if missing
    - Prepares metadata for manual WordPress entry
    - Outputs checklist for publishing

IMPORTANT: This tool generates publishing instructions.
You will copy-paste the formatted content into WordPress yourself.
No direct FTP/database access here - keeping credentials safe!
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

def count_words(text):
    """Count words in text, excluding frontmatter."""
    return len(text.split())

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    if not content.startswith('---'):
        return {}, content

    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content

    fm_text = match.group(1)
    body = content[match.end():]

    metadata = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip()] = val.strip().strip('"\'')

    return metadata, body

def generate_excerpt(body, length=150):
    """Generate excerpt from body text."""
    # Remove markdown formatting
    text = re.sub(r'[#*_\[\]()]', '', body)
    text = re.sub(r'\n+', ' ', text)
    text = text.strip()

    if len(text) <= length:
        return text
    return text[:length] + '...'

def validate_metadata(metadata):
    """Check required fields."""
    required = ['title', 'category', 'status']
    missing = [f for f in required if f not in metadata or not metadata[f]]
    return missing

def generate_publishing_checklist(filename, metadata, word_count):
    """Generate WordPress publishing checklist."""
    checklist = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORDPRESS PUBLISHING CHECKLIST FOR: {metadata.get('title', 'UNTITLED')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SOURCE FILE: {filename}
GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METADATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title:        {metadata.get('title', '❌ MISSING')}
Author:       {metadata.get('author', 'Sourov Deb')}
Date:         {metadata.get('date', datetime.now().strftime('%Y-%m-%d'))}
Category:     {metadata.get('category', '❌ MISSING')}
Tags:         {metadata.get('tags', '[Set in WordPress]')}
Word Count:   {word_count} words {f'(⚠️ Target ~500, got {abs(500-word_count)} away)' if abs(500-word_count) > 50 else '✓'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PUBLISHING INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://www.sourovdeb.com/wp-admin/post-new.php

2. Fill in WordPress fields:
   ☐ Post Title: {metadata.get('title', '')}
   ☐ Content: [Copy-paste body text below]
   ☐ Category: {metadata.get('category', '')}
   ☐ Tags: {metadata.get('tags', '')}
   ☐ Excerpt: [See "EXCERPT" section below]
   ☐ Featured Image: {metadata.get('featured_image', '[Optional]')}

3. Before Publishing:
   ☐ Proofread: Read aloud for tone
   ☐ Links: Check all links work
   ☐ Formatting: H2 headings only (## not #)
   ☐ Images: Optimized and credited
   ☐ Meta: Author + Date set correctly

4. Publish:
   ☐ Set Status: "Published"
   ☐ Set Visibility: "Public"
   ☐ Click: "Publish"

5. After Publishing:
   ☐ Test link: https://www.sourovdeb.com/?p=[POST_ID]
   ☐ Check formatting in browser
   ☐ Share on social media (if desired)
   ☐ Update Google Sheet: https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXCERPT (for WordPress preview)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Use auto-generated below or write your own]

"""
    return checklist

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 WP_PUBLISH_HELPER.py <essay_file.md>")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    with open(filepath, 'r') as f:
        content = f.read()

    metadata, body = extract_frontmatter(content)
    word_count = count_words(body)
    excerpt = generate_excerpt(body)

    # Validate
    missing = validate_metadata(metadata)

    print(generate_publishing_checklist(filepath.name, metadata, word_count))
    print(excerpt)
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("ESSAY BODY (copy to WordPress)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print(body)

    if missing:
        print(f"\n⚠️  Missing metadata: {', '.join(missing)}")

    print("\n✓ Review checklist above before publishing!")

if __name__ == '__main__':
    main()
