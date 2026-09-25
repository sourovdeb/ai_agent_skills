# Set up Story Studio in Mistral

The screenshots establish the visible fields; current official documentation supplies the implementation distinctions. UI placement can vary by workspace/version. No Mistral account settings were changed during preparation of this pack. The available plugin directory did not expose a Mistral connection in this session.

## 1. Start with the author-facing agent

Use one Writing Director before creating multiple agents. In the Playground, select a model actually available in your workspace. The package pins `mistral-small-2603`, whose official model page lists Agents, function calling and structured outputs. This is a cost-sensitive starting choice, not proof that it is the cheapest or best creative-writing model. Use the compact runner for smaller-model trials; choose a stronger available model only after comparing the same tasks. Changing prompt text cannot switch the model. [S5]

In the agent's Instructions field paste **prompts/studio-agent.txt**. This includes the core and all six methods so it does not rely on an unverified native Skill attachment. The local runner instead composes the core plus one relevant method. Set text output for normal writing; use JSON only for a structured data task. The default temperature of 0.6 and output limit of 3,000 tokens are starting configuration choices, not measured optima. [S3, S6]

In the Create Agent dialog shown in your screenshot:

| Field | Value |
|---|---|
| Agent Name | Story Studio - Writing Director |
| Description | Story Bible, scene drafting, editing, continuity, sourced research and human narration coaching. |
| Optional metadata | package=mistral-writing-specialist; version=1.0.0; mode=author-assistant |

Metadata labels are descriptive, not instructions or security controls. Start with no custom functions. Enable built-in Web Search for research and Document Library only after configuring the relevant knowledge collection. Code Interpreter, image generation, MCP and background workers are not required for the initial writing workflow. [S3, S4]

## 2. Save the reusable Prompt

On the New prompt screen, set title **Story Studio - Writing Director**, identifier **story-studio-writing-director**, description **Develop, draft, revise and rehearse writing while preserving approved project canon**, and body from **prompts/studio-agent.txt**. The lowercase identifier follows the rule visible in your screenshot. Keep it private initially and create a new version when upgrading. [S1]

Saving a Prompt does not automatically bind it to every Agent. Copy the tested body into agent Instructions, or explicitly retrieve the desired registry version in application code. The official Prompt Registry guide fetches the definition and passes its content into a system message; do not invent a universal `prompt_id` field on unrelated request bodies. The supplied runner uses version-controlled local files and does not call the Prompt Registry API. [S7]

## 3. Create focused native Skills

For an agent-building assistant, create **mistral-writing-specialist** from the root SKILL.md. For author tasks, create the six focused Skills in `writing-skills/`. Use each YAML description for the Description field and its Markdown procedure for Instructions; keep the front matter when using a file-based skill host. Attach only genuinely needed templates/examples. [S2]

A saved Skill, workspace sharing, publishing to Vibe, and an Agent's tool configuration are different operations. The documentation describes testing on the intended surface. Do not assume the Skills list automatically equips an API Agent or that ZIP upload is supported. The compiled agent prompt is the explicit fallback; it already contains the methods. Do not add them a second time if that surface loads the same Skills natively. [S2, S3]

## 4. Build the Story Bible

Copy `knowledge/story-bible.template.json` into a private project folder and fill known facts only. Null and empty values mean unknown. The seven visible sections match the mobile screenshot. Supporting timeline/canon/source/session records make long work resumable. These are our project data conventions, not claims about the mobile app's storage schema.

For Studio-only work, supply the relevant sections in the conversation or create a Library and connect that Library to the agent. Uploading a raw file to Files is not the same as connecting a searchable Library. Wait until processing reports Completed and run a retrieval test: ask for a distinctive fact and its source locator. Keep only the currently approved snapshot in the active canon collection; archive or clearly separate superseded versions. Retrieval is evidence access, not reliable transactional write-back. [S4]

The local runner stores sections in SQLite, with proposals and drafts in separate tables. `stage_canon_update` creates a pending proposal; `approve` is a host-only CLI operation. Review the complete replacement because shape validation does not establish semantic correctness. Previous approved content is retained in the history table. Use a new filename for exports; do not overwrite the source manuscript.

## 5. Understand the Add function screen

`tools.json` contains three real function declarations: `get_project_context`, `stage_canon_update`, and `save_draft`. In the modal, copy the function's name and description, turn Strict on, and paste only its **parameters** object into Parameters. Do not paste the entire outer tools array into that field. [S8]

Those declarations do not execute Python or grant access to your computer. Their implementations are in writer.py and are driven by its chat-completion loop. Only register them on another agent after wiring an equivalent client-side handler or authenticated connector. Do not attach nonfunctional local tools to the standalone Studio agent. Strict JSON constrains argument shape; it does not validate plot logic or grant write permission. [S6, S8]

## 6. Use the separate mobile app's Custom Prompt

Paste **prompts/chat-personalization.txt** into the shown Chat Personalization field. This text asks the application to use the Story Bible that it actually supplies. It does not connect that app to Mistral, synchronize project files, install Skills or establish an API key. No brand identity or hidden app capability has been inferred from the screenshots.

## 7. Runtime, prerequisites and fallbacks

Studio-only requires an active account, an available model and the chosen built-in tools. The optional runner requires Python 3.10+ and write access to a private folder. Cloud commands additionally require MISTRAL_API_KEY in the process environment. It has no third-party Python dependencies and performs no local model inference; a 4 GB GPU is not used. Actual RAM and latency depend on input size and were not benchmarked on your machine.

Missing API access: use `compose` and paste the generated packet into an available text host. Model unavailable: inspect `models`, choose an accessible model in config.json, then rerun the same acceptance cases. Do not silently escalate price. Missing native Skills: use the compiled prompt. Missing Library: paste relevant versioned excerpts. Missing search: return evidence gaps instead of invented references. Missing audio/OCR: supply readable text. The runner does not implement transcription, OCR or TTS; those remain optional Studio ingestion services, not dependencies. Typesafe, Agnes and other providers are not required or secretly used.

Cloud calls are sequential, limited to four completion calls per task, with 3,000 output tokens per call and a 48,000-byte conversation ceiling. Tool descriptions add request overhead; the ceiling is not exact token accounting or a dollar cap. HTTP 429 has two bounded retries; other errors stop without a blind provider switch. No shell execution or publishing tool is exposed to the model. Usage counts are preserved in the response. Set any account-level spending cap separately in Studio.

Run EVALUATION.md on both your chosen compact and stronger model before treating either as production-ready. Offline tests do not establish literary quality, narration feasibility or a live API deployment.
