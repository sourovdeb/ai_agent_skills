# Publishing Template for Investigative Psychology Micro-Blogs

## WordPress Publishing

### API Configuration
Endpoint: https://www.sourovdeb.com/wp-json/sourov/v1/ai-post
Authentication: Header X-Sourov-Key: [PROVIDED_KEY]

### Post Structure
- title: HEADLINE
- content: Full content with HTML formatting
- status: draft
- category: Philosophy & Mental Health (ID: 54)
- tags: Array of relevant tags
- meta_description: SEO description (155 chars max)
- seo_title: SEO-optimized title

### Category Mapping
- Psychology & Neuroscience: 1
- Marketing & Manipulation: 2
- Pharmaceutical Industry: 3
- Mental Health Treatment: 4
- Conflict of Interest: 5
- Investigative Reports: 6
- Source Verification: 7

## Ghost Publishing

### API Configuration
Admin API Endpoint: https://sourovdeb.ghost.io/ghost/api/v3/admin/
Content API Key: [stored in the personal API inventory skill — do not hardcode here]
Admin API Key: [stored in the personal API inventory skill — do not hardcode here]

### Post Structure
- title: HEADLINE
- html: Full HTML content
- status: draft
- tags: Array of tag objects with name property
- custom_excerpt: LEAD text

## Automated Publishing Workflow

1. Draft Creation: Format content according to templates
2. WordPress Posting: POST to REST API endpoint
3. Ghost Posting: POST to Admin API endpoint
4. Parallel Publishing: Post to both platforms simultaneously
5. Error Handling: Retry failed posts with exponential backoff
6. Logging: Record all publishing attempts with timestamps

## Content Formatting

### Markdown to HTML Conversion
- Headings: # -> <h1>, ## -> <h2>, etc.
- Paragraphs: Double line breaks
- Lists: Convert to <ul>/<ol> with <li> items
- Citations: Use <cite> tags or keep as plain text

### Tag Determination
Automatically extract tags from content:
- mental-health, neuroscience, bias, identity, programming
- marketing-tricks, marketing, corporate-research
- antidepressants, therapy, treatment, pharmaceutical
- conflict-of-interest, lobbying, trauma, empathy, intelligence
- brain-limits, hidden-sources, government-data

Always include: investigative