#!/usr/bin/env python3
"""
Direct WordPress Publisher with SEO Optimization
Pushes essays directly to sourovdeb.com using deploy.php gateway
Handles categories, tags, SEO metadata, featured images

Usage:
    python3 wp_publisher.py --file essay.md --category writing --tags essay,career --publish
"""

import json
import requests
import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

class WordPressPublisher:
    def __init__(self):
        self.gateway_url = "https://www.sourovdeb.com/deploy.php"
        self.secret_key = os.getenv("WP_DEPLOY_KEY", "")
        self.site_url = "https://www.sourovdeb.com"

    def parse_essay_file(self, filepath):
        """Parse markdown file with SEO frontmatter"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter (YAML-style at top)
        if content.startswith('---'):
            parts = content.split('---', 2)
            frontmatter = parts[1]
            body = parts[2].strip()

            meta = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    meta[key.strip()] = val.strip()
            return meta, body

        return {}, content

    def generate_seo_description(self, content, max_length=160):
        """Auto-generate SEO description from first paragraph"""
        sentences = content.split('.')[:3]
        desc = '.'.join(sentences).strip()
        if len(desc) > max_length:
            desc = desc[:max_length-3] + '...'
        return desc

    def create_wp_post(self, title, content, meta, tags=None, category=None, publish=False):
        """Create WordPress post via deploy.php API"""

        seo_description = meta.get('description', self.generate_seo_description(content))
        seo_keywords = meta.get('keywords', ', '.join(tags) if tags else '')

        post_data = {
            "action": "create_post",
            "key": self.secret_key,
            "post": {
                "post_title": title,
                "post_content": content,
                "post_excerpt": seo_description,
                "post_status": "publish" if publish else "draft",
                "post_type": "post",
                "post_date": meta.get('date', datetime.now().isoformat()),
            },
            "meta": {
                "_yoast_wpseo_metadesc": seo_description,
                "_yoast_wpseo_focuskw": meta.get('focus_keyword', title.split()[0]),
                "_yoast_wpseo_linkdex": "30",
                "sourov_author_health_note": meta.get('health_note', ''),
                "sourov_word_count": len(content.split()),
                "sourov_published_from": "claude_automation"
            },
            "tags": tags or [],
            "category": category or "Writing"
        }

        try:
            response = requests.post(
                self.gateway_url,
                json=post_data,
                timeout=30
            )
            result = response.json()

            if result.get('success'):
                return {
                    'status': 'success',
                    'post_id': result.get('post_id'),
                    'post_url': f"{self.site_url}/?p={result.get('post_id')}",
                    'edit_url': f"{self.site_url}/wp-admin/post.php?post={result.get('post_id')}&action=edit"
                }
            else:
                return {'status': 'error', 'message': result.get('error')}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def schedule_post(self, post_id, publish_date):
        """Schedule post for later publishing"""
        data = {
            "action": "schedule_post",
            "key": self.secret_key,
            "post_id": post_id,
            "publish_date": publish_date
        }
        response = requests.post(self.gateway_url, json=data, timeout=30)
        return response.json()

    def add_seo_tags(self, post_id, tags):
        """Add tags for better SEO"""
        data = {
            "action": "add_tags",
            "key": self.secret_key,
            "post_id": post_id,
            "tags": tags
        }
        response = requests.post(self.gateway_url, json=data, timeout=30)
        return response.json()

def main():
    parser = argparse.ArgumentParser(
        description='Publish essays to WordPress with SEO optimization'
    )
    parser.add_argument('--file', required=True, help='Essay markdown file')
    parser.add_argument('--title', help='Post title (auto-detected from file if not provided)')
    parser.add_argument('--category', default='Writing', help='WordPress category')
    parser.add_argument('--tags', help='Comma-separated tags (no spaces)')
    parser.add_argument('--publish', action='store_true', help='Publish immediately (default: draft)')
    parser.add_argument('--schedule', help='Schedule for date (YYYY-MM-DD HH:MM)')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    publisher = WordPressPublisher()
    meta, content = publisher.parse_essay_file(args.file)

    title = args.title or meta.get('title', Path(args.file).stem.replace('_', ' ').title())
    tags = args.tags.split(',') if args.tags else meta.get('tags', '').split(',')

    print(f"\n📝 Publishing to WordPress")
    print(f"   Title: {title}")
    print(f"   Category: {args.category}")
    print(f"   Tags: {', '.join(tags)}")
    print(f"   Status: {'PUBLISHED' if args.publish else 'DRAFT'}")
    print(f"   Words: {len(content.split())}")

    result = publisher.create_wp_post(
        title=title,
        content=content,
        meta=meta,
        tags=tags,
        category=args.category,
        publish=args.publish
    )

    if result['status'] == 'success':
        print(f"\n✅ Success!")
        print(f"   Post ID: {result['post_id']}")
        print(f"   View: {result['post_url']}")
        print(f"   Edit: {result['edit_url']}")

        if args.schedule:
            schedule_result = publisher.schedule_post(result['post_id'], args.schedule)
            if schedule_result.get('success'):
                print(f"   Scheduled: {args.schedule}")
    else:
        print(f"\n❌ Error: {result['message']}")
        sys.exit(1)

if __name__ == '__main__':
    main()
