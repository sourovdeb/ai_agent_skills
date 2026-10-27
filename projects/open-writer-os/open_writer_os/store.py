#!/usr/bin/env python3
"""Filesystem project store for Open Writer OS.

Folder canon (from the MISHU Writer OS):

    <project>/
        provider.json          non-secret model configuration
        AUTHOR/                writer profile, style, preferences, AI rules
        PROJECTS/<BOOK>/       one folder per book inside a project
            PROJECT_CORE.md STORY_BIBLE.md CANON_LEDGER.md
            CURRENT_STATE.md STYLE_TARGET.md
            CHARACTERS/ OUTLINE/ SCENES/ MANUSCRIPT/ NOTES/
        ENGINES/               mode instructions (SHORT_FICTION, MEMOIR, ...)

All state is plain Markdown so writers can read, edit and back up their
work with any text editor. No database, no lock-in.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

AUTHOR_FILES = (
    "00_WRITER_PROFILE.md",
    "01_STYLE_CONSTITUTION.md",
    "02_CREATIVE_PREFERENCES.md",
    "03_AI_WORKING_RULES.md",
)
BOOK_DIRS = ("CHARACTERS", "OUTLINE", "SCENES", "MANUSCRIPT", "NOTES")
CORE_FILES = (
    "PROJECT_CORE.md",
    "STORY_BIBLE.md",
    "CANON_LEDGER.md",
    "CURRENT_STATE.md",
    "STYLE_TARGET.md",
)
FACT_STATUSES = ("CANON", "PROPOSED", "UNKNOWN", "CHARACTER_BELIEF",
                 "READER_KNOWLEDGE", "REJECTED", "RETCONNED")
MEMOIR_STATUSES = ("REMEMBERED", "DOCUMENTED", "CORROBORATED", "RECONSTRUCTED",
                   "INFERRED", "UNCERTAIN", "DISPUTED", "FICTIONALIZED")


class StoreError(RuntimeError):
    pass


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "untitled"


def project_root(path: str | Path) -> Path:
    root = Path(path).expanduser().resolve()
    if not (root / "AUTHOR").is_dir():
        raise StoreError(f"not an Open Writer OS project: {root} (missing AUTHOR/)")
    return root


def new_project(root: str | Path, name: str, backend: str = "ollama",
                base_url: str = "", model: str = "") -> Path:
    root = Path(root).expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        raise StoreError(f"project directory already exists and is not empty: {root}")
    (root / "AUTHOR").mkdir(parents=True, exist_ok=True)
    (root / "PROJECTS").mkdir(exist_ok=True)
    (root / "ENGINES").mkdir(exist_ok=True)
    for filename in AUTHOR_FILES:
        (root / "AUTHOR" / filename).write_text(_author_template(filename), encoding="utf-8")
    provider = {
        "backend": backend,
        "model": model or "llama3.2",
    }
    if backend == "ollama":
        provider["base_url"] = base_url or "http://127.0.0.1:11434"
    else:
        provider["base_url"] = base_url or "https://api.openai.com/v1"
        provider["api_key_env"] = "OPEN_WRITER_OS_API_KEY"
    (root / "provider.json").write_text(
        json.dumps(provider, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "README.md").write_text(_project_readme(name), encoding="utf-8")
    return root


def new_book(root: str | Path, title: str) -> Path:
    root = project_root(root)
    book = root / "PROJECTS" / slugify(title)
    if book.exists():
        raise StoreError(f"book already exists: {book.name}")
    for sub in BOOK_DIRS:
        (book / sub).mkdir(parents=True)
    for filename in CORE_FILES:
        (book / filename).write_text(_core_template(filename, title), encoding="utf-8")
    return book


def list_books(root: str | Path) -> list[str]:
    root = project_root(root)
    projects = root / "PROJECTS"
    if not projects.is_dir():
        return []
    return sorted(p.name for p in projects.iterdir() if p.is_dir())


def book_dir(root: str | Path, book: str) -> Path:
    root = project_root(root)
    path = root / "PROJECTS" / slugify(book)
    if not path.is_dir():
        raise StoreError(f"book not found: {book} (looked in {path})")
    return path


def read_file(path: str | Path) -> str:
    return Path(path).expanduser().read_text(encoding="utf-8")


def write_file(path: str | Path, text: str) -> None:
    Path(path).expanduser().write_text(text, encoding="utf-8")


def append_section(path: str | Path, heading: str, body: str) -> None:
    """Append a dated section to a Markdown ledger-style file."""
    path = Path(path).expanduser()
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    separator = "" if existing.endswith("\n\n") or not existing else "\n"
    path.write_text(existing + separator + f"\n## {heading}\n\n{body}\n", encoding="utf-8")


def load_provider(root: str | Path) -> dict:
    root = project_root(root)
    path = root / "provider.json"
    if not path.is_file():
        raise StoreError("provider.json not found; run `init` first")
    return json.loads(path.read_text(encoding="utf-8"))


def save_provider(root: str | Path, provider: dict) -> None:
    root = project_root(root)
    (root / "provider.json").write_text(
        json.dumps(provider, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _author_template(filename: str) -> str:
    titles = {
        "00_WRITER_PROFILE.md": "Writer Profile",
        "01_STYLE_CONSTITUTION.md": "Style Constitution",
        "02_CREATIVE_PREFERENCES.md": "Creative Preferences",
        "03_AI_WORKING_RULES.md": "AI Working Rules",
    }
    return f"# {titles[filename]}\n\n(To be filled in as the writer works.)\n"


def _core_template(filename: str, title: str) -> str:
    if filename == "PROJECT_CORE.md":
        return (f"# Project Core — {title}\n\n"
                "## Story in plain language\n\n## Central characters\n\n"
                "## Main conflict\n\n## Emotional promise\n\n"
                "## Known beginning\n\n## Known ending\n\n"
                "## Themes or concerns\n\n## Tone\n\n## Non-negotiables\n\n"
                "## Open design questions\n")
    if filename == "STORY_BIBLE.md":
        return _story_bible_template(title)
    if filename == "CURRENT_STATE.md":
        return _current_state_template()
    if filename == "CANON_LEDGER.md":
        return _canon_ledger_template()
    if filename == "STYLE_TARGET.md":
        return ("# Style Target\n\n## Narrative\n\n## Prose\n\n## Emotion\n\n"
                "## Dialogue\n\n## Description\n\n## Avoid\n")
    return f"# {filename.replace('.md', '').replace('_', ' ')}\n\n"


def _story_bible_template(title: str) -> str:
    return (f"# Story Bible — {title}\n\n"
            "Keep this factual. Do not mix in speculative brainstorming.\n\n"
            "## Characters\n\n## Relationships\n\n## Important history\n\n"
            "## Locations\n\n## Organizations\n\n## World rules\n\n"
            "## Important objects\n\n## Secrets\n")


def _current_state_template() -> str:
    return ("# Current Story State\n\n"
            "What is happening right now: recent scenes, unresolved threads,\n"
            "character emotional states, knowledge states, location, time.\n")


def _canon_ledger_template() -> str:
    return ("# Canon Ledger\n\n"
            "Important facts that must not drift. Label each with a fact status:\n\n"
            + " ".join(f"`{s}`" for s in FACT_STATUSES) + "\n")


def _project_readme(name: str) -> str:
    return f"""# {name}

An Open Writer OS project. Everything is plain Markdown — read it, edit it,
back it up with any tool.

- `AUTHOR/` — your writer profile, style constitution, preferences, AI rules
- `PROJECTS/<BOOK>/` — one folder per book (bible, characters, outline, scenes, manuscript)
- `ENGINES/` — the mode instructions the assistant follows
- `provider.json` — which model backend to use (ollama locally, or any
  OpenAI-compatible API). API keys are read from environment variables only.

Free for non-profit use by writers, educators and communities.
"""
