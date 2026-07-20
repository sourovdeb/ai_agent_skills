# OpenClaw Troubleshooting: Unknown Model Errors

**Problem:** Your agents fail with errors like: Unknown model: mistral/mistral-small-latest. Found agents.defaults.models["mistral/mistral-small-latest"], but no matching models.providers["mistral"].models[] entry.

Your fallback chain shows 28 models, but agents timeout trying each one.

---

## Solution

Models must be registered in BOTH locations:
1. Fallback chain (models.fallbacks)
2. Provider registry (models.providers.<provider>.models[])

Use PowerShell bracket notation:

```powershell
$config = Get-Content "$env:OPENCLAW_HOME\openclaw.json" | ConvertFrom-Json -Depth 10
$config.models.providers["mistral"]["models"] = @(
    @{id="mistral-small-latest"; name="mistral-small-latest"}
)
$config | ConvertTo-Json -Depth 10 | Set-Content "$env:OPENCLAW_HOME\openclaw.json"
```

---

## Why It Works

OpenClaw validates models exist in provider registry before using them.

---

## Prevention

- Always register models with providers before adding to fallback chains
- Use bracket notation: models.providers["provider"]["models"]
- Never use dot notation for dynamic properties

---

**Tags:** #openclaw #troubleshooting #models #providers #configuration