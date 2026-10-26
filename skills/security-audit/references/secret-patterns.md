# Secret Detection Patterns

## Regex Patterns for Common Secret Types

### API Keys
```
# AWS
AKIA[0-9A-Z]{16}
ASIA[0-9A-Z]{16}

# Google
AIza[0-9A-Za-z\-_]{35}

# GitHub
ghp_[0-9a-zA-Z]{36}
gho_[0-9a-zA-Z]{36}
ghu_[0-9a-zA-Z]{36}
ghs_[0-9a-zA-Z]{36}
ghr_[0-9a-zA-Z]{36}

# Stripe
sk_live_[0-9a-zA-Z]{24}
pk_live_[0-9a-zA-Z]{24}
sk_test_[0-9a-zA-Z]{24}

# Slack
xox[baprs]-[0-9]{10,13}-[0-9a-zA-Z-]+

# Twilio
SK[0-9a-fA-F]{32}

# SendGrid
SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}

# Generic API key patterns
(?i)(api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*["']?[0-9a-zA-Z\-_]{16,}["']?
(?i)(secret[_-]?key|secret)\s*[=:]\s*["']?[0-9a-zA-Z\-_]{16,}["']?
```

### Private Keys
```
-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY( BLOCK)?-----
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

### Passwords and Tokens
```
(?i)(password|passwd|pwd)\s*[=:]\s*["']?[^\s"']{8,}["']?
(?i)(token|auth[_-]?token|access[_-]?token|bearer)\s*[=:]\s*["']?[0-9a-zA-Z\-_\.]{16,}["']?
(?i)(private[_-]?key|client[_-]?secret)\s*[=:]\s*["']?[0-9a-zA-Z\-_]{16,}["']?
```

### Database Connection Strings
```
# PostgreSQL
postgres(ql)?://[^:]+:[^@]+@[^/]+/

# MySQL
mysql://[^:]+:[^@]+@[^/]+/

# MongoDB
mongodb(\+srv)?://[^:]+:[^@]+@[^/]+/

# Redis
redis://[^:]+:[^@]+@[^/]+/
```

### Cloud Credentials
```
# AWS Secret Key (40 chars, base64-like)
(?i)aws(.{0,20})?(?-i)['"][0-9a-zA-Z/+]{40}['"]

# Azure
(?i)(azure|account[_-]?key)\s*[=:]\s*["']?[0-9a-zA-Z+/=]{40,}["']?

# GCP
(?i)(gcp|google).{0,20}(private[_-]?key|client[_-]?email)
```

### Generic High-Entropy Strings
Look for base64 or hex strings > 20 chars assigned to variables with suspicious names:
```
(?i)(key|secret|token|password|credential|auth).{0,10}[=:]\s*["'][0-9a-zA-Z+/=]{20,}["']
```

## Files to Always Check

- `.env`, `.env.*`, `.env.local`, `.env.production`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`
- `credentials*`, `secrets*`, `config/secrets*`
- `.github/workflows/*.yml` (CI/CD secrets)
- `docker-compose.yml`, `Dockerfile`
- `*.tf`, `*.tfvars` (Terraform)
- `serverless.yml`, `serverless.ts`
- `.npmrc`, `.pypirc`, `.netrc`
- `id_rsa`, `id_ed25519`, `*.ppk`

## Files to Exclude from Scanning

- `node_modules/`, `vendor/`, `.git/`
- `dist/`, `build/`, `coverage/`
- `*.lock`, `package-lock.json`, `yarn.lock` (false positives)
- Binary files, images, PDFs

## Entropy Heuristics

High-entropy strings are likely secrets:
- Shannon entropy > 4.5 for base64-like strings
- Shannon entropy > 3.5 for hex strings
- Length > 20 characters
- Assigned to variables named: key, secret, token, password, credential

## CI/CD Specific Checks

### GitHub Actions
```yaml
# Look for hardcoded secrets instead of ${{ secrets.NAME }}
env:
  API_KEY: "sk_live_abc123..."  # BAD
  API_KEY: ${{ secrets.API_KEY }}  # GOOD
```

### Docker
```dockerfile
# BAD: secrets in Dockerfile
ENV API_KEY=sk_live_abc123

# GOOD: use build args or secrets
ARG API_KEY
```

## Response to Finding a Secret

1. **Do NOT commit the secret**
2. **Revoke/rotate the secret immediately** at the provider
3. **Remove from git history** if already committed:
   ```bash
   # Using git filter-repo (recommended)
   git filter-repo --invert-paths --path path/to/file-with-secret

   # Or BFG Repo-Cleaner
   bfg --delete-files secret-file.env
   ```
4. **Use environment variables or a secrets manager**
5. **Add pre-commit hooks** to prevent future leaks:
   ```bash
   # Using gitleaks
   gitleaks protect --staged
   ```
