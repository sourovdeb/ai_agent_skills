# Language-Specific Vulnerability Patterns

## JavaScript / TypeScript

### Dangerous Functions
| Function | Risk | Safe Alternative |
|----------|------|-----------------|
| `eval()` | Code injection | `JSON.parse()`, specific parsers |
| `new Function()` | Code injection | Avoid; use specific logic |
| `child_process.exec()` | Command injection | `execFile()` with array args |
| `child_process.spawn()` with `shell: true` | Command injection | `spawn()` without shell, or `execFile()` |
| `dangerouslySetInnerHTML` | XSS | Use text content, or sanitize with DOMPurify |
| `innerHTML =` | XSS | `textContent`, or sanitize |
| `document.write()` | XSS | DOM manipulation APIs |
| `setTimeout(string)` | Code injection | `setTimeout(fn, ms)` with function |
| `JSON.parse()` on untrusted data | Prototype pollution | Validate schema after parsing |
| `Object.assign(target, userInput)` | Prototype pollution | Filter keys, use `Object.create(null)` |

### Framework-Specific
**React:**
- `dangerouslySetInnerHTML` → XSS
- `href={userInput}` → `javascript:` URL injection
- Missing `rel="noopener noreferrer"` on `target="_blank"`

**Next.js:**
- `getServerSideProps` returning sensitive data to client
- API routes without auth checks
- `dangerouslySetInnerHTML` in `_document.js`

**Express:**
- Missing `helmet()` middleware
- `req.body` used without validation
- `res.send(userInput)` without escaping
- Static file serving with path traversal risk

**Node.js:**
- `fs.readFile(userPath)` → path traversal
- `require(userInput)` → code injection
- Prototype pollution via `__proto__` in JSON

---

## Python

### Dangerous Functions
| Function | Risk | Safe Alternative |
|----------|------|-----------------|
| `eval()` | Code injection | `ast.literal_eval()`, specific parsers |
| `exec()` | Code injection | Avoid |
| `pickle.loads()` | Code execution | `json.loads()`, `msgpack` |
| `os.system()` | Command injection | `subprocess.run([cmd, arg], shell=False)` |
| `subprocess.call(shell=True)` | Command injection | `shell=False` with list args |
| `yaml.load()` | Code execution | `yaml.safe_load()` |
| `input()` in Python 2 | Code execution | Use `raw_input()` (Python 2) |
| `jinja2.Template(string)` | SSTI | Use `autoescape=True` |

### Framework-Specific
**Django:**
- `mark_safe()` on user input → XSS
- `raw()` SQL queries → SQL injection
- Missing `CSRF` middleware
- `DEBUG = True` in production

**Flask:**
- `render_template_string(userInput)` → SSTI
- Missing input validation
- Session secret key hardcoded

**FastAPI:**
- Missing dependency injection for auth
- `response_model` excluding sensitive fields
- No rate limiting on auth endpoints

---

## Java

### Dangerous Patterns
| Pattern | Risk | Safe Alternative |
|---------|------|-----------------|
| `Runtime.exec(string)` | Command injection | `ProcessBuilder` with list args |
| `ObjectInputStream.readObject()` | Deserialization RCE | Use JSON, validate classes |
| String concatenation in SQL | SQL injection | `PreparedStatement` |
| `MessageDigest.getInstance("MD5")` | Weak hash | SHA-256 or stronger |
| `MessageDigest.getInstance("SHA-1")` | Weak hash | SHA-256 or stronger |
| XML parser without XXE protection | XXE attack | Disable external entities |
| `new Random()` for tokens | Predictable | `SecureRandom` |

### Framework-Specific
**Spring Boot:**
- `@RequestMapping` without auth on sensitive endpoints
- SpEL injection in `@Value` with user input
- Missing CSRF protection
- Actuator endpoints exposed

---

## Go

### Dangerous Patterns
| Pattern | Risk | Safe Alternative |
|---------|------|-----------------|
| `os/exec.Command(name, userArg)` | Command injection | Validate/allowlist args |
| `template.HTML(userInput)` | XSS | `template.HTMLEscapeString()` |
| `html/template` with `template.HTML()` | XSS | Use auto-escaping |
| String concatenation in SQL | SQL injection | `database/sql` with placeholders |
| `math/rand` for tokens | Predictable | `crypto/rand` |
| `json.Unmarshal` into `interface{}` | Type confusion | Use concrete types |

---

## PHP

### Dangerous Functions
| Function | Risk | Safe Alternative |
|----------|------|-----------------|
| `eval()` | Code injection | Avoid |
| `system()`, `exec()`, `shell_exec()` | Command injection | `escapeshellarg()` + allowlist |
| `passthru()`, `proc_open()` | Command injection | Validate input strictly |
| `unserialize()` | Object injection | `json_decode()` |
| `include($userInput)` | LFI/RFI | Allowlist of files |
| `file_get_contents($userUrl)` | SSRF | Validate URL, allowlist hosts |
| String concatenation in SQL | SQL injection | PDO prepared statements |
| `md5()`, `sha1()` for passwords | Weak hash | `password_hash()` |

---

## Ruby

### Dangerous Patterns
| Pattern | Risk | Safe Alternative |
|---------|------|-----------------|
| `eval()` | Code injection | Avoid |
| `system()`, backticks, `%x()` | Command injection | Use array form, validate input |
| `Marshal.load()` | Code execution | `JSON.parse()` |
| `YAML.load()` | Code execution | `YAML.safe_load()` |
| String interpolation in SQL | SQL injection | ActiveRecord parameterization |
| `render inline: userInput` | SSTI/XSS | Use templates with auto-escaping |

### Framework-Specific
**Rails:**
- `raw()` or `html_safe()` on user input → XSS
- `params` used directly in queries → SQL injection
- Missing `protect_from_forgery`
- Mass assignment without `strong_parameters`

---

## Rust

### Dangerous Patterns
| Pattern | Risk | Safe Alternative |
|---------|------|-----------------|
| `std::process::Command` with user input | Command injection | Validate args strictly |
| `unsafe` blocks without justification | Memory safety violation | Document safety invariants |
| Integer overflow (release mode wraps) | Logic bugs | Use `checked_*`, `saturating_*`, or `wrapping_*` explicitly |
| `transmute()` | Type confusion | Use safe conversions |
| Deserialization without validation | Various | Validate after deserialization |

---

## C/C++

### Dangerous Patterns
| Pattern | Risk | Safe Alternative |
|---------|------|-----------------|
| `strcpy()`, `strcat()`, `sprintf()` | Buffer overflow | `strncpy()`, `snprintf()`, or C++ `std::string` |
| `system()` | Command injection | `execve()` with array args |
| `gets()` | Buffer overflow | `fgets()` |
| Manual memory management | Use-after-free, leaks | RAII, smart pointers |
| Format string vulnerabilities | Information disclosure | Always use format specifiers |

---

## Quick Reference: Dangerous → Safe

| Dangerous | Safe |
|-----------|------|
| `eval(userInput)` | Never use with user input |
| `exec("cmd " + userInput)` | `execFile("cmd", [validatedArg])` |
| `"SELECT * FROM t WHERE id=" + id` | `"SELECT * FROM t WHERE id=?", [id]` |
| `innerHTML = userInput` | `textContent = userInput` |
| `pickle.loads(data)` | `json.loads(data)` |
| `md5(password)` | `bcrypt.hash(password, 12)` |
| `Math.random()` for tokens | `crypto.randomBytes(32)` |
| `YAML.load(data)` | `YAML.safe_load(data)` |
| `unserialize(data)` | `json_decode(data)` |
