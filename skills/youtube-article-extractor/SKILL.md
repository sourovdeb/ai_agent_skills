---
name: "youtube-article-extractor"
description: "Load this skill when you need to extract and summarize content from YouTube videos or web articles. Bypasses multimedia consumption by scraping transcripts and structural data."
---
# YouTube & Article Extractor

Bypasses extensive multimedia consumption by precisely scraping transcripts and structural data from web articles and YouTube videos for hyper-focused textual synthesis.

## Natural Triggers
- "summarize this video"
- "extract article content"
- "get transcript"
- "scrape webpage"
- "video to text"
- "article summary"
- "extract key points"
- "get main ideas"
- "text from video"
- "web content extraction"

## Core Capabilities

### YouTube Extraction
- Fetch video transcripts
- Extract closed captions
- Get video metadata
- Download subtitles
- Identify key moments
- Extract chapters

### Article Extraction
- Scrape web page content
- Extract main article text
- Remove boilerplate
- Preserve structure
- Extract images and media
- Get metadata

### Content Processing
- Clean extracted text
- Remove ads and noise
- Normalize formatting
- Extract key information
- Identify structure

### Summarization
- Generate concise summaries
- Extract key points
- Identify main themes
- Create structured outlines
- Highlight important quotes

## Supported Sources

### YouTube
- Public videos
- Age-restricted videos (with appropriate access)
- Live streams (transcripts when available)
- Shorts
- Playlists (batch processing)

### Web Articles
- News articles
- Blog posts
- Documentation pages
- Tutorials
- Research papers (when publicly accessible)
- Technical documentation

### Formats
- HTML pages
- PDF documents
- Markdown files
- Text files

## Workflow

### YouTube Video Processing

#### Step 1: URL Input
```
User provides: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

#### Step 2: Metadata Extraction
- Video title
- Channel name
- Upload date
- Duration
- View count
- Like/dislike counts
- Tags
- Description
- Thumbnail URL

#### Step 3: Transcript Extraction
- Fetch available transcripts
- Handle multiple languages
- Sync with video timing
- Clean and normalize text
- Remove speaker labels (if unwanted)

#### Step 4: Content Analysis
- Identify key topics
- Detect structure (intro, sections, conclusion)
- Extract important quotes
- Identify action items
- Detect sentiment

#### Step 5: Summarization
- Generate overall summary
- Create chapter-wise summaries
- Extract key takeaways
- Identify calls to action
- Highlight important moments

### Article Processing

#### Step 1: URL Input
```
User provides: https://example.com/article
```

#### Step 2: Page Fetching
- Download HTML content
- Handle redirects
- Respect robots.txt
- Manage rate limiting
- Handle authentication (if provided)

#### Step 3: Content Extraction
- Identify main content area
- Remove navigation, headers, footers
- Extract article title
- Get author information
- Extract publication date
- Preserve headings and structure
- Extract images and captions

#### Step 4: Cleaning
- Remove ads and promotional content
- Normalize whitespace
- Fix encoding issues
- Remove tracking elements
- Clean up formatting

#### Step 5: Analysis & Summarization
- Identify key points
- Extract quotes
- Create structured summary
- Identify main arguments
- Extract supporting evidence

## Output Formats

### Raw Text
- Plain text of transcript/article
- Preserved formatting
- With or without timestamps

### Structured Data
```json
{
  "title": "Video/Article Title",
  "source": "URL",
  "date": "Publication/Upload Date",
  "author": "Creator/Author",
  "summary": "Concise summary",
  "key_points": ["Point 1", "Point 2", "..."],
  "transcript": "Full text...",
  "metadata": { ... }
}
```

### Markdown
- Formatted for readability
- With headings and structure
- Code blocks preserved
- Links maintained

### CSV/Table
- For batch processing
- Structured columns
- Easy to import

### Knowledge Graph Input
- For Tapestry Knowledge Graphs
- Structured relationships
- Concept extraction

## Summarization Levels

### Level 1: Ultra-Concise (1-2 sentences)
- Main takeaway only
- For quick understanding

### Level 2: Key Points (5-10 bullet points)
- Main arguments
- Important facts
- Key decisions

### Level 3: Detailed Summary (Paragraphs)
- Comprehensive overview
- All major points
- Supporting details

### Level 4: Full Transcript/Article
- Complete text
- With structure
- All details

## Quality Standards

### Extraction Quality
- **Accuracy**: Extracted content matches source
- **Completeness**: All important content included
- **Cleanliness**: No ads, navigation, or boilerplate
- **Structure**: Headings and formatting preserved

### Summarization Quality
- **Relevance**: Focuses on important content
- **Conciseness**: Removes redundancy
- **Clarity**: Easy to understand
- **Objectivity**: No bias or interpretation (unless requested)

## Tools & Libraries

### YouTube
- youtube-transcript-api
- yt-dlp
- pytube
- YouTube Data API

### Web Scraping
- BeautifulSoup (Python)
- Cheerio (Node.js)
- Puppeteer (for JavaScript-heavy sites)
- Playwright
- Scrapy

### NLP
- NLTK
- spaCy
- Transformers (HuggingFace)
- Sumy (for summarization)

### Text Processing
- html2text
- readability-lxml
- trafilatura
- newspaper3k

## Rate Limiting & Ethics

### Respectful Scraping
- Check robots.txt
- Respect Crawl-delay
- Use appropriate User-Agent
- Don't overload servers
- Cache results when possible

### Legal Considerations
- Public content only
- Respect copyright
- Don't bypass paywalls
- Honor terms of service
- Attribute sources

### Privacy
- Don't extract personal data
- Anonymize when necessary
- Don't store sensitive information
- Comply with GDPR/CCPA

## Best Practices

### For Users
- Provide clear, direct URLs
- Specify desired output format
- Indicate summarization level
- Mention any specific sections of interest
- Request timestamped transcripts when needed

### For Developers
- Handle errors gracefully
- Provide clear error messages
- Respect rate limits
- Cache frequently accessed content
- Update extraction methods when sites change

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills

## Integration with Other Skills
- **Tapestry Knowledge Graphs**: For structuring extracted knowledge
- **Content Research Writer**: For creating research from extracted content
- **Superpowers**: For complex extraction workflows
