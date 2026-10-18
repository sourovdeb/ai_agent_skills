---
name: local-software-launcher
description: Launch, resolve, search, list, and stop installed Windows software through the localSoftware MCP tools. Use when the user asks to open, run, or close a local program, file, shortcut, or URL, or to check mounted drives or installed apps.
---

# Local Software Launcher

Click-and-execute access to Windows software. `localSoftware.launch` is the
programmatic equivalent of double-clicking an app, file, shortcut, or URL.

## Tools

| Tool | Purpose |
|---|---|
| `localSoftware.launch` | Open a program, document, shortcut, or URL by name or path; returns resolved path and pid |
| `localSoftware.resolve` | Locate a program via PATH, App Paths registry, Start Menu shortcuts |
| `localSoftware.search` | Bounded executable search under Program Files, Local Programs, E:\tools, E:\apps, or custom roots |
| `localSoftware.list_apps` | Start Menu app names, optional substring filter |
| `localSoftware.list_drives` | Mounted drives with type and free/total bytes |
| `localSoftware.status` | Check whether a pid is still running |
| `localSoftware.stop` | Force-stop a process tree by pid (taskkill /T /F) |

## Method

1. Identify the software the task needs. If the exact name is unknown, use
   `list_apps` with a query, or `search` with a name substring.
2. `resolve` first when the exact install path matters.
3. `launch` it. Report the resolved path and pid from the tool output.
4. Verify with `status` when the launch must be confirmed running.
5. `stop` what you started unless the user wants it left open.

## Rules

- Evidence is the tool output: resolved path, pid, or taskkill exit code.
  Never claim a launch without it.
- Do not stop processes you did not start unless the user asked.
- `launch` accepts URLs and documents; Windows file associations apply.
- The server runs on the Vibe Python at
  `E:\tools\uv-tools\mistral-vibe\Scripts\python.exe` (pure stdlib, no installs).
  If that path stops working, point `mcp.json` at another Python 3.10+.
