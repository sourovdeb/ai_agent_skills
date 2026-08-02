# Configuration & Reference

Reference documentation and configuration files for the repository.

## Reference Files

| File | Purpose |
|------|----------|
| JSON Schemas.MD | Schema definitions for validating agent outputs and data structures |
| GIF_MD.MD | Markdown reference for embedding and creating GIF documentation |
| update.MD | Update procedures, changelog, and version management |

## JSON Schema Usage

Use the JSON schemas to:
- Validate agent outputs programmatically
- Define expected data structures
- Document API contracts
- Generate documentation automatically

Example:
```python
from json_schemas import validate_skill_output
validate_skill_output(output_data, schema_name='SkillOutput')
```

## GIF Markdown

Create animated documentation:
- Embed GIFs in markdown files
- Reference tools in `/tools/gif-builder.py`
- Use easing functions from `/tools/gif_easing.py`

## Updates & Maintenance

Track repository updates:
- Review `update.MD` for recent changes
- Follow version management procedures
- Document your contributions

---
*Part of the ai_agent_skills repository*