#!/usr/bin/env python3
"""
Dev.to Publisher — AI & Programming Content
Scans repos for AI/programming content and posts as drafts to Dev.to.
Rate: 5 posts per run (designed to run hourly via cron).

Usage:
    python3 devto_publisher.py              # normal run
    python3 devto_publisher.py --dry-run    # preview without posting
    python3 devto_publisher.py --state      # show published log
"""

import os
import re
import sys
import json
import time
import hashlib
import requests
import argparse
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────

API_KEY = os.environ.get("DEVTO_API_KEY") or os.environ.get("DEV_TO_API_KEY") or ""
DEVTO_API = "https://dev.to/api"
BATCH_SIZE = 5          # posts per run
RATE_SLEEP = 3          # seconds between posts (be polite to the API)

REPOS = [
    Path("/home/user/my_professional_documents"),
    Path("/home/user/free_education"),
]

# Directories to scan (relative to repo root)
INCLUDE_DIRS = [
    "AI_Lessons", "AI_Term_Lessons", "Presentations/AI_Term_Lessons",
    "guides", "weekly-briefings", "Growth_Hub", "initiatives",
    "content/ai_lessons", "routines/02_python_toolkit_routine",
    "wordpress_integration",          # tech incident write-ups
    "WordPress_Incidents",            # troubleshooting docs
]

# Additional single-file sources to convert (troubleshooting → blog)
TROUBLESHOOT_FILES = [
    "WordPress_Incidents/2026-07-06_Critical_Error/WORDPRESS_CRITICAL_ERROR_REPORT_2026-07-06.md",
    "wordpress_integration/SEO_GUIDE.md",
    "wordpress_integration/SYNC_STATUS.md",
]

EXCLUDE_PATTERNS = [
    "_archive", "credentials", "legal", "biography", "therapy",
    "story_of", "medical", "Biography", "Legal", "therapy_and",
    "Story_of", "contact", "cv_and", "cover-letter", "job_leads",
    "Profile_Doc", "browser_extension", "templates", ".github",
]

# Keyword filter — only include if file content matches any
AI_PROG_KEYWORDS = re.compile(
    r"\b(python|javascript|api|automation|claude|gpt|llm|ai agent|machine learning|"
    r"artificial intelligence|wordpress|github|git|script|programming|code|developer|"
    r"deepseek|mistral|openai|chatgpt|prompt|software|function|class|def |import |"
    r"json|rest api|devto|dev\.to|tool use|agent|model|token|embedding|fine.tun)\b",
    re.IGNORECASE,
)

STATE_FILE = Path("/home/user/my_professional_documents/devto_integration/published_log.json")

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"published": {}}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()[:12]


def extract_title(content: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Try frontmatter
    m = re.search(r"^title:\s*(.+)", content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"\'')
    return fallback


def infer_tags(content: str, title: str) -> list[str]:
    combined = (title + " " + content[:3000]).lower()
    tag_map = {
        "python": "python",
        "javascript": "javascript",
        "ai agent": "ai",
        "automation": "automation",
        "wordpress": "wordpress",
        "github": "github",
        "llm": "machinelearning",
        "claude": "claudeai",
        "gpt": "openai",
        "deepseek": "deepseek",
        "api": "api",
        "programming": "programming",
        "developer": "webdev",
        "json": "json",
        "tutorial": "tutorial",
        "beginner": "beginners",
        "tool": "tools",
        "productivity": "productivity",
    }
    tags = []
    for kw, tag in tag_map.items():
        if kw in combined and tag not in tags:
            tags.append(tag)
        if len(tags) >= 4:
            break
    if not tags:
        tags = ["ai", "programming"]
    return tags[:4]


def markdown_to_devto(content: str) -> str:
    """Light cleanup for Dev.to markdown rendering."""
    # Remove Jekyll/Hugo frontmatter
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)
    # Collapse excessive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)
    # Trim
    content = content.strip()
    return content


def build_troubleshoot_blog(path: Path) -> dict:
    """Convert a troubleshooting/incident doc into a Dev.to blog format."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    title = extract_title(raw, path.stem.replace("_", " ").title())
    # Prefix to make clear it's a real incident
    if "incident" in title.lower() or "critical" in title.lower() or "error" in title.lower():
        title = f"How I Fixed: {title}"
    body = markdown_to_devto(raw)
    # Add Dev.to header note
    header = (
        f"*This post is a real incident/troubleshooting log converted into a guide.*\n\n"
        f"---\n\n"
    )
    return {
        "title": title,
        "body": header + body,
        "tags": infer_tags(raw, title) + ["debugging"],
    }


def build_article_post(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    title = extract_title(raw, path.stem.replace("-", " ").replace("_", " ").title())
    body = markdown_to_devto(raw)
    return {
        "title": title,
        "body": body,
        "tags": infer_tags(raw, title),
    }


def post_to_devto(article: dict, dry_run: bool = False) -> dict | None:
    payload = {
        "article": {
            "title": article["title"],
            "body_markdown": article["body"],
            "published": False,  # always draft
            "tags": article["tags"],
        }
    }
    if dry_run:
        print(f"  [DRY RUN] Would post: {article['title']!r}")
        print(f"            Tags: {article['tags']}")
        return {"id": "dry-run", "url": "https://dev.to/draft"}

    resp = requests.post(
        f"{DEVTO_API}/articles",
        headers={"api-key": API_KEY, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if resp.status_code in (200, 201):
        data = resp.json()
        return {"id": data.get("id"), "url": data.get("url", "")}
    else:
        print(f"  ERROR {resp.status_code}: {resp.text[:300]}")
        return None


def collect_candidates(state: dict) -> list[dict]:
    """Scan repos and return unposted AI/programming files."""
    candidates = []
    published = state["published"]

    # 1. Scan directory trees
    for repo in REPOS:
        for inc_dir in INCLUDE_DIRS:
            scan_root = repo / inc_dir
            if not scan_root.exists():
                continue
            for md in scan_root.rglob("*.md"):
                # Skip excluded paths
                parts = str(md)
                if any(ex in parts for ex in EXCLUDE_PATTERNS):
                    continue
                fid = str(md)
                if fid in published:
                    continue
                try:
                    content = md.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                if len(content) < 200:
                    continue
                if not AI_PROG_KEYWORDS.search(content):
                    continue
                candidates.append({"path": md, "kind": "article"})

    # 2. Specific troubleshooting files
    for repo in REPOS:
        for rel in TROUBLESHOOT_FILES:
            fp = repo / rel
            if not fp.exists():
                continue
            fid = str(fp)
            if fid in published:
                continue
            candidates.append({"path": fp, "kind": "troubleshoot"})

    return candidates


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Dev.to publisher for AI/programming content")
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    parser.add_argument("--state", action="store_true", help="Show published log and exit")
    parser.add_argument("--batch", type=int, default=BATCH_SIZE, help="Posts this run (default 5)")
    args = parser.parse_args()

    if not API_KEY and not args.dry_run:
        print("ERROR: Set DEVTO_API_KEY or DEV_TO_API_KEY environment variable.")
        sys.exit(1)

    state = load_state()

    if args.state:
        pub = state["published"]
        print(f"Published posts: {len(pub)}")
        for fid, meta in list(pub.items())[-20:]:
            print(f"  {meta['posted_at'][:10]}  {meta['title'][:70]}")
        return

    candidates = collect_candidates(state)
    print(f"Found {len(candidates)} unposted candidate files.")

    if not candidates:
        print("Nothing new to post.")
        return

    posted = 0
    for cand in candidates:
        if posted >= args.batch:
            break

        path = cand["path"]
        kind = cand["kind"]
        fid = str(path)

        print(f"\n[{posted+1}/{args.batch}] {path.name}")

        try:
            if kind == "troubleshoot":
                article = build_troubleshoot_blog(path)
            else:
                article = build_article_post(path)
        except Exception as e:
            print(f"  SKIP (parse error): {e}")
            continue

        if len(article["title"]) < 5 or len(article["body"]) < 100:
            print(f"  SKIP (too short)")
            continue

        result = post_to_devto(article, dry_run=args.dry_run)
        if result:
            state["published"][fid] = {
                "title": article["title"],
                "tags": article["tags"],
                "devto_id": result.get("id"),
                "devto_url": result.get("url"),
                "posted_at": datetime.utcnow().isoformat(),
                "kind": kind,
            }
            save_state(state)
            posted += 1
            print(f"  ✓ Draft created: {result.get('url', 'N/A')}")
            if not args.dry_run:
                time.sleep(RATE_SLEEP)
        else:
            print(f"  ✗ Failed to post")

    print(f"\nDone. Posted {posted} drafts this run.")
    remaining = len(collect_candidates(state))
    print(f"Remaining in queue: {remaining}")


if __name__ == "__main__":
    main()
