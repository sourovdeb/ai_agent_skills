---
name: "defense-in-depth-hardening"
description: "Load this skill when you need to apply a rigorous, multi-layered security assessment paradigm to surface vulnerabilities, sanitize input paths, and harden custom codebases."
---
# Defense-in-Depth Hardening

Applies a rigorous, multi-layered security assessment paradigm across code structures to surface vulnerabilities, sanitize input paths, and overall harden custom codebases.

## Natural Triggers
- "secure this codebase"
- "harden the application"
- "security audit"
- "vulnerability assessment"
- "defense in depth"
- "security review"
- "code hardening"
- "secure coding"
- "threat modeling"

## Core Principles

### Defense in Depth
Multiple layers of security controls so that if one fails, others still provide protection.

### Security by Design
Security considerations integrated into every phase of development.

### Least Privilege
Users, processes, and systems have only the minimum permissions necessary.

### Fail Securely
Systems fail in a secure state, denying access by default.

### Keep It Simple
Complexity is the enemy of security. Simple, understandable code is more secure.

## Security Layers

### Layer 1: Code Level
- Input validation
- Output encoding
- Secure coding practices
- Error handling
- Logging

### Layer 2: Framework Level
- Framework security features
- Dependency security
- Configuration security
- Middleware security

### Layer 3: Application Level
- Authentication
- Authorization
- Session management
- Rate limiting
- CSRF protection

### Layer 4: Infrastructure Level
- Network security
- Host security
- Container security
- Secrets management

### Layer 5: Operational Level
- Monitoring
- Incident response
- Patch management
- Security updates
- Backup and recovery

## Assessment Workflow

### Phase 1: Discovery
1. **Inventory Assets**
   - List all applications
   - Identify all dependencies
   - Map data flows
   - Document trust boundaries

2. **Threat Modeling**
   - Identify threats using STRIDE
   - Create data flow diagrams
   - Identify trust boundaries
   - Document attack surfaces

3. **Risk Assessment**
   - Identify vulnerabilities
   - Assess impact
   - Determine likelihood
   - Calculate risk scores

### Phase 2: Code Analysis

#### Static Analysis
```bash
# Run linters
npm run lint
npm run type-check

# Security-focused linters
npm install -g eslint-plugin-security
npm run lint:security

# SAST tools
# Semgrep
semgrep --config=p/ci

# SonarQube
sonar-scanner

# Bandit (Python)
bandit -r .

# Goblin (Go)
goblin .
```

#### Dependency Analysis
```bash
# Check for vulnerable dependencies
npm audit
npm audit fix

# Snyk
npx snyk test
npx snyk monitor

# OWASP Dependency Check
dependency-check.sh --project "My Project" --scan .
```

#### Secrets Detection
```bash
# GitLeaks
gitleaks detect --source .

# TruffleHog
trufflehog --regex --entropy=False .

# GitHub Secret Scanning
git secrets --scan .
```

### Phase 3: Dynamic Analysis

#### Runtime Testing
```bash
# OWASP ZAP
zap-baseline.py -t http://localhost:3000

# Nikto
nikto -h http://localhost:3000

# Nuclei
nuclei -u http://localhost:3000 -t ~/
```

#### Fuzzing
- Use ffuf Security Fuzzer skill
- Test all input vectors
- Validate error handling
- Check for information disclosure

#### Penetration Testing
- Manual testing
- Automated scanning
- Exploit attempts (in controlled environments)
- Social engineering testing

### Phase 4: Configuration Review

#### Application Configuration
```bash
# Check for sensitive data in config files
grep -r "password\|secret\|key\|token" config/

# Validate configuration
npm run config:validate
```

#### Infrastructure Configuration
```bash
# Check Docker configurations
docker scan

# Check Kubernetes configurations
kubesec scan

# Check cloud configurations
# AWS
checkov -d .
# Terraform
checkov -d terraform/
```

#### Network Configuration
- Firewall rules review
- Network segmentation
- Access controls
- VPN configurations

### Phase 5: Hardening

## Code Hardening

### Input Validation
```javascript
// BAD: No validation
app.get('/api/user', (req, res) => {
  const userId = req.query.id;
  // ...
});

// GOOD: Proper validation
app.get('/api/user', (req, res) => {
  const userId = req.query.id;
  if (!/^[a-f0-9]{24}$/.test(userId)) {
    return res.status(400).send('Invalid user ID');
  }
  // ...
});
```

### Output Encoding
```javascript
// BAD: No encoding
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${query}</h1>`);
});

// GOOD: Proper encoding
const escape = require('escape-html');
app.get('/search', (req, res) => {
  const query = escape(req.query.q);
  res.send(`<h1>Results for: ${query}</h1>`);
});
```

### Error Handling
```javascript
// BAD: Leaking stack traces
app.use((err, req, res, next) => {
  res.status(500).send(err.stack);
});

// GOOD: Safe error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Internal Server Error');
});
```

### Secure Defaults
```javascript
// BAD: Insecure defaults
app.use(express.json({ limit: '100mb' }));

// GOOD: Secure defaults
app.use(express.json({ limit: '10kb' }));
app.disable('x-powered-by');
app.use(helmet());
```

## Framework-Specific Hardening

### Express.js
```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const csrf = require('csurf');
const cookieParser = require('cookie-parser');

const app = express();

// Security middleware
app.use(helmet());
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));
app.use(cookieParser());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// CSRF protection
app.use(csrf({ cookie: true }));

// Disable X-Powered-By
app.disable('x-powered-by');
```

### Django
```python
# settings.py

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
```

### Spring Boot
```java
// application.properties

# Security
server.port=8443
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=changeit
server.ssl.keyStoreType=PKCS12

# Session
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.http-only=true

# Headers
server.servlet.session.cookie.same-site=lax
```

## Infrastructure Hardening

### Docker
```dockerfile
# Use minimal base images
FROM alpine:3.18

# Run as non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Use multi-stage builds
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
USER nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Kubernetes
```yaml
# Deployment with security context
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: my-app
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
```

## Monitoring & Logging

### Security Logging
```javascript
// Security event logging
const securityLogger = require('./securityLogger');

app.use((req, res, next) => {
  // Log failed login attempts
  if (req.path === '/login' && req.method === 'POST') {
    securityLogger.log('login_attempt', {
      ip: req.ip,
      userAgent: req.get('User-Agent'),
      success: res.statusCode === 200
    });
  }
  next();
});
```

### Monitoring
- Set up SIEM (Splunk, ELK, etc.)
- Configure security alerts
- Monitor for anomalous behavior
- Set up dashboards for security metrics

## Incident Response

### Preparation
- Create incident response plan
- Define roles and responsibilities
- Set up communication channels
- Prepare tools and access

### Detection & Analysis
- Identify security incidents
- Contain affected systems
- Preserve evidence
- Analyze root cause

### Response
- Remove malicious access
- Patch vulnerabilities
- Restore systems from backups
- Rotate credentials

### Recovery
- Validate system integrity
- Monitor for recurrence
- Update documentation
- Conduct post-incident review

## Compliance

### Standards
- OWASP Top 10
- CIS Benchmarks
- NIST Guidelines
- ISO 27001
- PCI DSS
- GDPR
- HIPAA

### Checklists
- [ ] Input validation on all user inputs
- [ ] Output encoding for all user outputs
- [ ] Authentication and authorization implemented
- [ ] Session management secure
- [ ] Error handling doesn't leak information
- [ ] Sensitive data encrypted
- [ ] Dependencies up to date and secure
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Logging configured
- [ ] Monitoring in place
- [ ] Incident response plan exists

## Security Testing Checklist

### Code Review Checklist
- [ ] All user inputs validated
- [ ] All user outputs encoded
- [ ] No hardcoded secrets
- [ ] Error handling secure
- [ ] Logging appropriate
- [ ] Dependencies secure
- [ ] Authentication/authorization implemented
- [ ] Session management secure
- [ ] Rate limiting in place
- [ ] Security headers configured

### Penetration Testing Checklist
- [ ] Information gathering
- [ ] Configuration management testing
- [ ] Authentication testing
- [ ] Authorization testing
- [ ] Session management testing
- [ ] Input validation testing
- [ ] Error handling testing
- [ ] Cryptography testing
- [ ] Business logic testing
- [ ] Client-side testing

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- OWASP Top 10: https://owasp.org/Top10/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks/
- NIST Guidelines: https://csrc.nist.gov/

## Integration with Other Skills
- **ffuf Security Fuzzer**: For vulnerability discovery
- **Systematic Debugging**: For analyzing security issues
- **Test-Driven Development**: For writing security tests
- **Webapp Testing via Playwright**: For security testing of web applications
