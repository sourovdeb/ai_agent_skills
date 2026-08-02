# WP AI Studio — VS Code Extension

Source: `sourovdeb/wordpress-control`

WordPress site control extension for VS Code with AI-powered post generation.
Supports Claude, DeepSeek, and Ollama as AI providers.

## Features

- Open WP AI Studio panel inside VS Code
- Generate WordPress posts via AI
- Check site status
- Approval mode (all changes draft by default)

## Files

| File | Description |
|------|-------------|
| `extension.js` | Main VS Code extension entry point (~14KB) |
| `webview.js` | Webview panel UI with AI controls (~28KB) |
| `package.json` | Extension manifest (commands, configuration schema) |
| `icon.svg` | Extension activity bar icon |

## Configuration (VS Code settings)

All credentials are configured via VS Code settings — never hard-code in source files:

```json
{
  "wpai.wordpressUrl": "https://your-site.com",
  "wpai.wpUser": "your-username",
  "wpai.wpAppPassword": "[set in VS Code settings — never in files]",
  "wpai.aiProvider": "claude",
  "wpai.claudeKey": "[set in VS Code settings]",
  "wpai.approvalMode": true,
  "wpai.defaultStatus": "draft"
}
```

## Security

Credentials must be stored in VS Code settings UI, not in `settings.json` committed to
version control. Never paste API keys into chat, files, or markdown documents.

## Original Repository

`sourovdeb/wordpress-control` — the extension source lives there.
This folder mirrors the manifest and documentation for discoverability.
