# ai_agent_skills

Specific rules for specific tasks — a collection of AI agent skills.

---

## Skill: Reorganise and Rename Based on Document Contents

**Rule:** Always reorganise and rename files based on the contents inside the
document, not the existing filename.

The skill reads each file, extracts a meaningful title from the content
(heading, docstring, JSON key, or first meaningful line), converts it to a
clean slug, and renames the file accordingly.  Optionally it also moves files
into topic sub-folders detected from the content.

### Usage

```bash
# Preview renames (dry-run, default)
python skills/reorganise_rename.py path/to/file_or_directory

# Apply renames
python skills/reorganise_rename.py path/to/directory --apply

# Apply renames AND organise into topic sub-folders
python skills/reorganise_rename.py path/to/directory --organise --apply
```

### Supported file types

`.txt` `.md` `.rst` `.html` `.csv` `.json` `.yaml` `.yml`
`.py` `.js` `.ts` `.java` `.go` `.rb` `.php` `.cpp` `.c` `.cs` `.sh` `.log`

### Running tests

```bash
pip install pytest
pytest tests/
```

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for
the full rule specification used by the AI agent.
