#!/usr/bin/env python3
"""Offline test suite for Open Writer OS. No network access required.

Run from the project root:
    python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from open_writer_os import cli, engines, providers, store  # noqa: E402


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "proj"

    def tearDown(self):
        self.tmp.cleanup()

    def test_slugify(self):
        self.assertEqual(store.slugify("The Salt Road!"), "the-salt-road")
        self.assertEqual(store.slugify("  "), "untitled")
        self.assertEqual(store.slugify("Émile's Café"), "mile-s-caf")

    def test_new_project_creates_canon(self):
        store.new_project(self.root, "Test Project")
        for name in store.AUTHOR_FILES:
            self.assertTrue((self.root / "AUTHOR" / name).is_file(), name)
        self.assertTrue((self.root / "PROJECTS").is_dir())
        self.assertTrue((self.root / "ENGINES").is_dir())
        provider = json.loads((self.root / "provider.json").read_text())
        self.assertEqual(provider["backend"], "ollama")
        self.assertNotIn("api_key", json.dumps(provider).lower())

    def test_new_project_refuses_nonempty_dir(self):
        self.root.mkdir(parents=True)
        (self.root / "junk.txt").write_text("x")
        with self.assertRaises(store.StoreError):
            store.new_project(self.root, "Nope")

    def test_project_root_requires_author(self):
        with self.assertRaises(store.StoreError):
            store.project_root(self.root)

    def test_new_book_creates_core_files_and_dirs(self):
        store.new_project(self.root, "Test")
        book = store.new_book(self.root, "The Salt Road")
        self.assertEqual(book.name, "the-salt-road")
        for name in store.CORE_FILES:
            self.assertTrue((book / name).is_file(), name)
        for sub in store.BOOK_DIRS:
            self.assertTrue((book / sub).is_dir(), sub)
        self.assertIn("The Salt Road", (book / "PROJECT_CORE.md").read_text())
        self.assertIn("CANON", (book / "CANON_LEDGER.md").read_text())

    def test_new_book_rejects_duplicate(self):
        store.new_project(self.root, "Test")
        store.new_book(self.root, "Same Title")
        with self.assertRaises(store.StoreError):
            store.new_book(self.root, "Same Title")

    def test_list_and_book_dir(self):
        store.new_project(self.root, "Test")
        store.new_book(self.root, "Book A")
        store.new_book(self.root, "Book B")
        self.assertEqual(store.list_books(self.root), ["book-a", "book-b"])
        self.assertEqual(store.book_dir(self.root, "Book A").name, "book-a")
        with self.assertRaises(store.StoreError):
            store.book_dir(self.root, "missing")

    def test_append_section(self):
        store.new_project(self.root, "Test")
        ledger = self.root / "CANON_LEDGER.md"
        store.append_section(ledger, "Entry 1", "body one")
        store.append_section(ledger, "Entry 2", "body two")
        text = ledger.read_text()
        self.assertIn("## Entry 1", text)
        self.assertIn("## Entry 2", text)
        self.assertLess(text.index("Entry 1"), text.index("Entry 2"))

    def test_provider_round_trip(self):
        store.new_project(self.root, "Test", backend="openai",
                          base_url="https://example.com/v1", model="m")
        provider = store.load_provider(self.root)
        self.assertEqual(provider["backend"], "openai")
        self.assertEqual(provider["api_key_env"], "OPEN_WRITER_OS_API_KEY")
        provider["model"] = "m2"
        store.save_provider(self.root, provider)
        self.assertEqual(store.load_provider(self.root)["model"], "m2")


class EngineTests(unittest.TestCase):
    def test_all_twelve_modes_have_instructions(self):
        self.assertEqual(len(engines.MODES), 12)
        for mode in engines.MODES:
            self.assertIn(mode, engines.MODE_INSTRUCTIONS)

    def test_system_prompt_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            engines.system_prompt("NOPE")

    def test_system_prompt_memoir_adds_evidence_rules(self):
        base = engines.system_prompt("DRAFT")
        memoir = engines.system_prompt("DRAFT", memoir=True)
        self.assertGreater(len(memoir), len(base))
        for status in store.MEMOIR_STATUSES:
            self.assertIn(status, memoir)

    def test_system_prompt_contains_core_principles(self):
        prompt = engines.system_prompt("CONTINUITY")
        self.assertIn("SOURCE-OF-TRUTH", prompt)
        for status in store.FACT_STATUSES:
            self.assertIn(status, prompt)

    def test_truncate(self):
        short = "abc"
        self.assertEqual(engines.truncate(short), short)
        long = "x" * (engines.MAX_FILE_CHARS + 100)
        out = engines.truncate(long)
        self.assertLess(len(out), len(long))
        self.assertIn("truncated", out)

    def test_build_messages_structure(self):
        messages = engines.build_messages(
            "DRAFT", [("STORY_BIBLE.md", "bible text")], "write the scene")
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("bible text", messages[1]["content"])
        self.assertIn("write the scene", messages[1]["content"])
        self.assertIn("MODE: DRAFT", messages[0]["content"])

    def test_build_messages_respects_context_budget(self):
        big = "y" * (engines.MAX_CONTEXT_CHARS * 2)
        messages = engines.build_messages(
            "DRAFT", [("A", big), ("B", big), ("C", big)], "task")
        user = messages[1]["content"]
        # context portion must stay within budget (task text adds a little more)
        self.assertLessEqual(len(user), engines.MAX_CONTEXT_CHARS + 500)
        # the overflowing section is cut, not passed through whole
        self.assertLess(user.count("y"), 3 * engines.MAX_CONTEXT_CHARS)
        self.assertIn("context budget reached", user)

    def test_load_skill(self):
        root = Path(__file__).resolve().parent.parent
        text = engines.load_skill(root, "short-fiction")
        self.assertIn("Short Fiction", text)
        with self.assertRaises(FileNotFoundError):
            engines.load_skill(root, "does-not-exist")


class _FakeResponse:
    def __init__(self, payload: dict):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class ProviderTests(unittest.TestCase):
    def test_ollama_chat_success(self):
        captured = {}

        def fake_urlopen(request, timeout=0):
            captured["url"] = request.full_url
            captured["payload"] = json.loads(request.data.decode("utf-8"))
            return _FakeResponse({"message": {"content": "hello story"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            out = providers.chat(
                {"backend": "ollama", "base_url": "http://127.0.0.1:11434",
                 "model": "llama3.2"},
                [{"role": "user", "content": "hi"}], {})
        self.assertEqual(out, "hello story")
        self.assertEqual(captured["url"], "http://127.0.0.1:11434/api/chat")
        self.assertFalse(captured["payload"]["stream"])

    def test_ollama_http_error_wrapped(self):
        def fake_urlopen(request, timeout=0):
            raise urllib.error.HTTPError(
                request.full_url, 500, "boom", {}, io.BytesIO(b"server exploded"))

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(providers.ProviderError) as ctx:
                providers.chat({"backend": "ollama", "model": "m"},
                               [{"role": "user", "content": "hi"}], {})
        self.assertIn("HTTP 500", str(ctx.exception))

    def test_ollama_unreachable_wrapped(self):
        def fake_urlopen(request, timeout=0):
            raise urllib.error.URLError("connection refused")

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(providers.ProviderError) as ctx:
                providers.chat({"backend": "ollama", "model": "m"},
                               [{"role": "user", "content": "hi"}], {})
        self.assertIn("cannot reach provider", str(ctx.exception))

    def test_openai_requires_api_key(self):
        env = {k: v for k, v in os.environ.items()
               if k != "OPEN_WRITER_OS_API_KEY"}
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(providers.ProviderError) as ctx:
                providers.chat({"backend": "openai", "model": "m"},
                               [{"role": "user", "content": "hi"}], {})
        self.assertIn("OPEN_WRITER_OS_API_KEY", str(ctx.exception))

    def test_openai_chat_sends_bearer_and_parses(self):
        captured = {}

        def fake_urlopen(request, timeout=0):
            captured["auth"] = request.get_header("Authorization")
            captured["payload"] = json.loads(request.data.decode("utf-8"))
            return _FakeResponse(
                {"choices": [{"message": {"content": "api reply"}}]})

        with mock.patch.dict(os.environ, {"OPEN_WRITER_OS_API_KEY": "sk-test"}):
            with mock.patch("urllib.request.urlopen", fake_urlopen):
                out = providers.chat(
                    {"backend": "openai",
                     "base_url": "https://api.example.com/v1",
                     "model": "m", "api_key_env": "OPEN_WRITER_OS_API_KEY"},
                    [{"role": "user", "content": "hi"}],
                    {"temperature": 0.5, "max_tokens": 256})
        self.assertEqual(out, "api reply")
        self.assertEqual(captured["auth"], "Bearer sk-test")
        self.assertEqual(captured["payload"]["max_tokens"], 256)
        self.assertEqual(captured["payload"]["temperature"], 0.5)

    def test_unknown_backend_rejected(self):
        with self.assertRaises(providers.ProviderError):
            providers.chat({"backend": "carrier-pigeon", "model": "m"},
                           [{"role": "user", "content": "hi"}], {})

    def test_list_ollama_models(self):
        def fake_urlopen(url, timeout=0):
            return _FakeResponse({"models": [{"name": "mistral"}, {"name": "llama3.2"}]})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            self.assertEqual(providers.list_ollama_models(), ["llama3.2", "mistral"])


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "proj"
        store.new_project(self.root, "Test Project")
        store.new_book(self.root, "The Salt Road")

    def tearDown(self):
        self.tmp.cleanup()

    def _run_cli(self, argv, stdin_text=""):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(stdin_text)):
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_init_new_book_books(self):
        root2 = Path(self.tmp.name) / "second"
        code, out, _ = self._run_cli(["init", str(root2), "--name", "Second"])
        self.assertEqual(code, 0)
        self.assertIn("created project", out)
        code, out, _ = self._run_cli(["new-book", str(root2), "--title", "Book X"])
        self.assertEqual(code, 0)
        code, out, _ = self._run_cli(["books", str(root2)])
        self.assertEqual(code, 0)
        self.assertIn("book-x", out)

    def test_run_rejects_unknown_mode(self):
        code, _, err = self._run_cli(
            ["run", str(self.root), "NOPE", "--book", "The Salt Road",
             "--prompt", "hi"])
        self.assertEqual(code, 2)
        self.assertIn("unknown mode", err)

    def test_run_requires_prompt(self):
        code, _, err = self._run_cli(
            ["run", str(self.root), "draft", "--book", "The Salt Road"],
            stdin_text="")
        # stdin is a StringIO (not a tty), so empty input -> empty prompt
        self.assertEqual(code, 2)
        self.assertIn("no prompt", err)

    def test_run_offline_ollama_fails_cleanly(self):
        # No ollama server in the test environment: expect a clean error.
        code, _, err = self._run_cli(
            ["run", str(self.root), "continuity", "--book", "The Salt Road",
             "--prompt", "check the timeline"])
        self.assertEqual(code, 1)
        self.assertIn("cannot reach provider", err)

    def test_run_saves_draft_output(self):
        def fake_urlopen(request, timeout=0):
            return _FakeResponse({"message": {"content": "The drafted scene."}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            code, out, err = self._run_cli(
                ["run", str(self.root), "draft", "--book", "The Salt Road",
                 "--prompt", "draft the opening"])
        self.assertEqual(code, 0)
        self.assertIn("The drafted scene.", out)
        drafts = list((self.root / "PROJECTS" / "the-salt-road"
                       / "MANUSCRIPT").glob("*_draft.md"))
        self.assertEqual(len(drafts), 1)
        self.assertIn("saved to MANUSCRIPT", err)

    def test_run_no_save_writes_nothing(self):
        def fake_urlopen(request, timeout=0):
            return _FakeResponse({"message": {"content": "ephemeral"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            code, out, _ = self._run_cli(
                ["run", str(self.root), "draft", "--book", "The Salt Road",
                 "--prompt", "draft", "--no-save"])
        self.assertEqual(code, 0)
        self.assertEqual(list((self.root / "PROJECTS" / "the-salt-road"
                               / "MANUSCRIPT").glob("*.md")), [])

    def test_run_with_skill_pack(self):
        captured = {}

        def fake_urlopen(request, timeout=0):
            payload = json.loads(request.data.decode("utf-8"))
            captured["user"] = payload["messages"][1]["content"]
            return _FakeResponse({"message": {"content": "ok"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            code, _, _ = self._run_cli(
                ["run", str(self.root), "draft", "--book", "The Salt Road",
                 "--skill", "short-fiction", "--prompt", "draft"])
        self.assertEqual(code, 0)
        self.assertIn("Short Fiction Skill Pack", captured["user"])

    def test_run_memoir_flag_adds_evidence_rules(self):
        captured = {}

        def fake_urlopen(request, timeout=0):
            payload = json.loads(request.data.decode("utf-8"))
            captured["system"] = payload["messages"][0]["content"]
            return _FakeResponse({"message": {"content": "ok"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            code, _, _ = self._run_cli(
                ["run", str(self.root), "draft", "--book", "The Salt Road",
                 "--memoir", "--prompt", "draft"])
        self.assertEqual(code, 0)
        self.assertIn("REMEMBERED", captured["system"])
        self.assertIn("MEMOIR MODE", captured["system"])

    def test_canon_update_appends_to_ledger(self):
        def fake_urlopen(request, timeout=0):
            return _FakeResponse({"message": {"content": "- Mira is CANON. Evidence: ch.1"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            code, _, _ = self._run_cli(
                ["run", str(self.root), "canon-update", "--book", "The Salt Road",
                 "--prompt", "update canon"])
        self.assertEqual(code, 0)
        ledger = (self.root / "PROJECTS" / "the-salt-road"
                  / "CANON_LEDGER.md").read_text()
        self.assertIn("Canon update", ledger)
        self.assertIn("Mira is CANON", ledger)

    def test_export_writes_full_book(self):
        out_file = Path(self.tmp.name) / "export.md"
        code, _, _ = self._run_cli(
            ["export", str(self.root), "--book", "The Salt Road",
             "--out", str(out_file)])
        self.assertEqual(code, 0)
        text = out_file.read_text()
        self.assertIn("PROJECT_CORE.md", text)
        self.assertIn("STORY_BIBLE.md", text)
        self.assertIn("CANON_LEDGER.md", text)

    def test_set_model(self):
        code, out, _ = self._run_cli(
            ["set-model", str(self.root), "--model", "mistral"])
        self.assertEqual(code, 0)
        self.assertEqual(store.load_provider(self.root)["model"], "mistral")


if __name__ == "__main__":
    unittest.main()
