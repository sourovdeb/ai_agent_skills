# Health & Productivity Tools for Bipolar and Depression

This guide focuses on reducing cognitive load — every system here is designed to work even on your lowest-energy days.

---

## The Core Problem (and Solution)

Bipolar disorder creates irregular energy cycles. The system needs to work on **both** ends:
- **High energy days:** You write 2,000 words. The system queues them all and drips them out over two weeks.
- **Low energy days:** You write 50 words. The system is still there waiting. Nothing breaks.

**The principle:** Never rely on today's energy to publish today's post. Always write ahead. Always queue.

---

## Tracking Your Health (Automation-Friendly Apps)

### eMoods Bipolar Mood Tracker
- **Platform:** Android and iOS — free
- **Website:** emoodtracker.com
- **Why this one:** Specifically designed for bipolar. Tracks elevated mood, depressed mood, anxiety, irritability, sleep hours, and medication.
- **Key feature:** Monthly PDF report you can show your psychiatrist
- **Automation:** Sends you a daily reminder at a set time. Takes 90 seconds to complete.

### Bearable Health Journal  
- **Platform:** iOS and Android — free with premium option
- **Why this one:** You can track symptoms, energy, activities, sleep, medication, diet in one place and see correlations ("I sleep badly before high-energy phases")
- **Key feature:** Graphing — see patterns over months

### Daylio (For Very Low Energy)
- **Platform:** iOS and Android — free
- **Why this one:** On a bad day, you just tap icons. No writing required. 10 seconds.
- **Use it for:** The days when eMoods feels like too much

---

## Reducing Decision Fatigue

Decision fatigue is a real problem with both bipolar and depression. Every decision costs energy you don't have. The solution is to automate or eliminate decisions.

### Writing Decisions to Eliminate

| Decision | Solution |
|----------|----------|
| What to write today | Create a 30-topic list on a good day. On a bad day, just pick the next one. |
| Which category | Let the Apps Script auto-guess from title keywords |
| What tags to use | Same — auto-generated |
| When to publish | Set schedule once. Never think about it again. |
| What format to use | Create one template. Always use it. |

### Your Writing Template (ELT Blog)

Save this as `drafts/TEMPLATE_ELT_POST.md` and copy it for every new post:

```markdown
# [TITLE: Day X – Topic Name]

## Introduction
[2 sentences: what this post is about and why it matters to ELT students]

## What is [Topic]?
[Definition + 1 example]

## Why It Matters for Language Learners
[2-3 practical reasons]

## Practical Exercise
[One exercise the reader can do today]

## Common Mistakes
[2-3 mistakes students make]

## Summary
[3 bullet points summarising the post]

<!-- metadata -->
Category: [ELT Masterclass / Grammar / Listening / Speaking]
Tags: [tag1, tag2, tag3]
Meta: [One sentence, 155 chars max]
```

With this template, you only fill in the blanks. No blank page paralysis.

---

## The No-Zero Days System

The rule: **every day, do at least one thing that moves your writing forward.**

On a good day: write 500 words.  
On a neutral day: write 200 words.  
On a bad day: write one sentence — a title, an idea, anything.  
On the worst day: open the file. That counts.

**Never two zeros in a row.** Missing one day is fine. Missing two days starts a habit of avoidance.

To implement this in your system:
- Keep a simple checklist in Google Sheets — one row per day, one column: "Did something? Y/N"
- The Apps Script can flag any 2-day gap and send you a reminder email

---

## Body Doubling for Writing

Body doubling means working alongside another person (in person or online). It is proven to help people with ADHD, bipolar, and depression focus.

**Focusmate (focusmate.com)**
- Free: 3 sessions/week
- Book a 25 or 50 minute session with a stranger
- You both show up on video, state your goal ("write 500 words"), work silently, check in at the end
- The social accountability makes it much easier to start

**Virtual Coworking Discord servers**
- Search Discord for "study with me" or "body doubling"
- Join a voice channel and work alongside others

---

## Medication and Sleep Tracking Integration

Many mood episodes are preceded by sleep disruption. Tracking sleep is one of the most useful early-warning systems for bipolar.

**Free sleep tracking without a wearable:**
- Open eMoods every morning → log your sleep hours (takes 30 seconds)
- After 30 days, you will see your patterns

**If you have a phone:**
- Android: Sleep as Android (free tier) — analyses sleep automatically
- iPhone: Built-in Health app → Sleep

**Connect to your writing system:**  
In your Google Sheet queue, add a column H: `Energy_Level` (1-5).  
Every morning, rate your energy. Over time you will see which energy levels correspond to which post quality. On high-energy days, write complex posts. On low-energy days, use your template for simple posts.

---

## Crisis Support Links (Official)

| Resource | URL | Who it helps |
|----------|-----|-------------|
| International Bipolar Foundation | ibpf.org | Bipolar education, peer support |
| NIMH Bipolar Disorder | nimh.nih.gov/health/topics/bipolar-disorder | Evidence-based information |
| WHO Mental Health | who.int/mental_health | Global resources |
| Mind UK | mind.org.uk | UK-based mental health support |
| SANE Australia | sane.org | For those outside UK/US |
| PubMed | pubmed.ncbi.nlm.nih.gov | Search your medication name + "bipolar" for research |
| eMoods emergency planning | emoodtracker.com/resources | Create a personalised crisis plan |

---

## The Productivity Stack (Low Cost)

This is the minimum viable setup:

1. **eMoods** — daily health tracking (free)
2. **Daylio** — backup tracker for very bad days (free)
3. **Focusmate** — body doubling for writing sessions (free 3/week)
4. **Google Sheets Queue** — post scheduling (free)
5. **Apps Script** — auto-publishing (free)
6. **Mistral Le Chat Canvas** — writing assistant (free)
7. **f.lux** — evening blue light reduction (free)

Total monthly cost: **£0**
