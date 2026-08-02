#!/usr/bin/env python3
"""
Multi-platform publisher: WordPress, Ghost, Dev.to, Box, IndexNow
Resilient: continues if one platform fails.
Credentials from environment (set before running).
"""

import os
import sys
import json
import re
import base64
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
from urllib.parse import quote

# ==== ENVIRONMENT CONFIGURATION ====
WP_USER = os.getenv("WP_USER", "")
WP_PASS = os.getenv("WP_PASS", "")
WP_ENDPOINT = "https://www.sourovdeb.com/wp-json/wp/v2/posts"

DEVTO_KEY = os.getenv("DEVTO_KEY", "")
DEVTO_ENDPOINT = "https://dev.to/api/articles"

BOX_TOKEN = os.getenv("BOX_TOKEN", "")

INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "")
INDEXNOW_URLS = f"https://www.sourovdeb.com/{INDEXNOW_KEY}.txt"

SITE_URL = "https://www.sourovdeb.com"
BATCH_SIZE = 10  # Process in batches

class SyncLogger:
    """Log sync operations."""

    def __init__(self):
        self.logs = []
        self.timestamp = datetime.now().isoformat()

    def log(self, level: str, platform: str, post_title: str, message: str):
        """Log an operation."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "platform": platform,
            "post": post_title,
            "message": message
        }
        self.logs.append(entry)
        print(f"  [{level:3}] {platform:12} | {post_title[:30]:30} | {message}")

    def save(self, filepath: str):
        """Save log to file."""
        with open(filepath, 'w') as f:
            json.dump({"timestamp": self.timestamp, "logs": self.logs}, f, indent=2)

class Publisher:
    """Publish to all platforms."""

    def __init__(self, manifest_path: str):
        with open(manifest_path) as f:
            self.manifest = json.load(f)

        self.logger = SyncLogger()
        self.results = {"wordpress": 0, "devto": 0, "box": 0, "indexnow": 0, "failed": []}

    def publish_all(self):
        """Publish all content in batches."""
        posts = self.manifest["posts"]
        total = len(posts)

        print(f"\n🚀 Publishing {total} posts across platforms...\n")

        for i, post in enumerate(posts[:BATCH_SIZE], 1):
            print(f"\n[{i}/{min(BATCH_SIZE, total)}] {post['title']}")
            self._publish_post(post)

        self.logger.save("/home/user/sync_results.json")
        self._print_summary()

    def _publish_post(self, post: Dict[str, Any]):
        """Publish to all platforms, continue on failure."""
        title = post["title"]
        platforms = [
            ("WordPress", self._wp_publish),
            ("Dev.to", self._devto_publish),
            ("Box", self._box_backup),
            ("IndexNow", self._indexnow_index),
        ]

        for platform_name, publish_func in platforms:
            try:
                result = publish_func(post)
                self.logger.log("OK", platform_name, title, result)
                self.results[platform_name.lower().replace(".", "")] += 1
            except Exception as e:
                self.logger.log("ERR", platform_name, title, str(e)[:60])
                self.results["failed"].append((platform_name, title))

    def _wp_publish(self, post: Dict[str, Any]) -> str:
        """Publish to WordPress."""
        auth = (WP_USER, WP_PASS)

        # Check for existing
        resp = requests.get(
            f"{WP_ENDPOINT}?search={quote(post['title'][:50])}",
            auth=auth,
            timeout=5,
            verify=False
        )

        payload = {
            "title": post["title"],
            "content": f"<p>Category: {post['category']}</p>",
            "status": "draft",
        }

        if resp.status_code == 200 and resp.json():
            post_id = resp.json()[0]["id"]
            requests.post(f"{WP_ENDPOINT}/{post_id}", json=payload, auth=auth, timeout=5, verify=False)
            return f"Updated #{post_id}"
        else:
            r = requests.post(WP_ENDPOINT, json=payload, auth=auth, timeout=5, verify=False)
            post_id = r.json().get("id", "?")
            return f"Created #{post_id}"

    def _devto_publish(self, post: Dict[str, Any]) -> str:
        """Publish to Dev.to."""
        headers = {"api-key": DEVTO_KEY}

        payload = {
            "article": {
                "title": post["title"],
                "body_markdown": f"## {post['title']}\n\nCategory: {post['category']}",
                "published": False,
                "canonical_url": f"{SITE_URL}/blog/{post['slug']}",
            }
        }

        resp = requests.post(DEVTO_ENDPOINT, json=payload, headers=headers, timeout=5)
        post_id = resp.json().get("id", "?")
        return f"Created #{post_id}"

    def _box_backup(self, post: Dict[str, Any]) -> str:
        """Backup to Box."""
        headers = {"Authorization": f"Bearer {BOX_TOKEN}"}

        filename = f"{post['slug']}.json"
        content = json.dumps(post, indent=2)

        files = {
            "attributes": (None, json.dumps({"name": filename, "parent": {"id": "0"}})),
            "file": (filename, content)
        }

        requests.post(
            "https://upload.box.com/api/2.0/files/content",
            headers=headers,
            files=files,
            timeout=5
        )

        return f"Backed up {filename}"

    def _indexnow_index(self, post: Dict[str, Any]) -> str:
        """Index to Bing/Yandex."""
        url = f"{SITE_URL}/blog/{post['slug']}"

        payload = {
            "urlList": [url],
            "key": INDEXNOW_KEY,
            "keyLocation": INDEXNOW_URLS
        }

        requests.post("https://www.bing.com/indexnow", json=payload, timeout=5)
        return f"Indexed"

    def _print_summary(self):
        """Print summary."""
        print("\n" + "="*70)
        print("📊 SYNC COMPLETE")
        print("="*70)
        print(f"✅ WordPress: {self.results['wordpress']} posts")
        print(f"✅ Dev.to: {self.results['devto']} posts")
        print(f"✅ Box: {self.results['box']} backups")
        print(f"✅ IndexNow: {self.results['indexnow']} indexed")
        if self.results["failed"]:
            print(f"\n❌ Failed: {len(self.results['failed'])}")
            for plat, title in self.results["failed"][:5]:
                print(f"   {plat}: {title}")
        print("="*70)
        print(f"📝 Logs saved to: sync_results.json")

def main():
    manifest_path = "/home/user/sync_manifest.json"

    if not Path(manifest_path).exists():
        print("❌ sync_manifest.json not found. Run sync_prep.py first.")
        sys.exit(1)

    publisher = Publisher(manifest_path)
    publisher.publish_all()

if __name__ == "__main__":
    main()
