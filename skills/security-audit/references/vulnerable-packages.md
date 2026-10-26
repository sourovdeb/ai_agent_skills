# Vulnerable Packages Watchlist

Common packages with frequent CVEs. Always check current versions against CVE databases.

## Node.js / npm

| Package | Common Issues | Notes |
|---------|-------------|-------|
| `lodash` | Prototype pollution (CVE-2019-10744, CVE-2020-8203) | Update to >= 4.17.21 |
| `axios` | SSRF (CVE-2021-3749, CVE-2023-45857) | Update to >= 0.21.1 / 1.6.0 |
| `jsonwebtoken` | Algorithm confusion, weak verification | Update to >= 9.0.0 |
| `node-fetch` | Various SSRF, info disclosure | Consider native `fetch` (Node 18+) |
| `moment` | ReDoS, path traversal (CVE-2022-31129) | Consider `date-fns` or native `Intl` |
| `request` | Deprecated, multiple CVEs | Migrate to `axios` or native `fetch` |
| `xmldom` / `@xmldom/xmldom` | XXE, prototype pollution | Update to latest |
| `ejs` | RCE via template injection (CVE-2022-29078) | Update to >= 3.1.7 |
| `minimist` | Prototype pollution (CVE-2021-44906) | Update to >= 1.2.6 |
| `node-serialize` | RCE (CVE-2017-5941) | Do not use |
| `immer` | Prototype pollution (CVE-2022-24757, older versions) | Update to >= 9.0.6 |
| `tar` | Path traversal (CVE-2021-32804, etc.) | Update to >= 6.1.11 |
| `ws` | DoS (CVE-2024-37890) | Update to >= 8.17.1 |
| `validator` | ReDoS, URL validation bypass | Update to >= 13.7.0 |
| `immer` | Prototype pollution | Update to latest |
| `immer` | Prototype pollution | Update to latest |

## Python / pip

| Package | Common Issues | Notes |
|---------|-------------|-------|
| `PyYAML` | Code execution via `yaml.load()` | Use `yaml.safe_load()`, update to >= 5.1 |
| `requests` | CVE-2018-18074 (credential leak), CVE-2023-32681 | Update to >= 2.31.0 |
| `pillow` / `PIL` | Multiple buffer overflows, DoS | Keep updated |
| `django` | SQL injection, XSS, open redirect (various CVEs) | Keep updated, follow security releases |
| `flask` | Session cookie issues, debug mode | Disable debug in production |
| `lxml` | XXE, billion laughs | Disable entity processing |
| `cryptography` | Various | Keep updated |
| `pyjwt` | Algorithm confusion, key confusion | Update to >= 2.4.0 |
| `urllib3` | CVE-2021-33503 (ReDoS), CVE-2023-43804 | Update to >= 1.26.17 / 2.0.7 |
| `tornado` | Open redirect, header injection, DoS | Update to >= 6.3.2 |
| `aiohttp` | Various request smuggling, CRLF injection | Keep updated |
| `jinja2` | SSTI (CVE-2020-28493, CVE-2024-22195) | Update to >= 3.1.3, use autoescape |
| `setuptools` | Various | Keep updated |

## Java / Maven

| Package | Common Issues | Notes |
|---------|-------------|-------|
| `log4j` / `log4j-core` | Log4Shell RCE (CVE-2021-44228) | Update to >= 2.17.1 immediately |
| `jackson-databind` | Deserialization RCE (multiple CVEs) | Update to latest, disable default typing |
| `spring-core` / `spring-framework` | Various SpEL, RCE | Keep updated |
| `spring-security` | Various auth bypass | Keep updated |
| `commons-collections` | Deserialization RCE (CVE-2015-7501) | Avoid or update |
| `commons-text` | String interpolation RCE (CVE-2022-42889) | Update to >= 1.10.0 |
| `snakeyaml` | Code execution (CVE-2022-1471) | Update to >= 2.0 |
| `xstream` | RCE via deserialization (CVE-2021-39139, etc.) | Update to >= 1.4.19, use allowlist |
| `apache-struts` | Multiple RCE | Keep updated |
| `guava` | Various | Keep updated |

## Ruby / Gems

| Package | Common Issues | Notes |
|---------|-------------|-------|
| `nokogiri` | XXE, command injection (CVE-2019-5477, etc.) | Keep updated, use `libxml2` >= 2.9.10 |
| `rails` | Multiple (SQL injection, XSS, etc.) | Follow security releases |
| `actionpack` | Various | Keep updated |
| `activerecord` | SQL injection | Keep updated |
| `loofah` | XSS (CVE-2019-15587, CVE-2022-23514) | Update to >= 2.19.1 |
| `rack` | Various (DoS, info disclosure) | Keep updated |

## Go

| Package | Common Issues | Notes |
|---------|-------------|-------|
| `golang.org/x/crypto` | Various | Keep updated |
| `golang.org/x/net` | HTTP/2 DoS, header injection | Keep updated |
| `golang.org/x/text` | Various | Keep updated |
| `github.com/dgrijalva/jwt-go` | Algorithm confusion (CVE-2020-26160) | Migrate to `golang-jwt/jwt` |

## How to Check

Always run the appropriate audit tool:
```bash
npm audit          # Node.js
pip-audit          # Python
cargo audit        # Rust
govulncheck ./...  # Go
bundle audit       # Ruby
mvn org.owasp:dependency-check-maven:check  # Java
```

## Response to Vulnerable Dependency

1. Check if the vulnerable code path is actually used
2. Update to a patched version
3. If no patch available, apply workarounds or replace the dependency
4. Add the package to your watchlist for future updates
