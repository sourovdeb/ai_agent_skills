---
name: skill-seekers
description: Load this skill when you need to generate a custom skill from documentation, API docs, codebases, or PDFs. Point at any knowledge source and synthesize a native skill.
---

# Skill Seekers

A highly flexible meta-skill generator. Point this engine at any documentation site, API documentation, framework standard (React, Django, Godot), codebase, or PDF to instantly synthesize a native Claude Skill.

## Natural Triggers
- "create a skill from this doc"
- "generate skill from API"
- "make a skill for this framework"
- "convert documentation to skill"
- "build a custom skill"
- "synthesize from PDF"
- "documentation to skill"
- "auto-generate skill"
- "point at repo and generate"
- "turn docs into skill"

## Core Functionality

### Input Sources
- Documentation sites (web URLs)
- API documentation
- Framework standards (React, Django, Godot, etc.)
- Codebases (GitHub repositories)
- PDF documents
- Markdown files
- Technical specifications

### Output
- Ready-to-use SKILL.md file
- Proper YAML frontmatter
- Natural language triggers
- Structured instructions
- Category classification

### Process
1. Analyze source material
2. Identify key concepts and workflows
3. Extract trigger phrases
4. Generate skill structure
5. Create natural language instructions
6. Validate output

## Usage Examples

### From Documentation Site
User: "Create a skill from the React documentation"
Skill Seekers: Analyzes react.dev, extracts key concepts, generates react-skill/SKILL.md

### From API Documentation
User: "Generate a skill for the GitHub API"
Skill Seekers: Analyzes GitHub API docs, creates github-api-skill/SKILL.md

### From Codebase
User: "Make a skill from this Django project"
Skill Seekers: Analyzes repository structure, generates django-project-skill/SKILL.md

## Quality Standards

Generated skills should:
- Solve ONE highly specific problem really well
- Have concrete, natural language triggers
- Include clear usage examples
- Reference source material
- Be under 500 lines
- Handle a single primary task

## Customization

After generation, review and refine:
- Trigger phrases for discoverability
- Skill description clarity
- Instruction specificity
- Category assignment
- Reference links

## Advanced Features

### Batch Processing
Generate multiple skills from a documentation hub

### Template-Based Generation
Use predefined templates for specific domains:
- API clients
- Framework wrappers
- Documentation generators
- Testing utilities

## References
- Repository: https://github.com/yusufkaraaslan/Skill_Seekers
- Inspired by: Documentation-to-skill pattern

## Best Practices
- Start with high-quality source material
- Validate generated skills before use
- Customize triggers for your workflow
- Keep skills focused and specific
- Test with real use cases