---
name: branded-cv-letter-design
description: >
  Reusable design system for professional CVs and motivation letters in PDF format.
  Use when the user asks to create, rebuild, or restyle a CV or motivation letter for
  the French/European market and wants something visually persuasive (not plain text).
  Two-column CV layout with navy sidebar + gold accents, letterhead with credentials bar.
  Outputs HTML → PDF via wkhtmltopdf. Designed for fast scanning by recruiters/partners.
---

# Branded CV + Motivation Letter Design Skill

## When to use
- User wants a CV or motivation letter that "looks professional" / "convinces partners"
- User dislikes plain DOCX-style output
- User targets French/EU market (A4, formal salutation)
- User wants key credentials scannable in seconds

## Design system

**Palette (variant A — corporate):**
- Primary navy: `#1B3A5C`
- Accent gold: `#C9A560`
- Background tint: `#F4F2EE`
- Body text: `#1a1a1a`

**Palette (variant B — aviation/premium):**
- Primary navy: `#0B2545`
- Accent gold: `#D4AF37`
- Background tint: `#F8F6F0`

**Typography:** Helvetica/Arial, 10.5pt body, 11-12pt headers, 22-24pt name
**Page:** A4, zero outer margin (layout handles padding internally)
**Tools:** `wkhtmltopdf --page-size A4 --margin-top 0 --margin-bottom 0 --margin-left 0 --margin-right 0 --encoding utf-8 --enable-local-file-access --disable-smart-shrinking`

## CV layout (two-column)

```
┌─────────────┬──────────────────────────────┐
│  SIDEBAR    │  MAIN                        │
│  75mm wide  │  flex                        │
│  navy bg    │  white bg                    │
│  white text │  dark text                   │
│             │                              │
│  • Name H1  │  • Title bar (gold border)   │
│  • Tagline  │  • Profil (justified)        │
│  • Contact  │  • Experience (entries)      │
│  • Langues  │  • Formation                 │
│  • Skills   │  • Footer note (tinted box)  │
│  • Certifs  │                              │
│  • Funding  │                              │
└─────────────┴──────────────────────────────┘
```

Each experience entry:
- Header row: role (bold) ⟷ date (gold)
- Org line (italic grey)
- Bullets with colored square/arrow markers
- Bold lead-ins ("Leadership :", "Communication :", etc.) for skimmability

## Letter layout (single column)

```
┌──────────────────────────────────────────┐
│  HEADER BAND (navy, gold bottom border)  │
│  Name + tagline  |  Tél/Email/Lieu       │
├──────────────────────────────────────────┤
│  CREDENTIALS BAR (tinted bg)             │
│  4 stats side-by-side, BIG numbers       │
├──────────────────────────────────────────┤
│  Date (right-aligned)                    │
│  Madame, Monsieur,                       │
│  3-4 justified paragraphs                │
│  Optional modules box (tinted, bordered) │
│  Accent line                             │
│  Closing formula                         │
│  Signature block (name bold + contact)   │
└──────────────────────────────────────────┘
```

## Key rules
- **Credentials bar** is the persuasion device — 4 stats max, each with BIG value + small caps label
- **Bold lead-ins** in bullets ("Leadership :", "Relations clients :") create scan anchors
- **Gold square/arrow bullets** instead of black dots
- **Justified body text** in letters (formal French style)
- **Right-aligned date** before salutation
- **Accent line** (30mm gold) before closing formula
- **Footer note box** at end of CV with single highlight statement (tinted bg, gold left border)

## Process

1. Build 4 HTML files: `cv1.html`, `letter1.html`, `cv2.html`, `letter2.html` (or as many as needed)
2. Convert each: `wkhtmltopdf <opts> input.html /mnt/user-data/outputs/<NUMBERED_NAME>.pdf`
3. Always preview at least one with `pdftoppm -jpeg -r 100` before presenting
4. Numbered prefix in filename = display order in `present_files`

## Filename convention
- `01_LETTRE_MOTIVATION_<CONTEXT>_<YEAR>.pdf`
- `02_CV_SOUROV_DEB_<MARKET>_<YEAR>.pdf`
- `03_LETTRE_MOTIVATION_<OTHER>_<YEAR>.pdf`
- `04_CV_SOUROV_DEB_<SPECIALTY>_<YEAR>.pdf`

## Accuracy notes
- **CELTA representation:** "Cambridge CELTA (2026)" + "Cours complété, 120 heures supervisées, travaux écrits validés" — never claim certification was awarded
- **Languages:** Anglais natif/C2, Français C1, Bengali natif, Hindi courant

## Reusable templates
HTML source files: `cv1.html`, `cv2.html`, `letter1.html`, `letter2.html`.
Copy and adapt the `<style>` block and structural divs for new variants.
