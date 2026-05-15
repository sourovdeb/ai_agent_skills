# AI Agent Skill: Reorganise and Rename Based on Document Contents

## Rule

**Always reorganise and rename files based on the contents inside the document.**

When asked to work with documents, files, or a directory of files, the agent
must:

1. **Read the content** of each file before deciding on a name or location.
2. **Derive a descriptive name** from the content (e.g. the first heading,
   module docstring, JSON `title` field, or first meaningful sentence).
3. **Rename the file** to a lowercase, underscore-separated slug that reflects
   what the document actually contains — never rely solely on the existing
   filename.
4. **Reorganise into topic sub-folders** (when `--organise` is requested)
   based on detected keywords (meetings, finance, reports, docs, tests,
   config, tasks, notes, scripts, data).
5. **Default to a dry-run** (show what *would* change) and only apply changes
   when the user explicitly confirms or passes `--apply`.

## Skill script

The implementation lives in [`skills/reorganise_rename.py`](../skills/reorganise_rename.py).

### Supported file types

`.txt` · `.md` · `.rst` · `.html` · `.csv` · `.json` · `.yaml` / `.yml` ·
`.py` · `.js` · `.ts` · `.java` · `.go` · `.rb` · `.php` · `.cpp` · `.c` ·
`.cs` · `.sh` · `.log`

### Quick reference

```bash
# Preview renames for a single file
python skills/reorganise_rename.py my_notes.txt

# Preview renames for an entire directory
python skills/reorganise_rename.py ./documents

# Apply renames
python skills/reorganise_rename.py ./documents --apply

# Apply renames AND organise into topic sub-folders
python skills/reorganise_rename.py ./documents --organise --apply
```

## Title-extraction strategy

| File type | Strategy |
|-----------|----------|
| Markdown / RST | First ATX (`#`) or setext (`===`/`---`) heading |
| HTML | `<title>` tag, then first `<h1>` |
| JSON | `title`, `name`, `subject`, `description`, or `label` key |
| Python | Module docstring first line, then first class/function name |
| Shell / YAML | First non-blank comment line (`#`) |
| Other code | First `//` comment line |
| Fallback (all types) | First non-blank, non-punctuation line (up to 80 chars) |

## Naming rules

* All lowercase.
* Words separated by underscores.
* Leading stop-words removed (`a`, `an`, `the`, `and`, …).
* Special characters stripped.
* Slug truncated to 60 characters.
* Numeric suffix appended automatically if a name collision occurs.
