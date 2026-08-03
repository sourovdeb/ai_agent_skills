# File Operations AI App — Prototype Plan

## Goal
Build a local-first desktop app for file intake, classification, Markdown conversion, move actions, and live execution logs.

## I want
- File manager with multi-folder intake
- Markdown conversion for convertible documents
- Content classification for documents, spreadsheets, PDFs, and scripts
- Metadata creation for every processed file
- Move rules for image, audio, and video files
- Separate handling for corrupt, locked, oversized, or non-convertible files
- Login gate before access
- Side panel for prompt-driven execution with local model or API connection
- Live log panel for every step
- Screenshot and HTML read support for browser-based analysis and execution

## Why
- Faster organization of mixed file collections
- Less manual sorting
- Better search and retrieval through Markdown plus metadata
- Safer handling of complex files through fallback moves instead of failed conversion
- Clear traceability through logs and per-file status

## How
### Core flow
1. User login
2. Folder selection, including multiple input locations
3. File scan and type detection
4. Route by file class:
   - Convertible document, spreadsheet, PDF, script → MarkItDown pipeline
   - Image, audio, video → keep in folder or move by rule
   - Corrupt, encrypted, oversized, unreadable → quarantine folder
5. Context extraction
6. AI classification and tag generation
7. Output creation:
   - Markdown file
   - Metadata JSON
   - Move action or copy action
8. Live logging and result summary

### Processing rules
- Simple files: full conversion
- Complex files: partial extraction, then metadata only
- Very large files: chunked read, then classification and move
- Images with diagrams: extract when supported, otherwise metadata plus move
- Scripts: read as text, classify by purpose, then convert to Markdown
- Archives: inspect contents, extract supported files, preserve source structure

### Model layer
- Local Ollama or LM Studio connection
- Optional API mode for remote inference
- Structured output for category, confidence, summary, tags, and destination folder
- Prompt templates for document type, sensitivity, department, and action

### Browser and page analysis
- Playwright for page capture, DOM read, and screenshot capture
- HTML extraction for visible content and page metadata
- Execution trace stored in the live log panel

## Prototype scope
### App 1: File Manager + Markdown Converter
- Folder picker
- Queue view
- Convert button
- Classification results
- Move-to-folder action
- Metadata output
- Quarantine folder
- Log panel

### App 2: Prompt Console
- Login gate
- Connection selector: Ollama or API
- Upload zone for CSV, Markdown, PDF, and supported text files
- Prompt box
- Live output panel
- Browser capture tab for screenshot and HTML read tasks

## Suggested stack
- Desktop shell: Tauri or Electron
- Frontend: React + TypeScript
- Local file engine: Python service
- File conversion: MarkItDown
- Local model runtime: Ollama or LM Studio
- Automation layer: LangChain for loaders and structured output
- Workflow orchestration: n8n for chained jobs and external integrations
- Browser automation: Playwright
- Storage: SQLite for jobs, files, tags, and audit trail

## Data objects
### File record
- id
- source_path
- output_path
- file_type
- status
- model_used
- confidence
- tags
- category
- destination_folder
- error_message
- created_at

### Job record
- id
- user_id
- input_folders
- prompt
- action_type
- status
- log_path
- created_at

## UI screens
1. Login
2. Folder selection
3. File queue
4. Review and classify
5. Convert and move
6. Prompt console
7. Live log viewer
8. Settings

## MVP acceptance
- Multiple folders scanned successfully
- Supported documents converted to Markdown
- Non-convertible files moved to quarantine or user-selected folder
- AI-generated tags and categories saved
- Live logs visible during execution
- Prompt console handles uploads and executes tasks
- Screenshot and HTML read available for web pages

## Next build step
Create the folder tree, API contracts, and the first working desktop shell with one conversion path and one prompt-driven execution path.
