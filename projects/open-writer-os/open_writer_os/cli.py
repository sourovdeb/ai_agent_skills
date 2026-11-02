#!/usr/bin/env python3
"""Command-line interface for Open Writer OS.

Usage:
    python -m open_writer_os init <path> [--name NAME] [--backend ollama|openai]
                                    [--base-url URL] [--model MODEL]
    python -m open_writer_os new-book <project> --title TITLE
    python -m open_writer_os books <project>
    python -m open_writer_os models <project>
    python -m open_writer_os set-model <project> --model MODEL [--backend B] [--base-url U]
    python -m open_writer_os run <project> <MODE> --book BOOK
                                    [--prompt TEXT | --input FILE | stdin]
                                    [--skill NAME] [--memoir]
    python -m open_writer_os export <project> --book BOOK [--out FILE]

MODE is one of: DISCOVER ARCHITECT SCENE_PLAN DRAFT DIALOGUE DESCRIBE DEEPEN
COMPRESS CONTINUITY REVISE CANON_UPDATE PROFILE_UPDATE (case-insensitive).

The writer's prompt is read from --prompt, --input FILE, or stdin.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

from . import engines, providers, store

# Where each mode's output is filed inside the book folder.
_MODE_OUTPUT_DIR = {
    "DRAFT": "MANUSCRIPT",
    "DIALOGUE": "MANUSCRIPT",
    "DESCRIBE": "MANUSCRIPT",
    "DEEPEN": "MANUSCRIPT",
    "REVISE": "MANUSCRIPT",
    "SCENE_PLAN": "SCENES",
    "CANON_UPDATE": None,        # appended to CANON_LEDGER.md
    "PROFILE_UPDATE": None,      # appended to AUTHOR/03_AI_WORKING_RULES.md
    "CONTINUITY": "NOTES",
    "DISCOVER": "NOTES",
    "ARCHITECT": "OUTLINE",
    "COMPRESS": "NOTES",
}


def _die(message: str, code: int = 2) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def _read_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None:
        return args.prompt
    if args.input is not None:
        return Path(args.input).expanduser().read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _gather_context(book: Path, skill_text: str | None) -> list[tuple[str, str]]:
    """Collect the bounded context set for a mode, in source-of-truth order."""
    sections: list[tuple[str, str]] = []
    for name in ("CURRENT_STATE.md", "STORY_BIBLE.md", "PROJECT_CORE.md",
                 "STYLE_TARGET.md", "CANON_LEDGER.md"):
        path = book / name
        if path.is_file():
            sections.append((name, store.read_file(path)))
    manuscript = book / "MANUSCRIPT"
    if manuscript.is_dir():
        drafts = sorted(manuscript.glob("*.md"))
        if drafts:
            sections.append(("LATEST_DRAFT", store.read_file(drafts[-1])))
    if skill_text:
        sections.append(("SKILL_PACK", skill_text))
    return sections


def _save_output(book: Path, root: Path, mode: str, text: str) -> str:
    """File the mode output; return a short description of where it went."""
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = _MODE_OUTPUT_DIR.get(mode)
    if mode == "CANON_UPDATE":
        store.append_section(book / "CANON_LEDGER.md", f"Canon update {stamp}", text)
        return "appended to CANON_LEDGER.md"
    if mode == "PROFILE_UPDATE":
        profile = root / "AUTHOR" / "00_WRITER_PROFILE.md"
        store.append_section(profile, f"Profile update {stamp}", text)
        return "appended to AUTHOR/00_WRITER_PROFILE.md"
    if target_dir:
        path = book / target_dir / f"{stamp}_{mode.lower()}.md"
        store.write_file(path, f"# {mode} output ({stamp})\n\n{text}\n")
        return f"saved to {target_dir}/{path.name}"
    return "printed only (planning mode; nothing written)"


def cmd_init(args: argparse.Namespace) -> int:
    try:
        root = store.new_project(args.path, args.name, backend=args.backend,
                                 base_url=args.base_url, model=args.model)
    except store.StoreError as exc:
        return _die(str(exc))
    print(f"created project at {root}")
    print(f"  backend : {args.backend}")
    print(f"  model   : {args.model or 'llama3.2 (default)'}")
    if args.backend == "openai":
        print("  note    : set the API key via the environment variable "
              "OPEN_WRITER_OS_API_KEY before running a mode")
    print("next: python -m open_writer_os new-book "
          f"{root} --title \"My Book\"")
    return 0


def cmd_new_book(args: argparse.Namespace) -> int:
    try:
        book = store.new_book(args.project, args.title)
    except store.StoreError as exc:
        return _die(str(exc))
    print(f"created book at {book}")
    return 0


def cmd_books(args: argparse.Namespace) -> int:
    try:
        books = store.list_books(args.project)
    except store.StoreError as exc:
        return _die(str(exc))
    if not books:
        print("(no books yet)")
    for name in books:
        print(name)
    return 0


def cmd_models(args: argparse.Namespace) -> int:
    try:
        provider = store.load_provider(args.project)
    except (store.StoreError, ValueError) as exc:
        return _die(str(exc))
    if provider.get("backend") != "ollama":
        return _die("`models` only lists Ollama backends; "
                   "API backends manage their own model lists")
    try:
        names = providers.list_ollama_models(provider.get("base_url", ""))
    except providers.ProviderError as exc:
        return _die(str(exc))
    current = provider.get("model", "")
    for name in names:
        marker = " (current)" if name == current else ""
        print(name + marker)
    return 0


def cmd_set_model(args: argparse.Namespace) -> int:
    try:
        provider = store.load_provider(args.project)
        if args.model:
            provider["model"] = args.model
        if args.backend:
            provider["backend"] = args.backend
            if args.backend == "ollama":
                provider.pop("api_key_env", None)
                provider["base_url"] = args.base_url or providers.DEFAULT_OLLAMA_URL
            else:
                provider["api_key_env"] = "OPEN_WRITER_OS_API_KEY"
                provider["base_url"] = args.base_url or "https://api.openai.com/v1"
        elif args.base_url:
            provider["base_url"] = args.base_url
        store.save_provider(args.project, provider)
    except (store.StoreError, ValueError) as exc:
        return _die(str(exc))
    print(f"provider: backend={provider.get('backend')} "
          f"model={provider.get('model')} base_url={provider.get('base_url')}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    mode = args.mode.upper().replace("-", "_")
    if mode not in engines.MODES:
        return _die(f"unknown mode {args.mode!r}; expected one of "
                    f"{', '.join(engines.MODES)}")
    prompt = _read_prompt(args).strip()
    if not prompt:
        return _die("no prompt given; use --prompt, --input FILE, or pipe via stdin")
    try:
        root = store.project_root(args.project)
        book = store.book_dir(root, args.book)
        provider = store.load_provider(root)
        skill_text = None
        if args.skill:
            try:
                skill_path = Path(__file__).resolve().parent.parent / "skills"
                skill_text = store.read_file(skill_path / args.skill / "SKILL.md")
            except OSError as exc:
                return _die(f"skill pack not found: {exc}")
        sections = _gather_context(book, skill_text)
        messages = engines.build_messages(mode, sections, prompt, memoir=args.memoir)
        options = {"temperature": args.temperature}
        if args.max_tokens:
            options["max_tokens"] = args.max_tokens
        text = providers.chat(provider, messages, options)
    except (store.StoreError, providers.ProviderError, ValueError) as exc:
        return _die(str(exc), code=1)
    print(text)
    if not args.no_save:
        where = _save_output(book, root, mode, text)
        print(f"\n---\n[{mode}] {where}", file=sys.stderr)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Concatenate the book's core files and manuscript into one Markdown file."""
    try:
        root = store.project_root(args.project)
        book = store.book_dir(root, args.book)
    except store.StoreError as exc:
        return _die(str(exc))
    parts = [f"# {book.name}\n"]
    for name in store.CORE_FILES:
        path = book / name
        if path.is_file():
            parts.append(f"\n\n## {name}\n\n" + store.read_file(path))
    for sub in ("CHARACTERS", "OUTLINE", "SCENES", "MANUSCRIPT", "NOTES"):
        folder = book / sub
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            parts.append(f"\n\n## {sub}/{path.name}\n\n" + store.read_file(path))
    out = "\n".join(parts) + "\n"
    if args.out:
        store.write_file(args.out, out)
        print(f"exported to {args.out}")
    else:
        sys.stdout.write(out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="open_writer_os",
        description="Open Writer OS - free, open-source writing assistant "
                    "(Ollama offline or any OpenAI-compatible API).")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create a new project folder")
    p.add_argument("path")
    p.add_argument("--name", default="My Open Writer OS Project")
    p.add_argument("--backend", choices=["ollama", "openai"], default="ollama")
    p.add_argument("--base-url", default="")
    p.add_argument("--model", default="")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("new-book", help="create a new book inside a project")
    p.add_argument("project")
    p.add_argument("--title", required=True)
    p.set_defaults(func=cmd_new_book)

    p = sub.add_parser("books", help="list books in a project")
    p.add_argument("project")
    p.set_defaults(func=cmd_books)

    p = sub.add_parser("models", help="list models on the local Ollama server")
    p.add_argument("project")
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("set-model", help="change backend, base URL or model")
    p.add_argument("project")
    p.add_argument("--model", default="")
    p.add_argument("--backend", choices=["ollama", "openai"], default="")
    p.add_argument("--base-url", default="")
    p.set_defaults(func=cmd_set_model)

    p = sub.add_parser("run", help="run a writing mode against a book")
    p.add_argument("project")
    p.add_argument("mode", help="one of: " + ", ".join(engines.MODES))
    p.add_argument("--book", required=True)
    p.add_argument("--prompt", default=None, help="the writer's request text")
    p.add_argument("--input", default=None, help="read the request from a file")
    p.add_argument("--skill", default=None,
                   help="skill pack to load (short-fiction, biography)")
    p.add_argument("--memoir", action="store_true",
                   help="enable memoir/biography evidence rules")
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--max-tokens", type=int, default=0)
    p.add_argument("--no-save", action="store_true",
                   help="print output only; do not file it in the book folder")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("export", help="export a whole book as one Markdown file")
    p.add_argument("project")
    p.add_argument("--book", required=True)
    p.add_argument("--out", default=None, help="output file (default: stdout)")
    p.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
