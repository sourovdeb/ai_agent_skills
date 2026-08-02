# WordPress SEO Guide for sourovdeb.com

How to write essays that rank on Google and get readers.

---

## Before Publishing (SEO Checklist)

### Title (Most Important)
- [x] Includes your main keyword
- [x] Under 60 characters (so it fits in Google)
- [x] Active voice ("5 Ways to..." not "Ways That Can Help...")
- [x] Specific and clear (not vague)

**Good:** "How Disability Shaped My Writing Career"  
**Bad:** "My Life" or "Thoughts on Writing"

### Meta Description (The 160-char Preview)
```yaml
description: "I discovered disability wasn't a barrier to writing—it became my unique voice. Here's how I built my platform while managing my condition."
```

- [x] Under 160 characters
- [x] Includes main keyword early
- [x] Answers a question or creates curiosity
- [x] No keyword stuffing

### Keywords/Tags
```yaml
tags: "disability, writing, career, chronic pain, accessibility"
focus_keyword: "disability writing"
```

- [x] 3-5 tags per essay
- [x] One main focus keyword
- [x] Related but not identical (long-tail keywords)
- [x] Natural language (as people search)

**Search people actually make:**
- "disability writing career"
- "chronic pain writing"
- "accessible writing tips"
- "disabled writer freelance"

Find these using AnswerThePublic.com (free).

### Content Structure
```markdown
# Main Title (includes keyword)

**First paragraph** — This is your 160-char preview.
Keyword should appear in first 100 words.

## Section 1: The Problem/Hook
## Section 2: Your Angle
## Section 3: Actionable Insight
## Conclusion: Call to Reflection

[Optional: Internal link to another essay]
```

- [x] Keyword in title + first 100 words + conclusion
- [x] Clear headings (H2, H3 hierarchy)
- [x] Short paragraphs (2-3 sentences)
- [x] 1-2 internal links (to other essays on your site)
- [x] Active voice > Passive voice

### Images (Boosts Engagement)
```markdown
![Alt text describing image](image-url)
```

- [x] Add featured image (optional but helps)
- [x] Alt text: "A disabled writer at desk working on laptop"
- [x] Size: 1200x675px (16:9 ratio)
- [x] JPG/PNG, < 100KB file size

**Where to find free images:**
- Unsplash.com
- Pexels.com
- Pixabay.com

### Readability
Use `tools/wp_publisher.py` which checks:
- [x] Sentence length (avg < 20 words)
- [x] Paragraph length (max 5 sentences)
- [x] Passive voice (flag percentage)
- [x] Adverb overuse
- [x] Complex jargon

**Or use:** Hemingway Editor (hemingwayapp.com)

---

## Publishing Command (With SEO)

```bash
python3 tools/wp_publisher.py \
  --file daily_essays/2026-06-02_disability_writing.md \
  --category Writing \
  --tags "disability,writing,career,chronic pain" \
  --publish
```

This automatically:
- Extracts SEO metadata from frontmatter
- Sets meta description under 160 chars
- Adds focus keyword to Yoast/RankMath
- Categorizes and tags post
- Optimizes for Google

---

## After Publishing (Post-Optimization)

### Google Search Console
1. Go to search.google.com/search-console
2. Select your site: sourovdeb.com
3. **Performance** tab → See:
   - Which keywords you're ranking for
   - Which essays get impressions
   - Click-through rate (CTR)

### Fix Issues:
- Ranking but low CTR? → Improve meta description
- Not ranking at all? → Better keywords, more backlinks
- 404 errors? → Fix broken internal links

---

## Backlinks (Get Other Sites to Link to You)

**Why:** Google sees backlinks as "votes of confidence"

### Where to Get Backlinks:
1. **Social media** — Share essays on LinkedIn, Twitter
2. **Guest posts** — Write for other blogs, link back
3. **Comments** — Comment on other blogs with link to relevant essay
4. **Collaborations** — Work with other writers (cross-link)
5. **Directories** — Add to writing directories (Medium, Dev.to)

---

## SEO Timeline

**Week 1-2 after publish:** No Google traffic expected; manual share on social  
**Week 3-4:** Start appearing for long-tail keywords (5-20 visits)  
**Month 2-3:** Ranking for main keyword (50-200 visits)  
**Month 4+:** Established ranking; consistent traffic

**Patience:** SEO is not fast. But it's free & compounding.

---

## Common SEO Mistakes (Avoid These)

- **Keyword stuffing** — use keyword naturally
- **Title too long** — keep under 60 chars
- **Generic tags** (`article, writing, life`) — use specific long-tail tags
- **No internal links** — link each essay to 1-2 related essays

---

## Pre-Publish Checklist

```markdown
Title:
- [ ] Includes main keyword
- [ ] < 60 characters
- [ ] Active voice
- [ ] Clear & specific

Description:
- [ ] < 160 characters
- [ ] Includes keyword
- [ ] Answers a question or creates curiosity

Content:
- [ ] Keyword in title, first 100 words, conclusion
- [ ] 500+ words
- [ ] Clear headings (H2, H3)
- [ ] 1-2 internal links

Tags:
- [ ] 3-5 specific tags
- [ ] One focus keyword

Finalization:
- [ ] Hemingway Editor: clear & simple
- [ ] Grammarly: no grammar errors
- [ ] Spellcheck: no typos
```

---

## Tools

| Tool | Purpose | Free? |
|------|---------|-------|
| Google Search Console | Monitor rankings | Yes |
| Google Analytics | Track visitors | Yes |
| AnswerThePublic | Find keywords | Free tier |
| Hemingway Editor | Readability | Yes (web) |
| Yoast SEO | WordPress plugin | Free version |

---

## Remember

> **Quality > Rankings**
>
> Write for humans first, search engines second.
> Good essays rank eventually.
> Bad essays never rank, no matter what.

Focus on: **authentic voice + useful content + consistency**

---

**Source:** `my_professional_documents/wordpress_integration/SEO_GUIDE.md`  
**Last Updated:** 2026-06-02
