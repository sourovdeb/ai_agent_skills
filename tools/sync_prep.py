#!/usr/bin/env python3
"""
Prepare content for multi-platform sync (no API calls yet).
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

CATEGORIES = {
    "mental_health": "Mental Health",
    "elt": "ELT Masterclass",
    "english_teaching": "English Teaching",
    "philosophy": "Philosophy",
    "photography": "Photography",
    "software": "Software",
    "dxo": "DXO",
    "ai": "Learn AI in Mistral Studio"
}

def slugify(title: str) -> str:
    """Convert title to URL slug."""
    return re.sub(r'[^\w\s-]', '', title).lower().replace(' ', '-')[:60]

def normalize_title(title: str) -> str:
    """Normalize title to title case."""
    title = re.sub(r'\s+', ' ', title).strip()
    return ' '.join(word.capitalize() for word in title.split())

def is_blog_like(file_path: Path) -> bool:
    """Check if file is blog-like."""
    blog_patterns = ['blog', 'essay', 'post', 'daily', 'briefing', 'lesson']
    parent_dirs = str(file_path.parent).lower()
    return any(pattern in parent_dirs for pattern in blog_patterns)

def infer_category(file_path: Path, content: str) -> str:
    """Infer category from path and content."""
    path_lower = str(file_path).lower()
    content_lower = content.lower()[:500]

    keywords = {
        "mental_health": ["trauma", "therapy", "mental", "wellness", "health", "healing"],
        "elt": ["elt", "english", "language", "lesson", "esl", "efl"],
        "english_teaching": ["teaching", "grammar", "vocabulary"],
        "philosophy": ["philosophy", "ethics", "thought"],
        "photography": ["photo", "image", "visual", "dxo"],
        "software": ["code", "programming", "python", "javascript", "api"],
        "dxo": ["dxo", "developer", "experience"],
        "ai": ["ai", "machine learning", "gpt", "claude", "mistral"]
    }

    for cat_key, keywords_list in keywords.items():
        if any(kw in path_lower or kw in content_lower for kw in keywords_list):
            return CATEGORIES.get(cat_key, "Software")

    return "Software"

def parse_file(file_path: Path) -> Dict[str, Any]:
    """Parse markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()[:2000]  # First 2000 chars for preview

        title = normalize_title(file_path.stem.replace('_', ' '))
        category = infer_category(file_path, content)
        blog_like = is_blog_like(file_path)

        return {
            "title": title,
            "category": category,
            "is_blog": blog_like,
            "slug": slugify(title),
            "file": str(file_path),
            "size": len(content),
        }
    except Exception as e:
        return None

def scan_content(repo_paths: List[str]) -> List[Dict[str, Any]]:
    """Scan all blog-like directories."""
    blog_dirs = [
        "blog_and_essays", "daily_essays", "posts", "guides",
        "AI_Lessons", "AI_Term_Lessons", "CELTA_Teaching_Materials",
        "presentations", "Presentations", "Growth_Hub", "initiatives",
        "weekly-briefings", "elt365_lessons", "routines", "python_toolkit"
    ]

    content = []
    for repo_path in repo_paths:
        for blog_dir in blog_dirs:
            dir_path = Path(repo_path) / blog_dir
            if dir_path.exists():
                for file in dir_path.rglob("*.md"):
                    if file.is_file():
                        post = parse_file(file)
                        if post:
                            content.append(post)

    return content

def main():
    repos = [
        "/home/user/my_professional_documents",
        "/home/user/free_education"
    ]

    print("📂 Scanning content...")
    content = scan_content(repos)
    print(f"✅ Found {len(content)} posts\n")

    # Group by category
    by_cat = {}
    for post in content:
        cat = post["category"]
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(post["title"])

    print("📊 By Category:")
    for cat, posts in sorted(by_cat.items()):
        print(f"  {cat}: {len(posts)} posts")
        for t in posts[:3]:
            print(f"    - {t}")
        if len(posts) > 3:
            print(f"    ... and {len(posts)-3} more")

    # Save manifest
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "total_posts": len(content),
        "by_category": {cat: len(posts) for cat, posts in by_cat.items()},
        "posts": content
    }

    with open("/home/user/sync_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n💾 Manifest saved to sync_manifest.json")

if __name__ == "__main__":
    main()
