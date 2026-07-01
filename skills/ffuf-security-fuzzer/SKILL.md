---
name: "ffuf-security-fuzzer"
description: "Load this skill when you need to integrate web application fuzzing and security exploration tools into your prompt sequences for dynamic analysis and security posture verification."
---
# ffuf Security Fuzzer

Integrates web application fuzzing and security exploration tools directly into your prompt sequences. Best utilized for dynamic analysis and security posture verification.

## Natural Triggers
- "fuzz this endpoint"
- "security testing"
- "vulnerability scanning"
- "web app fuzzing"
- "penetration testing"
- "find security issues"
- "test API endpoints"
- "discover hidden paths"
- "security assessment"

## Core Capabilities

### Web Fuzzing
- Directory brute-forcing
- Parameter fuzzing
- File discovery
- API endpoint enumeration
- Subdomain discovery

### Security Testing
- Vulnerability detection
- Input validation testing
- Authentication testing
- Authorization testing
- Session management testing

### Dynamic Analysis
- Real-time request/response analysis
- Error-based detection
- Time-based detection
- Content-based detection

## Setup

### Installation
```bash
# Install ffuf
go install github.com/ffuf/ffuf/v2@latest

# Or using package manager
brew install ffuf
apt install ffuf

# Verify installation
ffuf -V
```

### Basic Usage
```bash
# Simple directory brute-forcing
ffuf -u http://target.com/FUZZ -w wordlist.txt

# Parameter fuzzing
ffuf -u http://target.com/api?param=FUZZ -w values.txt

# Multiple parameters
ffuf -u http://target.com/api?param1=FUZZ&param2=FUZ2Z -w wordlist1.txt -w wordlist2.txt
```

## Wordlists

### Common Wordlists
- `/usr/share/wordlists/dirb/common.txt` - Common directories
- `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt` - Medium directory list
- `raft-small-directories.txt` - Small, high-quality directories
- `raft-small-files.txt` - Common filenames
- `common.txt` - Common words

### Custom Wordlists
```bash
# Create custom wordlist
cat > custom.txt << EOF
admin
login
api
v1
v2
backup
config
EOF

# Use custom wordlist
ffuf -u http://target.com/FUZZ -w custom.txt
```

### Wordlist Management
```bash
# Download SecLists
git clone https://github.com/danielmiessler/SecLists

# Use SecLists wordlists
ffuf -u http://target.com/FUZZ -w SecLists/Discovery/Web-Content/common.txt
```

## Fuzzing Techniques

### Directory Brute-Forcing
```bash
# Basic directory fuzzing
ffuf -u http://target.com/FUZZ -w wordlist.txt

# With extensions
ffuf -u http://target.com/FUZZ.php -w wordlist.txt

# Multiple extensions
ffuf -u http://target.com/FUZZ -w wordlist.txt -e .php,.html,.aspx

# Recursive (with depth)
ffuf -u http://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 2
```

### Parameter Fuzzing
```bash
# Single parameter
ffuf -u http://target.com/api?user=FUZZ -w usernames.txt

# Multiple parameters (same wordlist)
ffuf -u http://target.com/api?user=FUZZ&pass=FUZZ -w users.txt

# Multiple parameters (different wordlists)
ffuf -u http://target.com/api?user=FUZZ&pass=FUZ2Z -w users.txt -w passwords.txt

# All HTTP methods
ffuf -u http://target.com/api/FUZZ -w wordlist.txt -X GET,POST,PUT,DELETE,HEAD,OPTIONS
```

### Subdomain Enumeration
```bash
# Subdomain brute-forcing
ffuf -u http://FUZZ.target.com -w subdomains.txt

# With DNS resolution only (no HTTP)
ffuf -u http://FUZZ.target.com -w subdomains.txt -mode dns

# Wildcard DNS filtering
ffuf -u http://FUZZ.target.com -w subdomains.txt -fs 1234
```

### Header Fuzzing
```bash
# Fuzz User-Agent header
ffuf -u http://target.com -H "User-Agent: FUZZ" -w user-agents.txt

# Fuzz custom header
ffuf -u http://target.com/api -H "X-API-Key: FUZZ" -w api-keys.txt

# Fuzz multiple headers
ffuf -u http://target.com/api -H "Authorization: FUZZ" -H "X-Custom: FUZ2Z" -w tokens.txt -w custom.txt
```

### POST Data Fuzzing
```bash
# Fuzz POST parameters
ffuf -u http://target.com/login -X POST -d "username=admin&password=FUZZ" -w passwords.txt

# Fuzz JSON body
ffuf -u http://target.com/api -X POST -H "Content-Type: application/json" -d '{"user":"admin","token":"FUZZ"}' -w tokens.txt

# Fuzz raw POST data
ffuf -u http://target.com/api -X POST -d "data=FUZZ" -w payloads.txt
```

## Filters

### Response Size Filtering
```bash
# Filter by response size
ffuf -u http://target.com/FUZZ -w wordlist.txt -fs 1234

# Filter by size range
ffuf -u http://target.com/FUZZ -w wordlist.txt -fs 1000-2000
```

### Status Code Filtering
```bash
# Filter out 404 responses
ffuf -u http://target.com/FUZZ -w wordlist.txt -fc 404

# Filter multiple status codes
ffuf -u http://target.com/FUZZ -w wordlist.txt -fc 404,403

# Only show specific status codes
ffuf -u http://target.com/FUZZ -w wordlist.txt -mc 200,204,301,302
```

### Word Count Filtering
```bash
# Filter by word count
ffuf -u http://target.com/FUZZ -w wordlist.txt -fw 10

# Filter by word count range
ffuf -u http://target.com/FUZZ -w wordlist.txt -fw 5-20
```

### Line Count Filtering
```bash
# Filter by line count
ffuf -u http://target.com/FUZZ -w wordlist.txt -fl 5
```

### Regex Filtering
```bash
# Filter responses matching regex
ffuf -u http://target.com/FUZZ -w wordlist.txt -mr "error|fail|exception"

# Filter responses NOT matching regex
ffuf -u http://target.com/FUZZ -w wordlist.txt -mr "success" -fr
```

## Rate Limiting & Performance

### Rate Control
```bash
# Set requests per second
ffuf -u http://target.com/FUZZ -w wordlist.txt -rate 100

# Random delay between requests
ffuf -u http://target.com/FUZZ -w wordlist.txt -p "0.1-0.5"
```

### Threads
```bash
# Set number of threads
ffuf -u http://target.com/FUZZ -w wordlist.txt -t 50

# Auto-tune threads
ffuf -u http://target.com/FUZZ -w wordlist.txt -t auto
```

### Timeouts
```bash
# Set timeout
ffuf -u http://target.com/FUZZ -w wordlist.txt -timeout 10

# Connection timeout
ffuf -u http://target.com/FUZZ -w wordlist.txt -ct 5
```

## Output & Reporting

### Output Formats
```bash
# JSON output
ffuf -u http://target.com/FUZZ -w wordlist.txt -o output.json -of json

# HTML output
ffuf -u http://target.com/FUZZ -w wordlist.txt -o output.html -of html

# CSV output
ffuf -u http://target.com/FUZZ -w wordlist.txt -o output.csv -of csv

# EJSON (extended JSON)
ffuf -u http://target.com/FUZZ -w wordlist.txt -o output.ejson -of ejson
```

### Verbose Output
```bash
# Show all requests/responses
ffuf -u http://target.com/FUZZ -w wordlist.txt -v

# Debug mode (very verbose)
ffuf -u http://target.com/FUZZ -w wordlist.txt -debug
```

### Quiet Mode
```bash
# Only show results
ffuf -u http://target.com/FUZZ -w wordlist.txt -s
```

### Color Output
```bash
# Disable colors
ffuf -u http://target.com/FUZZ -w wordlist.txt -c

# Force colors
ffuf -u http://target.com/FUZZ -w wordlist.txt -color
```

## Advanced Techniques

### Recursive Fuzzing
```bash
# Find directories, then fuzz within them
ffuf -u http://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 3

# With recursion and extensions
ffuf -u http://target.com/FUZZ -w wordlist.txt -e .php,.html -recursion -recursion-depth 2
```

### Multi-Mode Fuzzing
```bash
# DNS + HTTP mode
ffuf -u http://FUZZ.target.com -w subdomains.txt -mode dns,http

# All modes
ffuf -u http://FUZZ.target.com -w wordlist.txt -mode dns,http,https
```

### Input Mode
```bash
# Cluster bomb (all combinations)
ffuf -u http://target.com/FUZZ/FUZ2Z -w wordlist1.txt -w wordlist2.txt -mode clusterbomb

# Pitchfork (parallel with same line number)
ffuf -u http://target.com/FUZZ/FUZ2Z -w wordlist1.txt -w wordlist2.txt -mode pitchfork

# Sniper (single position)
ffuf -u http://target.com/FUZZ -w wordlist.txt -mode sniper
```

### Proxy Support
```bash
# Use HTTP proxy
ffuf -u http://target.com/FUZZ -w wordlist.txt -x http://proxy:8080

# Use SOCKS proxy
ffuf -u http://target.com/FUZZ -w wordlist.txt -x socks5://proxy:1080

# With authentication
ffuf -u http://target.com/FUZZ -w wordlist.txt -x http://user:pass@proxy:8080
```

### Authentication
```bash
# Basic authentication
ffuf -u http://target.com/FUZZ -w wordlist.txt -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ="

# Bearer token
ffuf -u http://target.com/api/FUZZ -w wordlist.txt -H "Authorization: Bearer TOKEN"

# Session cookies
ffuf -u http://target.com/FUZZ -w wordlist.txt -H "Cookie: session=SESSION_ID"
```

## Security Considerations

### Legal & Ethical
- **Only test systems you own or have explicit permission to test**
- Respect robots.txt
- Don't test production systems without authorization
- Obtain written permission before testing
- Follow responsible disclosure

### Rate Limiting
- Don't overload target systems
- Use reasonable rate limits
- Monitor target system health
- Stop if causing issues

### Data Protection
- Don't store sensitive data from responses
- Handle credentials securely
- Clean up after testing
- Use encrypted storage for results

## Common Vulnerabilities Found

### Information Disclosure
- Directory listings
- Source code exposure
- Debug pages
- Configuration files
- Backup files

### Injection Vulnerabilities
- SQL injection
- XSS (Cross-Site Scripting)
- Command injection
- LDAP injection
- XML external entities

### Authentication Issues
- Weak credentials
- Default credentials
- Credential stuffing
- Session fixation
- Insecure direct object references

### Authorization Issues
- Missing access controls
- Privilege escalation
- Horizontal/vertical access
- Forceful browsing

### API Vulnerabilities
- Excessive data exposure
- Mass assignment
- Security misconfiguration
- Broken object level authorization
- Broken user authentication

## Best Practices

### Before Fuzzing
- Obtain proper authorization
- Define scope clearly
- Set up monitoring
- Prepare wordlists
- Configure filters appropriately

### During Fuzzing
- Start with non-intrusive tests
- Monitor target system
- Adjust rate based on response
- Document findings
- Take screenshots of vulnerabilities

### After Fuzzing
- Analyze results thoroughly
- Validate findings manually
- Document vulnerabilities
- Create remediation plan
- Report responsibly

## Integration with Other Tools

### With Burp Suite
```bash
# Send ffuf results to Burp
ffuf -u http://target.com/FUZZ -w wordlist.txt -proxy http://127.0.0.1:8080
```

### With OWASP ZAP
```bash
# Use ZAP as proxy
ffuf -u http://target.com/FUZZ -w wordlist.txt -x http://127.0.0.1:8080
```

### With Nuclei
```bash
# Use ffuf to find endpoints, then scan with Nuclei
ffuf -u http://target.com/FUZZ -w wordlist.txt | nuclei -t ~/
```

### With Wayback Machine
```bash
# Get URLs from Wayback, fuzz with ffuf
cat urls.txt | waybackurls | ffuf -u FUZZ -mode clusterbomb
```

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- ffuf GitHub: https://github.com/ffuf/ffuf
- ffuf Documentation: https://github.com/ffuf/ffuf/blob/master/v2/cmd/ffuf/main.go
- SecLists: https://github.com/danielmiessler/SecLists

## Integration with Other Skills
- **Defense-in-Depth Hardening**: For fixing vulnerabilities found by fuzzing
- **Systematic Debugging**: For analyzing security issues
- **Webapp Testing via Playwright**: For functional testing of discovered endpoints
