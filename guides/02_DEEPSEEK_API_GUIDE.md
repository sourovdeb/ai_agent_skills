# DeepSeek API: The Affordable Alternative for WordPress Automation

## Why DeepSeek Over Other AI APIs?

| Model | Price per 1M input tokens | Price per 1M output tokens | Notes |
|-------|--------------------------|---------------------------|-------|
| **deepseek-chat (V3)** | **$0.14** | **$0.28** | Best for content writing |
| deepseek-reasoner (R1) | $0.55 | $2.19 | Best for complex reasoning |
| gpt-4o-mini | $0.15 | $0.60 | OpenAI cheapest |
| gemini-1.5-flash | $0.075 | $0.30 | Google cheapest |
| claude-haiku-4-5 | $0.80 | $4.00 | Anthropic cheapest |
| claude-sonnet-4 | $3.00 | $15.00 | Anthropic standard |

**DeepSeek V3 is ~21x cheaper than Sonnet** for the same task quality on blog writing.

For 1,000 blog posts (~600 words each), DeepSeek costs approximately **$0.17**. Anthropic Sonnet would cost **$3.60**.

---

## Step 1: Get Your DeepSeek API Key (5 minutes)

1. Go to **platform.deepseek.com**
2. Click **Sign Up** — use your email
3. Verify your email
4. In the left sidebar click **API Keys**
5. Click **Create new API key**
6. Give it a name: `wordpress-automation`
7. Copy the key — it starts with `sk-` — paste it somewhere safe immediately (it won't show again)
8. Add **$5 credit** minimum — this covers ~35 million words of content

---

## Step 2: Free Web Interface (No API Key Needed)

For casual use, go to **app.deepseek.com** — completely free, no registration required for basic use.

Use it to:
- Draft your ELT blog posts
- Generate 5 tags for any topic
- Write SEO meta descriptions
- Suggest post categories

Then copy-paste the result into your WordPress editor or Google Sheet queue.

**Prompt template to paste into the DeepSeek chat:**
```
Write a 500-word WordPress blog post about: [YOUR TOPIC]

Return ONLY this JSON:
{
  "title": "...",
  "content": "[HTML with h2, p, ul tags]",
  "category": "ELT Masterclass",
  "tags": ["tag1", "tag2", "tag3"],
  "meta_description": "Under 160 chars"
}
```

---

## Step 3: Use DeepSeek in WP AI Studio (VS Code)

1. Open VS Code → click the **WP AI Studio** icon in the sidebar
2. Click **Settings** tab
3. Under **AI Provider** select **DeepSeek (recommended — cheapest)**
4. Paste your `sk-...` key in **DeepSeek API Key**
5. Click **Save All Settings**
6. Click **ping** to test your WordPress connection
7. Go to **Generate** tab → type a topic → click **Generate with AI**

---

## Step 4: Python Script Using DeepSeek API

Save as `scripts/deepseek_wp_publisher.py`:

```python
import os
import requests
import json

DEEPSEEK_KEY = os.environ.get('DEEPSEEK_API_KEY', 'sk-YOUR-KEY-HERE')
WP_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post'
WP_KEY = os.environ.get('WP_PLUGIN_KEY', 'your-plugin-key')

def ask_deepseek(topic):
    resp = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
        json={
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': 'You are a WordPress content writer. Return ONLY valid JSON, no markdown.'},
                {'role': 'user', 'content': f'''Write a 500-word WordPress post about: "{topic}"
Return JSON: {{"title":"...","content":"HTML...","category":"ELT Masterclass","tags":["t1","t2","t3"],"meta_description":"..."}}'''}
            ]
        }
    )
    raw = resp.json()['choices'][0]['message']['content']
    raw = raw.strip().lstrip('```json').rstrip('```').strip()
    return json.loads(raw)

def publish_to_wordpress(post_data, status='draft'):
    post_data['status'] = status
    resp = requests.post(WP_URL, json=post_data, headers={'X-Sourov-Key': WP_KEY})
    return resp.json()

if __name__ == '__main__':
    topic = input('Enter post topic: ')
    print('Generating with DeepSeek...')
    post = ask_deepseek(topic)
    print(f'Title: {post["title"]}')
    confirm = input('Publish as draft? (y/n): ')
    if confirm.lower() == 'y':
        result = publish_to_wordpress(post)
        print(f'Done! Post ID: {result.get("post_id")}')
```

**Run it:**
```bash
export DEEPSEEK_API_KEY=sk-your-key
export WP_PLUGIN_KEY=your-plugin-key
python3 scripts/deepseek_wp_publisher.py
```

---

## Step 5: Google Apps Script + DeepSeek (No Local Setup)

Add this function to your existing sheet_publisher.gs to enrich posts with AI:

```javascript
function enrichWithDeepSeek(title, content) {
  const DEEPSEEK_KEY = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + DEEPSEEK_KEY, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [{
        role: 'user',
        content: `Given this blog title: "${title}" and content: "${content.substring(0,200)}..."
Return JSON only: {"tags":["t1","t2","t3"],"meta_description":"under 160 chars","category":"ELT Masterclass"}`
      }]
    }),
    muteHttpExceptions: true
  });
  const raw = JSON.parse(response.getContentText()).choices[0].message.content
    .replace(/```json/g,'').replace(/```/g,'').trim();
  return JSON.parse(raw);
}

// Store your key: File > Project properties > Script properties > Add DEEPSEEK_KEY
```

---

## Cost Calculator

| Task | Tokens used | Cost |
|------|------------|------|
| 1 blog post (600 words) | ~800 input + 700 output | $0.0003 |
| 30 posts/month | ~45,000 tokens | $0.009 |
| 1 year of daily posts | ~540,000 tokens | $0.11 |
| Auto-tagging 100 posts | ~50,000 tokens | $0.01 |

**Your entire year of blogging with AI costs less than a coffee.**
