"""Tests for skills/reorganise_rename.py"""

import json
import sys
from pathlib import Path

import pytest

# Ensure the repo root is on the path so we can import the skill directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.reorganise_rename import (
    classify_topic,
    derive_title,
    extract_title_from_html,
    extract_title_from_json,
    extract_title_from_markdown,
    plan_rename,
    process_path,
    slugify,
    unique_path,
)


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------

class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello_world"

    def test_removes_stop_words_at_start(self):
        assert slugify("The Quick Brown Fox") == "quick_brown_fox"

    def test_strips_special_chars(self):
        assert slugify("Meeting: Notes & Actions!") == "meeting_notes_actions"

    def test_truncates_long_title(self):
        long = "word " * 20
        result = slugify(long)
        assert len(result) <= 60

    def test_empty_string_returns_untitled(self):
        assert slugify("") == "untitled"

    def test_all_stop_words_returns_untitled(self):
        # All tokens removed → falls back to "untitled"
        assert slugify("the and a") == "untitled"

    def test_preserves_numbers(self):
        assert slugify("Q3 2024 Report") == "q3_2024_report"

    def test_hyphenated_words(self):
        assert slugify("well-known issue") == "well_known_issue"


# ---------------------------------------------------------------------------
# extract_title_from_markdown
# ---------------------------------------------------------------------------

class TestExtractTitleFromMarkdown:
    def test_atx_h1(self):
        assert extract_title_from_markdown("# My Title\n\nBody.") == "My Title"

    def test_atx_h2(self):
        assert extract_title_from_markdown("## Section Two") == "Section Two"

    def test_setext_equals(self):
        md = "Project Overview\n================\n\nSome text."
        assert extract_title_from_markdown(md) == "Project Overview"

    def test_setext_dashes(self):
        md = "Sub-section\n-----------\n\nDetails."
        assert extract_title_from_markdown(md) == "Sub-section"

    def test_no_heading_returns_none(self):
        assert extract_title_from_markdown("Just a paragraph.\nNo heading.") is None


# ---------------------------------------------------------------------------
# extract_title_from_html
# ---------------------------------------------------------------------------

class TestExtractTitleFromHtml:
    def test_title_tag(self):
        html = "<html><head><title>Page Title</title></head></html>"
        assert extract_title_from_html(html) == "Page Title"

    def test_h1_tag(self):
        html = "<body><h1>Main Heading</h1><p>Text</p></body>"
        assert extract_title_from_html(html) == "Main Heading"

    def test_prefers_title_over_h1(self):
        html = "<title>Document</title><h1>Different</h1>"
        assert extract_title_from_html(html) == "Document"

    def test_no_title_returns_none(self):
        assert extract_title_from_html("<p>No title here</p>") is None


# ---------------------------------------------------------------------------
# extract_title_from_json
# ---------------------------------------------------------------------------

class TestExtractTitleFromJson:
    def test_title_key(self):
        assert extract_title_from_json(json.dumps({"title": "My Doc"})) == "My Doc"

    def test_name_key(self):
        assert extract_title_from_json(json.dumps({"name": "Alice"})) == "Alice"

    def test_subject_key(self):
        data = json.dumps({"subject": "Invoice #42"})
        assert extract_title_from_json(data) == "Invoice #42"

    def test_no_known_key_returns_none(self):
        assert extract_title_from_json(json.dumps({"foo": "bar"})) is None

    def test_invalid_json_returns_none(self):
        assert extract_title_from_json("not json at all") is None

    def test_array_json_returns_none(self):
        assert extract_title_from_json(json.dumps([1, 2, 3])) is None


# ---------------------------------------------------------------------------
# derive_title
# ---------------------------------------------------------------------------

class TestDeriveTitle:
    def test_markdown_file_uses_heading(self, tmp_path):
        f = tmp_path / "notes.md"
        f.write_text("# Sprint Review\n\nDetails here.")
        assert derive_title(f, f.read_text()) == "Sprint Review"

    def test_html_file_uses_title_tag(self, tmp_path):
        f = tmp_path / "page.html"
        f.write_text("<title>Welcome Page</title><body></body>")
        assert derive_title(f, f.read_text()) == "Welcome Page"

    def test_json_file_uses_title_key(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text(json.dumps({"title": "Config Schema"}))
        assert derive_title(f, f.read_text()) == "Config Schema"

    def test_txt_fallback_to_first_line(self, tmp_path):
        f = tmp_path / "random.txt"
        f.write_text("Meeting agenda for Monday\nItem 1\nItem 2")
        assert derive_title(f, f.read_text()) == "Meeting agenda for Monday"

    def test_py_file_uses_docstring(self, tmp_path):
        f = tmp_path / "module.py"
        f.write_text('"""Utility functions for data processing."""\n\ndef foo(): pass')
        title = derive_title(f, f.read_text())
        assert title == "Utility functions for data processing."

    def test_empty_content_returns_stem(self, tmp_path):
        f = tmp_path / "mystery.txt"
        f.write_text("")
        assert derive_title(f, "") == "mystery"


# ---------------------------------------------------------------------------
# classify_topic
# ---------------------------------------------------------------------------

class TestClassifyTopic:
    def test_meeting_keywords(self):
        assert classify_topic("Agenda and minutes for the meeting with attendees") == "meetings"

    def test_finance_keywords(self):
        assert classify_topic("Invoice #123 payment due billing details") == "finance"

    def test_report_keywords(self):
        assert classify_topic("Quarterly report summary with findings and conclusion") == "reports"

    def test_no_match_returns_none(self):
        assert classify_topic("xyz zxc qwe random words no topics") is None

    def test_empty_string_returns_none(self):
        assert classify_topic("") is None


# ---------------------------------------------------------------------------
# unique_path
# ---------------------------------------------------------------------------

class TestUniquePath:
    def test_non_existing_path_unchanged(self, tmp_path):
        target = tmp_path / "newfile.txt"
        assert unique_path(target) == target

    def test_existing_path_gets_counter(self, tmp_path):
        existing = tmp_path / "file.txt"
        existing.write_text("x")
        result = unique_path(existing)
        assert result == tmp_path / "file_1.txt"

    def test_multiple_collisions(self, tmp_path):
        base = tmp_path / "file.txt"
        base.write_text("x")
        (tmp_path / "file_1.txt").write_text("x")
        result = unique_path(base)
        assert result == tmp_path / "file_2.txt"


# ---------------------------------------------------------------------------
# plan_rename (integration)
# ---------------------------------------------------------------------------

class TestPlanRename:
    def test_markdown_renamed_from_heading(self, tmp_path):
        f = tmp_path / "draft.md"
        f.write_text("# Budget Proposal 2025\n\nDetails.")
        source, destination = plan_rename(f)
        assert destination.stem == "budget_proposal_2025"
        assert destination.suffix == ".md"

    def test_file_with_no_content_uses_untitled(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        source, destination = plan_rename(f)
        # stem is "mystery" → derive_title returns original stem → slug
        assert destination.suffix == ".txt"

    def test_organise_puts_file_in_subfolder(self, tmp_path):
        f = tmp_path / "expense.txt"
        f.write_text("Invoice #42, payment, billing department")
        source, destination = plan_rename(f, organise=True)
        assert destination.parent.name == "finance"

    def test_no_organise_keeps_same_folder(self, tmp_path):
        f = tmp_path / "report.md"
        f.write_text("# Q3 Report\n\nFindings and conclusion.")
        source, destination = plan_rename(f, organise=False)
        assert destination.parent == tmp_path


# ---------------------------------------------------------------------------
# process_path (end-to-end, dry-run)
# ---------------------------------------------------------------------------

class TestProcessPath:
    def test_dry_run_does_not_rename(self, tmp_path):
        f = tmp_path / "old_name.md"
        f.write_text("# New Shiny Title\n\nContent.")
        ops = process_path(tmp_path, apply=False)
        # File should still have original name
        assert f.exists()

    def test_apply_renames_file(self, tmp_path):
        f = tmp_path / "old_name.md"
        f.write_text("# Renamed Document\n\nContent.")
        process_path(tmp_path, apply=True)
        assert not f.exists()
        assert (tmp_path / "renamed_document.md").exists()

    def test_apply_with_organise(self, tmp_path):
        f = tmp_path / "some_meeting.txt"
        f.write_text("Meeting agenda and minutes for the team attendees")
        process_path(tmp_path, organise=True, apply=True)
        assert not f.exists()
        # Should end up in meetings/ sub-folder
        meeting_files = list((tmp_path / "meetings").iterdir())
        assert len(meeting_files) == 1

    def test_skips_unsupported_extensions(self, tmp_path, capsys):
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG\r\n")
        process_path(f, apply=False)
        captured = capsys.readouterr()
        assert "unsupported extension" in captured.err

    def test_nonexistent_path_exits(self, tmp_path):
        with pytest.raises(SystemExit):
            process_path(tmp_path / "ghost.txt")

    def test_same_name_no_collision(self, tmp_path):
        """If the derived slug already matches the filename, keep it unchanged."""
        f = tmp_path / "budget_proposal.md"
        f.write_text("# Budget Proposal\n\nSome details.")
        ops = process_path(tmp_path, apply=True)
        # Source and destination should be equal (KEEP)
        for source, destination in ops:
            if source == f:
                assert source.resolve() == destination.resolve()
