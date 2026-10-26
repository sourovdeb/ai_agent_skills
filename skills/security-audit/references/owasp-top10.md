# OWASP Top 10 (2021) — Detection Checklist

## A01:2021 — Broken Access Control

**What to look for:**
- Missing authorization checks on endpoints
- IDOR: users can access other users' data by changing IDs
- Privilege escalation paths (user → admin)
- CORS misconfiguration allowing unauthorized origins
- Access control checks only on the client side
- Metadata access (e.g., cloud metadata endpoints)

**Detection patterns:**
- Routes/endpoints without auth middleware
- Direct object references without ownership checks
- `userId` from request body instead of session/token
- Missing role checks on admin endpoints

**Safe pattern:**
```typescript
// Check ownership at the data access layer
async function getDocument(id: string, userId: string) {
  const doc = await db.documents.findOne({ _id: id, ownerId: userId });
  if (!doc) throw new NotFoundError();
  return doc;
}
```

---

## A02:2021 — Cryptographic Failures

**What to look for:**
- Sensitive data stored in plaintext
- Weak algorithms: MD5, SHA1, DES, ECB mode
- Hardcoded encryption keys or IVs
- Missing encryption for data in transit (no TLS)
- Weak random number generation for tokens/sessions
- Passwords hashed without salt or with weak hashing (bcrypt < 10 rounds)

**Detection patterns:**
- `MD5`, `SHA1`, `DES` used for security purposes
- `Math.random()` for tokens, session IDs, or nonces
- Hardcoded keys: `const key = "abc123"`
- `http://` URLs for sensitive data

**Safe pattern:**
```typescript
// Use strong, modern crypto
import { hash, compare } from 'bcrypt';
const hashed = await hash(password, 12); // 12 rounds minimum

// Use crypto-secure random
import { randomBytes } from 'crypto';
const token = randomBytes(32).toString('hex');
```

---

## A03:2021 — Injection

**What to look for:**
- SQL injection: string concatenation in queries
- NoSQL injection: user input in MongoDB queries
- OS command injection: user input in exec/spawn/system
- LDAP/XPath/Header/Log injection
- Template injection (SSTI)

**Detection patterns:**
```typescript
// SQL Injection
`SELECT * FROM users WHERE id = ${userId}`  // BAD
`SELECT * FROM users WHERE id = '${userId}'`  // BAD

// Command Injection
exec(`ls ${userInput}`)  // BAD

// NoSQL Injection
db.users.find({ username: req.body.username })  // BAD if not validated

// Template Injection
render(`Hello ${userInput}`)  // BAD if userInput is a template
```

**Safe pattern:**
```typescript
// Parameterized queries
db.query('SELECT * FROM users WHERE id = ?', [userId]);

// ORM with parameterization
await User.findOne({ where: { id: userId } });

// Input validation before use
if (!isValidUsername(username)) throw new ValidationError();
```

---

## A04:2021 — Insecure Design

**What to look for:**
- Missing or ineffective security controls in the design
- Business logic flaws (negative amounts, race conditions in transactions)
- Lack of rate limiting on sensitive operations
- Missing threat modeling for new features

**Detection patterns:**
- No rate limiting on login/password reset
- Business logic that allows negative quantities
- State machines with invalid transitions
- Missing transaction boundaries for financial operations

---

## A05:2021 — Security Misconfiguration

**What to look for:**
- Default credentials in use
- Debug mode enabled in production
- Unnecessary features enabled (ports, services, pages)
- Missing security headers
- Verbose error messages exposing stack traces
- Permissive CORS (`Access-Control-Allow-Origin: *`)

**Detection patterns:**
- `debug: true` in production config
- Stack traces in API error responses
- Default admin credentials
- Missing CSP, HSTS, X-Frame-Options headers
- Directory listing enabled

**Required security headers:**
```
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

---

## A06:2021 — Vulnerable and Outdated Components

**What to look for:**
- Dependencies with known CVEs
- Outdated frameworks/libraries
- Unused dependencies (increase attack surface)
- Components from untrusted sources

**Detection:**
```bash
npm audit
pip-audit
cargo audit
govulncheck ./...
```

---

## A07:2021 — Identification and Authentication Failures

**What to look for:**
- Weak password policies
- Missing or weak MFA
- Session fixation
- Credentials in URLs
- No account lockout / rate limiting on login
- Weak session tokens (predictable, short, no expiry)
- JWT with `alg: none` or weak secrets

**Detection patterns:**
- `jwt.sign(payload, 'secret')` with weak/hardcoded secret
- Session tokens without expiry
- Password reset tokens that don't expire
- Login without rate limiting

---

## A08:2021 — Software and Data Integrity Failures

**What to look for:**
- Insecure deserialization
- CI/CD pipeline without integrity checks
- Auto-update without signature verification
- Unsigned or unverified plugins/dependencies

**Detection patterns:**
- `pickle.loads()` on untrusted data (Python)
- `ObjectInputStream.readObject()` on untrusted data (Java)
- `unserialize()` on user input (PHP)
- `Marshal.load()` on untrusted data (Ruby)
- `eval()` on untrusted data

---

## A09:2021 — Security Logging and Monitoring Failures

**What to look for:**
- Sensitive data in logs (passwords, tokens, PII)
- Missing logs for security events (login failures, access control failures)
- Logs not monitored or alerted on
- No audit trail for sensitive operations

**Detection patterns:**
- `console.log(password)` or logging request bodies with credentials
- No logging on authentication failures
- No logging on authorization failures (403s)

---

## A10:2021 — Server-Side Request Forgery (SSRF)

**What to look for:**
- User-controlled URLs fetched by the server
- No validation of URL schemes (file://, gopher://)
- No allowlist of permitted hosts
- Access to internal services (cloud metadata, internal APIs)

**Detection patterns:**
- `fetch(userProvidedUrl)`
- `axios.get(req.body.url)`
- Webhook URLs that are user-controlled
- Image/document processing with user-provided URLs

**Safe pattern:**
```typescript
// Validate URL against allowlist
const ALLOWED_HOSTS = ['api.example.com', 'cdn.example.com'];
const url = new URL(userProvidedUrl);
if (!ALLOWED_HOSTS.includes(url.hostname)) throw new ValidationError();
if (url.protocol !== 'https:') throw new ValidationError();
```
