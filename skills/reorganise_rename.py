"""
Skill: Reorganise and Rename Documents Based on Contents

This skill analyses the contents of a document (or a directory of documents)
and renames/moves each file to a path that accurately reflects what is inside it.

Supported formats: .txt, .md, .rst, .html, .csv, .json, .yaml, .yml, .py, .js,
                   .ts, .java, .go, .rb, .php, .cpp, .c, .cs, .sh, .log

Usage
-----
    # Preview changes (dry-run, default)
    python skills/reorganise_rename.py path/to/file_or_directory

    # Apply changes
    python skills/reorganise_rename.py path/to/file_or_directory --apply

    # Limit title extraction to the first N characters of content
    python skills/reorganise_rename.py path/to/file_or_directory --max-chars 2000

    # Organise files into topic sub-folders as well as renaming them
    python skills/reorganise_rename.py path/to/directory --organise --apply
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS: set[str] = {
    ".txt", ".md", ".rst", ".html", ".htm",
    ".csv", ".json", ".yaml", ".yml",
    ".py", ".js", ".ts", ".java", ".go", ".rb", ".php",
    ".cpp", ".c", ".cs", ".sh", ".log",
}

# Maximum characters read from a file when extracting a title
DEFAULT_MAX_CHARS: int = 4000

# Words that should not appear at the start of a filename (stop words for titles)
STOP_WORDS: set[str] = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "this", "that", "these", "those", "it", "its",
}

# Broad topic keywords → sub-folder name
TOPIC_MAP: list[tuple[set[str], str]] = [
    ({"meeting", "agenda", "minutes", "attendees", "action items"}, "meetings"),
    ({"invoice", "receipt", "payment", "billing", "purchase", "order"}, "finance"),
    ({"report", "summary", "analysis", "findings", "conclusion"}, "reports"),
    ({"readme", "documentation", "guide", "tutorial", "how to", "howto"}, "docs"),
    ({"test", "tests", "spec", "specs", "unit test", "integration"}, "tests"),
    ({"config", "configuration", "settings", "env", "environment"}, "config"),
    ({"todo", "task", "tasks", "backlog", "sprint"}, "tasks"),
    ({"note", "notes", "journal", "diary", "log"}, "notes"),
    ({"script", "automation", "pipeline", "workflow"}, "scripts"),
    ({"data", "dataset", "csv", "table", "spreadsheet"}, "data"),
]

# Sub-folder used when no topic keyword matches (only when --organise is active)
MISC_FOLDER: str = "misc"


# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------

def read_content(path: Path, max_chars: int) -> str:
    """Return the first *max_chars* characters of *path*, decoded leniently."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError as exc:
        print(f"  [warn] cannot read {path}: {exc}", file=sys.stderr)
        return ""


def extract_title_from_markdown(content: str) -> Optional[str]:
    """Return the text of the first ATX or setext heading, if any."""
    for line in content.splitlines():
        # ATX heading: # Title or ## Title …
        m = re.match(r"^#{1,6}\s+(.+)", line)
        if m:
            return m.group(1).strip()
        # Setext heading: underlined with === or ---
    lines = content.splitlines()
    for i, line in enumerate(lines[:-1]):
        if re.match(r"^[=\-]{2,}\s*$", lines[i + 1]) and line.strip():
            return line.strip()
    return None


def extract_title_from_html(content: str) -> Optional[str]:
    """Return the text of the first <title> or <h1> tag."""
    for pattern in (r"<title[^>]*>(.*?)</title>", r"<h1[^>]*>(.*?)</h1>"):
        m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if m:
            raw = re.sub(r"<[^>]+>", "", m.group(1))
            return raw.strip() or None
    return None


def extract_title_from_json(content: str) -> Optional[str]:
    """Return a title from common JSON keys: title, name, subject, description."""
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    for key in ("title", "name", "subject", "description", "label"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def extract_title_from_code(content: str, extension: str) -> Optional[str]:
    """
    For source-code files, return the first docstring / module-level comment
    or the name of the first public class / function.
    """
    # Python: module docstring
    if extension == ".py":
        m = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if m:
            first_line = m.group(1).strip().splitlines()[0]
            if first_line:
                return first_line
        m = re.search(r"'''(.*?)'''", content, re.DOTALL)
        if m:
            first_line = m.group(1).strip().splitlines()[0]
            if first_line:
                return first_line
        # First class or function
        m = re.search(r"^class\s+(\w+)|^def\s+(\w+)", content, re.MULTILINE)
        if m:
            return (m.group(1) or m.group(2)).replace("_", " ").title()

    # Shell / config: first non-blank comment line
    if extension in {".sh", ".yml", ".yaml"}:
        for line in content.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#") and len(stripped) > 2:
                return stripped[1:].strip()

    # Generic: first non-empty line of comments ( // … or /* … */ )
    m = re.search(r"//\s*(.+)", content)
    if m:
        return m.group(1).strip()

    return None


def first_meaningful_sentence(content: str) -> str:
    """
    Fall-back: return a cleaned snippet of the first non-blank line of *content*
    (up to 80 characters).
    """
    for line in content.splitlines():
        line = line.strip()
        if line:
            # strip leading punctuation / markdown artefacts
            line = re.sub(r"^[#>\-\*\+\|`\s]+", "", line).strip()
            return line[:80]
    return ""


def derive_title(path: Path, content: str) -> str:
    """
    Return the best human-readable title for *content*, trying format-specific
    strategies before falling back to the first meaningful line.
    """
    ext = path.suffix.lower()
    title: Optional[str] = None

    if ext in {".md", ".rst"}:
        title = extract_title_from_markdown(content)
    elif ext in {".html", ".htm"}:
        title = extract_title_from_html(content)
    elif ext in {".json"}:
        title = extract_title_from_json(content)
    elif ext in {".py", ".sh", ".yml", ".yaml", ".js", ".ts", ".java",
                 ".go", ".rb", ".php", ".cpp", ".c", ".cs"}:
        title = extract_title_from_code(content, ext)

    if not title:
        title = first_meaningful_sentence(content)

    return title or path.stem


# ---------------------------------------------------------------------------
# Filename sanitisation
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    """Convert *title* to a safe, lowercase, underscore-separated filename slug."""
    # Lowercase
    slug = title.lower()
    # Remove characters that are not alphanumeric, spaces, or hyphens/underscores
    slug = re.sub(r"[^\w\s\-]", "", slug)
    # Collapse whitespace and replace with underscores
    slug = re.sub(r"[\s\-]+", "_", slug).strip("_")
    # Drop leading stop words
    parts = slug.split("_")
    while parts and parts[0] in STOP_WORDS:
        parts = parts[1:]
    slug = "_".join(parts)
    # Truncate to a reasonable length
    return slug[:60].strip("_") or "untitled"


def unique_path(target: Path) -> Path:
    """If *target* already exists (and differs from source), append a counter."""
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


# ---------------------------------------------------------------------------
# Topic classification
# ---------------------------------------------------------------------------

def classify_topic(content: str) -> Optional[str]:
    """
    Return the name of the best-matching topic folder for *content*,
    or *None* if no topic matches.
    """
    lower = content.lower()
    best_folder: Optional[str] = None
    best_count = 0
    for keywords, folder in TOPIC_MAP:
        count = sum(1 for kw in keywords if kw in lower)
        if count > best_count:
            best_count = count
            best_folder = folder
    return best_folder if best_count > 0 else None


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def plan_rename(
    path: Path,
    max_chars: int = DEFAULT_MAX_CHARS,
    organise: bool = False,
) -> Tuple[Path, Path]:
    """
    Return *(source, destination)* for a single file.

    The destination is computed from the file's content.  If *organise* is
    True, a topic sub-folder is also inserted.
    """
    content = read_content(path, max_chars)
    title = derive_title(path, content)
    slug = slugify(title)
    new_name = slug + path.suffix.lower()

    if organise and content:
        topic = classify_topic(content)
        destination = path.parent / (topic or MISC_FOLDER) / new_name
    else:
        destination = path.parent / new_name

    # Only resolve collisions when the destination differs from the source.
    if destination.resolve() != path.resolve():
        destination = unique_path(destination)
    return path, destination


def process_path(
    root: Path,
    max_chars: int = DEFAULT_MAX_CHARS,
    organise: bool = False,
    apply: bool = False,
) -> List[Tuple[Path, Path]]:
    """
    Collect all rename operations for *root* (file or directory).

    Returns a list of *(source, destination)* pairs.
    If *apply* is True the renames/moves are executed.
    """
    targets: list[Path] = []

    if root.is_file():
        if root.suffix.lower() in SUPPORTED_EXTENSIONS:
            targets.append(root)
        else:
            print(f"[skip] unsupported extension: {root}", file=sys.stderr)
    elif root.is_dir():
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                targets.append(p)
    else:
        print(f"[error] path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    operations: list[tuple[Path, Path]] = []
    for target in targets:
        source, destination = plan_rename(target, max_chars, organise)
        operations.append((source, destination))

    # Print plan
    print(f"\n{'ACTION':6}  {'SOURCE':<45}  DESTINATION")
    print("-" * 100)
    for source, destination in operations:
        if source.resolve() == destination.resolve():
            action = "KEEP"
        else:
            action = "MOVE" if apply else "WOULD"
        print(f"{action:<6}  {str(source):<45}  {destination}")

    if apply:
        for source, destination in operations:
            if source.resolve() == destination.resolve():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
        applied = sum(
            1 for s, d in operations if s.resolve() != d.resolve()
        )
        print(f"\n✓ Applied {applied} rename(s).")
    else:
        would_change = sum(
            1 for s, d in operations if s.resolve() != d.resolve()
        )
        print(
            f"\nDry-run complete. {would_change} file(s) would be renamed. "
            "Pass --apply to execute."
        )

    return operations


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "path",
        type=Path,
        help="File or directory to process.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Actually rename/move files (default: dry-run only).",
    )
    parser.add_argument(
        "--organise",
        action="store_true",
        default=False,
        help="Also move files into topic sub-folders.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        metavar="N",
        help=f"Characters read from each file for analysis (default: {DEFAULT_MAX_CHARS}).",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    process_path(
        root=args.path,
        max_chars=args.max_chars,
        organise=args.organise,
        apply=args.apply,
    )


if __name__ == "__main__":
    main()
