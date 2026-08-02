# Implementation Manual — Step by Step

**Everything you click, in order.** The first four sections clear the AdSense blockers; the rest are quality fixes; the last section is the application itself.

**Before you start:** Log in at `[your-site]/wp-admin`. Keep the drafted files open in another tab.

---

## § 1 — Fix the mis-filed photography post (5 min) 🔴 BLOCKER

1. WP → **Posts** → **All Posts** → search "Photograp".
2. Hover → **Quick Edit**.
3. **Title:** change to `Photography Basics: 50 Essential Terms Every Photographer Should Know`.
4. **Do NOT change the Slug/URL.**
5. **Categories:** untick **English Teaching**, tick **Photography & Software**.
6. Click **Update**.

---

## § 2 — Publish the Privacy Policy (10 min) 🔴 BLOCKER

**Source file:** `privacy-policy.md`

1. WP → **Pages** → **Add New**.
2. Title: `Privacy Policy`. Permalink: `/privacy-policy/`.
3. Paste the body of `privacy-policy.md`. Fill the four `[[...]]` placeholders.
4. **Publish**.
5. Add to footer: WP → **Appearance** → **Menus** (or Widgets → Footer).

---

## § 3 — Install the cookie consent banner (10 min) 🔴 BLOCKER

Required because La Réunion is EU territory → GDPR applies.

1. WP → **Plugins** → **Add New** → search **CookieYes** (free) → Install → Activate.
2. Setup wizard: Region EU/GDPR, **prior consent** (block cookies until accepted).
3. Categories: Essential, Analytics, Advertisement.
4. Link banner's Privacy Policy button to your new page.
5. Add "Cookie Settings" link to footer.
6. Test in incognito: banner should appear on first visit.

---

## § 4 — Homepage meta title + description (10 min)

**Source file:** `homepage-meta-tags.md`

1. Install Yoast SEO or Rank Math (free) if not present.
2. Yoast: **Yoast SEO** → **Settings** → **Search appearance** → **Homepage**.
   Rank Math: **Rank Math** → **Titles & Meta** → **Homepage**.
3. Paste chosen SEO Title + Meta Description.
4. If there's a Social tab, add OG title/description and upload a 1200×630 banner.

---

## § 5 — Add a Contact page to the nav (10 min) 🔴 BLOCKER

1. Install **WPForms Lite** or **Contact Form 7** (free). Activate.
2. Create a simple form (Name, Email, Message).
3. WP → **Pages** → **Add New** → title `Contact`. Embed the form. Publish.
4. WP → **Appearance** → **Menus** → add **Contact** to main navigation. Save.

---

## § 6 — Add the "why it's free" statement (5 min)

On your **About Me** page, add:
> *"Everything on this site is free to read. I keep it that way by running unobtrusive ads, which cover hosting and let me keep publishing without a paywall."*

---

## § 7 — Unique category descriptions (20 min)

**Source file:** `category-descriptions.md`

1. WP → **Posts** → **Categories**.
2. For each category: hover → **Edit** → paste matching description → **Update**.

---

## § 8 — Remove duplicate widgets (15 min)

1. WP → **Appearance** → **Widgets** — look for duplicate "Related Posts" widget. Remove one.
2. If both remain: check theme settings for a built-in related posts toggle. Disable the duplicate.
3. Reload a post in incognito to confirm a single block + single nav.

---

## § 9 — Apply to Google AdSense (5 min) 🟢 LAST

**Only after §1–§5 are done and live.**

1. Go to **google.com/adsense** → sign in → Add your site.
2. Country: **France**.
3. Install **Site Kit by Google** plugin → connect AdSense → it places the code.
4. Submit for review. Review takes a few days to two weeks.
5. While waiting, keep publishing.

---

## § 10 — After approval: ad placement

- One **in-content** ad after the 2nd paragraph
- One **sidebar** ad
- One **after post content**, before the related-posts block
- **No ads** on lead-gen/Masterclass pages
- **Never** place ads next to buttons where a mis-click looks accidental

---

## Progress checklist

- [ ] §1 Photography post: title fixed + moved to correct category
- [ ] §2 Privacy Policy published + linked in footer
- [ ] §3 Cookie consent banner live (reject option works)
- [ ] §4 Homepage meta title + description set
- [ ] §5 Contact page created + in nav
- [ ] §6 "Why it's free" note on About page
- [ ] §7 Category descriptions filled
- [ ] §8 Duplicate widgets removed
- [ ] §9 AdSense application submitted
- [ ] §10 Ad placements configured after approval

---

*Source: sourovdeb/my_professional_documents docs/site-monetization/implementation-manual.md*
