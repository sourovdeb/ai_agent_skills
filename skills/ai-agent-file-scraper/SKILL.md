# SKILL: AI Agent — Project File Scraper & Information Extractor
## Version: 1.0 | Date: 29 May 2026
## Purpose: Enable an AI agent to autonomously search, extract, and synthesise information from all project files
---

## OVERVIEW

This skill enables an AI agent to:
1. Locate any piece of information across 88+ project files
2. Extract specific content (names, dates, evidence, quotes, data)
3. Cross-reference multiple documents
4. Answer questions from project context without external search
5. Generate summaries, timelines, comparisons from project files

---

## DIRECTORY MAP (Know Where Everything Is)

```
/mnt/project/          — 85 files (all project files, text + binary)
/mnt/user-data/outputs/ — 20+ files (session outputs, MD extractions)
/mnt/user-data/uploads/ — 3 files (user-uploaded originals)
/mnt/skills/           — All skill templates
```

### File Categories (for routing queries):

| Query Type | Go To |
|---|---|
| Medical diagnoses, treatment, medications | Official_Medical_Record.pdf, DEB_Sourov_courrier*.md |
| CELTA complaint evidence | MASTER_COMPLAINT_DOSSIER_FINAL.md, DOC_9*.pdf |
| Appeal report (Stage 1) | Stage_1_appeal_report__Sourov_Deb.md |
| Career / CV | CV_SOUROV_DEB_2026.md, CAREER_OPPORTUNITIES_CSV |
| Life story | TRANSCRIPT_SOUROV_DEB_LIFE_STORY.md |
| French authorities / regulatory | FRENCH_AUTHORITIES_COMPLETE_REGULATORY_MAP.md |
| Email templates | COMPLAINT_EMAILS_v3_DEFINITIVE.md, 03_EMAILS_FRENCH_AUTHORITIES.md |
| Automation scripts | AUTONOMOUS_CAMPAIGN_ENGINE_v4_1.gs, BATCH_SENDER_v2.gs |
| Organisations list | CAREER_OPPORTUNITIES_CSV_COMPREHENSIVE.csv |
| Research paper | JEFL_Paper_Comprehensive_v4.md |
| Disclosure/autoethnography | Disclosure_and_Adjustment_Autoethnography.md |
| Deep research findings | DEEP_RESEARCH_WARM_CONTACTS_OFFICIAL_LISTS.md |
| Session chat history | COMPLETE_CHAT_HISTORY_2026-05-29.md |

---

## AGENT WORKFLOW

### Step 1: Parse the Query

Identify:
- **Subject** (who/what is this about?)
- **Type** (fact? quote? date? list? comparison? document?)
- **Specificity** (precise reference vs. general theme?)

### Step 2: Route to File(s)

Use the directory map above. If uncertain, search these first:
1. MASTER_PROJECT_INDEX_2026-05-29.md (overview of everything)
2. COMPLETE_PROJECT_INDEX_ALL_FILES.md (full file list)
3. COMPLETE_CHAT_HISTORY_2026-05-29.md (session decisions)

### Step 3: Extract

```python
# For text files:
with open("/mnt/project/FILENAME.md", "r") as f:
    content = f.read()

# For CSVs:
import csv
with open("/mnt/project/CAREER_OPPORTUNITIES_CSV_COMPREHENSIVE.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# For JSON:
import json
with open("/mnt/project/authority_and_contacts_registry.json") as f:
    data = json.load(f)

# For PDFs (if not yet converted to MD):
from pypdf import PdfReader
reader = PdfReader("/mnt/user-data/uploads/FILE.pdf")
text = "".join(p.extract_text() for p in reader.pages)

# For ZIP-stored PDFs (CV, motivation, appeal report):
import zipfile
with zipfile.ZipFile("/mnt/project/CV_SOUROV_DEB_2026.pdf") as z:
    with z.open("1.txt") as f:
        text = f.read().decode("utf-8")
```

### Step 4: Cross-Reference

For queries requiring multiple documents:

```python
# Example: Find all mentions of "ADHD" across project files
import os, glob

query = "ADHD"
results = {}

for filepath in glob.glob("/mnt/project/*.md") + glob.glob("/mnt/user-data/outputs/*.md"):
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()
    if query.lower() in content.lower():
        # Find surrounding context (100 chars each side)
        idx = content.lower().find(query.lower())
        context = content[max(0,idx-100):idx+200]
        results[os.path.basename(filepath)] = context

for filename, snippet in results.items():
    print(f"\n=== {filename} ===\n{snippet}")
```

### Step 5: Synthesise

Return only relevant information. Format as:
- **Fact queries**: State fact + source file + date
- **List queries**: Bulleted list + source files
- **Date queries**: Chronological list + source files
- **Document queries**: Direct quote + source + page/section

---

## SEARCH PATTERNS (Reusable)

### Pattern 1: Find any keyword across all files

```python
import os, glob

def search_project(keyword, directories=None):
    if not directories:
        directories = ["/mnt/project/", "/mnt/user-data/outputs/", "/mnt/user-data/uploads/"]
    
    results = []
    extensions = [".md", ".txt", ".gs", ".json", ".csv"]
    
    for directory in directories:
        for ext in extensions:
            for filepath in glob.glob(f"{directory}*{ext}"):
                try:
                    with open(filepath, "r", errors="ignore") as f:
                        content = f.read()
                    if keyword.lower() in content.lower():
                        count = content.lower().count(keyword.lower())
                        results.append({
                            "file": os.path.basename(filepath),
                            "path": filepath,
                            "mentions": count
                        })
                except:
                    pass
    
    return sorted(results, key=lambda x: -x["mentions"])
```

### Pattern 2: Extract dated events from any document

```python
import re

def extract_dates(filepath):
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()
    
    # Match date patterns: DD/MM/YYYY, DD Month YYYY, YYYY-MM-DD
    patterns = [
        r'\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4}',
        r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}',
        r'\d{4}-\d{2}-\d{2}'
    ]
    
    dates = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        dates.extend(matches)
    
    return list(set(dates))
```

### Pattern 3: Extract names (people and organisations)

```python
def extract_entities(filepath):
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()
    
    # Look for capitalised names (crude but effective for this project)
    import re
    
    # People: Two or more capitalised words
    people = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][A-Z]+\b', content)
    
    # Organisations (all caps or Title Case with known keywords)
    orgs = re.findall(r'\b(?:ELT Hub|Cambridge|Ofqual|CSMRP|GRETA|CCI|AGEFIPH|MDPH|UPT)[^\n,\.]*', content)
    
    return {"people": list(set(people)), "organisations": list(set(orgs))}
```

### Pattern 4: Build timeline from all project files

```python
def build_project_timeline():
    """Extract all dated events across project files and sort chronologically"""
    import glob, re
    from datetime import datetime
    
    events = []
    
    for filepath in glob.glob("/mnt/project/*.md") + glob.glob("/mnt/user-data/outputs/*.md"):
        with open(filepath, "r", errors="ignore") as f:
            lines = f.readlines()
        
        for line in lines:
            # Look for lines with dates + context
            date_match = re.search(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}|\d{4}-\d{2}-\d{2})', line)
            if date_match and len(line.strip()) > 20:
                events.append({
                    "date_str": date_match.group(),
                    "event": line.strip()[:200],
                    "source": filepath.split("/")[-1]
                })
    
    return events
```

### Pattern 5: Answer specific questions

```python
def answer_from_project(question, max_results=5):
    """
    Given a question, search all project files and return relevant passages.
    Intended for agent use; agent then synthesises the answer.
    """
    # Extract key terms from question
    # (In production: use NLP; here, simple word extraction)
    stopwords = {"what","when","where","who","how","did","is","was","are","the","a","an","in","of","to","for","and","or"}
    keywords = [w for w in question.lower().split() if w not in stopwords and len(w) > 3]
    
    results = {}
    for keyword in keywords:
        found = search_project(keyword)
        for item in found[:3]:  # top 3 per keyword
            key = item["file"]
            if key not in results:
                results[key] = {"path": item["path"], "score": 0}
            results[key]["score"] += item["mentions"]
    
    # Sort by relevance score
    ranked = sorted(results.items(), key=lambda x: -x[1]["score"])
    
    # Extract relevant passages from top files
    passages = []
    for filename, info in ranked[:max_results]:
        with open(info["path"], "r", errors="ignore") as f:
            content = f.read()
        # Find most relevant 300-char passage
        best_idx = 0
        best_score = 0
        for kw in keywords:
            idx = content.lower().find(kw)
            if idx > 0:
                passage = content[max(0,idx-50):idx+300]
                passages.append({"source": filename, "passage": passage})
                break
    
    return passages
```

---

## AGENT PROMPT TEMPLATE

When deploying this skill as an API-powered agent:

```javascript
const systemPrompt = `
You are an AI agent with access to Sourov DEB's complete project files.
You can search, extract, and synthesise information from 88+ project files.

AVAILABLE INFORMATION:
- Medical records (diagnoses, medications, treatment plans)
- CELTA complaint evidence (appeal, policies, emails)
- Career documents (CV, motivation letter, 61 organisations)
- Life story transcript
- Research papers and analysis
- Automation tools and scripts
- Regulatory documents (French authorities, Ofqual)

SEARCH STRATEGY:
1. Route to correct file based on query type
2. Extract relevant passage
3. Cross-reference if needed
4. State source clearly
5. Answer only from documented evidence — no hypothesis

RESPONSE FORMAT:
- Fact: "[Finding]. Source: [filename], [date if available]"
- List: Bulleted list with source per item
- Document: Direct quote in quotation marks + source + context

NEVER invent information. If not found, say: "Not found in project files."
`;
```

---

## KNOWN LIMITATIONS

- ❌ Cannot read encrypted PDFs without password
- ❌ Cannot OCR scanned images (Stage 1 appeal images are readable via .txt files in ZIP)
- ⚠️ Large files (>1MB) may need chunked reading
- ⚠️ Binary DOCX files need python-docx library
- ✅ All .md, .txt, .gs, .csv, .json files readable directly

---

## REUSABILITY

Adapt this skill for:
- Any project with multiple documents (legal, medical, research)
- AI agents that need to answer from private knowledge base
- Automated report generation from document corpus
- Evidence compilation for legal/regulatory cases

---

## DEPENDENCIES

```bash
pip install pypdf pdfplumber --break-system-packages
# pdftotext: sudo apt-get install poppler-utils
# python-docx: pip install python-docx --break-system-packages
```

