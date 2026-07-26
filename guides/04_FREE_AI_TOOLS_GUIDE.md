# Free AI Tools for WordPress Publishing: Complete Guide

## The Big Picture: You Can Automate for Free

You do NOT need to pay for AI to automate your WordPress publishing. Here is the full landscape of free options.

---

## 1. DeepSeek (Free Web + Cheap API)

**Website:** app.deepseek.com  
**Cost:** Free web interface, API from $0.14/million tokens  
**Best for:** Writing blog posts, SEO descriptions, auto-tagging

DeepSeek's free web chat is the best free option for quality. Type your topic, get a complete structured blog post in seconds.

**Prompt to use:**
```
Write a 500-word ELT blog post about [topic].
Give me:
1. A title
2. The full HTML content (use <h2> and <p> tags)
3. 5 tags (comma-separated)
4. A category (ELT Masterclass, Grammar, Listening, Speaking, etc.)
5. A 155-character meta description
Format as JSON.
```

---

## 2. Mistral Le Chat (Free, Fast, "Vibe Mode")

**Website:** chat.mistral.ai  
**Cost:** Completely free  
**Best for:** Quick drafts, brainstorming, editing existing content

Mistral's Le Chat has a **Canvas mode** (their version of "vibe mode") where the AI writes directly into a document you can edit side-by-side. This is ideal when your energy is low — the AI writes, you adjust a few words.

**How to use Canvas mode:**
1. Go to chat.mistral.ai
2. Start a new chat
3. Click the **Canvas** icon (grid of squares)
4. Type: `Write a 500-word blog post about [topic] for ELT teachers`
5. The post appears in the canvas on the right — edit directly
6. Copy-paste the final result into WordPress or your Google Sheet queue

**Mistral for batch tagging (free API):**
Mistral API has a free tier with 1 request/second, 500K tokens/month.
Get a free key at console.mistral.ai — enough for ~800 auto-tag operations per month.

---

## 3. Google Gemini (Free)

**Website:** gemini.google.com  
**Cost:** Free (Gemini 1.5 Flash)  
**Best for:** Long content, summarizing, drafting from notes

Gemini integrates directly with Google Docs and Google Drive. You can:
- Open Google Docs → click the **Gemini** sidebar
- Paste your rough notes
- Ask it to expand them into a full blog post
- Copy the result to your WordPress queue sheet

**Gemini Extensions for automation:**
In Gemini settings, enable **Google Workspace** extension. Then ask:
`"Look at my Google Sheet called WordPress Queue and fill in the Tags column for all empty rows based on the Title column."`

---

## 4. ChatGPT Free Tier (GPT-4o mini)

**Website:** chatgpt.com  
**Cost:** Free (GPT-4o mini), limited GPT-4o  
**Best for:** Generating structured content, editing, SEO help

The free tier now uses **GPT-4o mini** which is very capable for blog writing. Limitations: no image generation, limited memory.

**Best free workflow:**
1. Write your rough 200-word notes in Google Docs
2. Paste into ChatGPT: `Expand these notes into a 500-word ELT blog post with proper HTML formatting`
3. Ask follow-up: `Now give me 5 SEO tags and a 155-character meta description`
4. Copy both into your Google Sheet
5. The Apps Script publishes it automatically

---

## 5. Groq (Fastest Free AI)

**Website:** console.groq.com  
**Cost:** Free tier: 6,000 tokens/minute, 500K tokens/day  
**Best for:** Quick content generation, fastest responses

Groq runs open-source models (Llama 3, Mixtral) at extraordinary speed — responses in under 1 second. This is ideal for batch processing.

**Free API key:** Sign up at console.groq.com → API Keys → Create  
**Models available free:** `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`

**Python example with Groq (free):**
```python
from groq import Groq
import json, os

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def generate_post(topic):
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{
            'role': 'user',
            'content': f'Write a WordPress ELT post about "{topic}". Return JSON: {{"title":"...","content":"HTML...","tags":[],"category":"...","meta_description":"..."}}'
        }],
        response_format={'type': 'json_object'}
    )
    return json.loads(resp.choices[0].message.content)
```

**Install:** `pip install groq`

---

## 6. Ollama (100% Free, Runs Locally)

**Website:** ollama.com  
**Cost:** Completely free forever, runs on your computer  
**Best for:** Privacy-conscious use, no internet dependency, unlimited usage

**Setup (one time):**
```bash
# Install Ollama (Linux/Mac)
curl -fsSL https://ollama.com/install.sh | sh

# Download a model (do once)
ollama pull mistral  # 4GB, good quality
# OR
ollama pull llama3.2  # 2GB, faster

# Run
ollama serve  # keeps running in background
```

Once running, WP AI Studio connects to it automatically at `http://localhost:11434`.

**Best models for blog writing (free):**
- `mistral` — best quality/size balance
- `llama3.2` — fastest, uses less RAM
- `phi3` — good for structured output, very lightweight

---

## 7. Perplexity AI (Free Research)

**Website:** perplexity.ai  
**Cost:** Free (limited Pro searches)  
**Best for:** Research-backed blog posts with citations

Perplexity searches the web AND summarizes. Use it to:
1. Research your ELT topic with up-to-date sources
2. Ask: `What are the latest research findings on listening comprehension in L2 acquisition?`
3. Get a researched summary with citations
4. Use that as the basis for your blog post

---

## Remote Publishing Without Any Coding

### Method A: Google Sheets + Apps Script (already in Guide 03)
Fill the sheet, script runs automatically. Zero code after setup.

### Method B: Zapier Free Tier
- 100 free tasks/month
- Connect: Google Sheets → WordPress
- When you add a row to your sheet → Zapier creates a draft in WordPress
- Setup at zapier.com — no code, visual interface

### Method C: Make.com (was Integromat) — Free Tier
- 1,000 operations/month free
- More powerful than Zapier
- Connect: Google Sheets → HTTP request to your WordPress plugin
- Visual flow builder

### Method D: n8n (Self-Hosted, Free Forever)
- Run on your own server (even a $5/month VPS)
- No usage limits
- GitHub: github.com/n8n-io/n8n
- Install: `docker run -p 5678:5678 n8nio/n8n`

---

## The "Lowest Energy" Free Workflow

For days when you have very low energy:

1. Open **Mistral Le Chat Canvas** (chat.mistral.ai)
2. Type three words: your topic (e.g., `past perfect tense`)
3. Mistral writes a full post in the canvas
4. Skim it, change one or two words if needed
5. Copy-paste the title and content into your **Google Sheet** (column A and B)
6. Set column E to `queued`
7. Close everything

The Apps Script trigger will find it within the hour and publish it as a draft to WordPress. Done. Total time: 5 minutes. Zero code.
