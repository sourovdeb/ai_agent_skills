# PowerShell: Dot Notation vs Bracket Notation

**Problem:** The property 'ollama-cloud' cannot be found on this object when using $config.models.providers.ollama-cloud

---

## Solution

Use bracket notation:

```powershell
# FAILS
$config.models.providers.ollama-cloud.models = @()

# WORKS
$config.models.providers["ollama-cloud"]["models"] = @()
```

---

**Tags:** #powershell #json #configuration #troubleshooting