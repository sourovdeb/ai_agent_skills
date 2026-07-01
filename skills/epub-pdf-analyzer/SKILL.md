---
name: "epub-pdf-analyzer"
description: "Load this skill when you need to perform deep structural parsing, indexing, cross-referencing, and semantic querying of digital ebooks and whitepapers for academic research."
---
# EPUB & PDF Analyzer

Tailored primarily for academic researchers. Specialized in deep structural parsing, indexing, cross-referencing, and semantic querying of digital ebooks and whitepapers.

## Natural Triggers
- "analyze this PDF"
- "extract from ebook"
- "parse academic paper"
- "search whitepaper"
- "index document"
- "cross-reference"
- "semantic search"
- "literature review"
- "research extraction"

## Core Capabilities

### Document Parsing
- EPUB format parsing
- PDF text extraction
- Structural analysis
- Metadata extraction
- Content organization

### Indexing
- Full-text indexing
- Keyword extraction
- Concept indexing
- Entity recognition
- Citation indexing

### Cross-Referencing
- Citation network analysis
- Reference extraction
- Bibliography parsing
- Cross-document linking
- Similarity detection

### Semantic Querying
- Natural language queries
- Concept-based search
- Context-aware retrieval
- Semantic similarity
- Knowledge graph queries

## Supported Formats

### EPUB
- EPUB 2.0
- EPUB 3.0
- EPUB 3.1
- EPUB 3.2
- Fixed-layout EPUB
- Reflowable EPUB

### PDF
- Text-based PDFs
- Scanned PDFs (with OCR)
- Searchable PDFs
- PDF/A (Archival)
- PDF/X (Exchange)

### Other Formats
- MOBI
- AZW (Kindle)
- HTML
- Markdown
- Plain text

## Workflow

### Phase 1: Document Ingestion

#### Source Acquisition
- Upload files
- Fetch from URLs
- Import from reference managers
- Batch processing
- Incremental updates

#### Format Detection
```python
import magic

def detect_format(file_path):
    mime = magic.from_file(file_path, mime=True)
    if mime == 'application/epub+zip':
        return 'epub'
    elif mime == 'application/pdf':
        return 'pdf'
    elif mime == 'text/html':
        return 'html'
    # ... other formats
```

#### Parsing
```python
# EPUB parsing
from ebooklib import epub

book = epub.read_epub('book.epub')
for item in book.get_items():
    if item.get_type() == epub.ITEM_DOCUMENT:
        print(item.get_content())

# PDF parsing
import PyPDF2

with open('document.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        print(page.extract_text())
```

### Phase 2: Structural Analysis

#### Document Structure Extraction
- Table of contents
- Chapter/section hierarchy
- Headings and subheadings
- Paragraphs and sentences
- Lists and tables
- Figures and captions

#### Metadata Extraction
- Title
- Author(s)
- Publication date
- Publisher
- ISBN/ISSN
- DOI
- Keywords
- Abstract
- Language

#### Reference Extraction
- Citations (in-text)
- Bibliography/References
- Footnotes
- Endnotes
- Cross-references

### Phase 3: Indexing

#### Full-Text Index
- Tokenization
- Normalization
- Stop word removal
- Stemming/Lemmatization
- Inverted index creation

#### Semantic Index
- Named Entity Recognition (NER)
- Keyphrase extraction
- Concept extraction
- Topic modeling
- Embedding generation

#### Citation Index
- Citation parsing
- Reference normalization
- Author disambiguation
- Publication matching
- Citation network building

### Phase 4: Querying

#### Basic Search
```python
# Simple keyword search
def search(keyword):
    results = []
    for doc in documents:
        if keyword.lower() in doc.text.lower():
            results.append(doc)
    return results
```

#### Advanced Search
```python
# Boolean search
# Phrase search
# Proximity search
# Wildcard search
# Fuzzy search
```

#### Semantic Search
```python
# Vector similarity search
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode(query)

documents = [...]  # List of document embeddings
similarities = np.dot(documents, query_embedding)
top_results = np.argsort(similarities)[-10:][::-1]
```

#### Citation-Based Search
```python
# Find documents citing a specific paper
# Find papers cited by a document
# Find co-citation networks
# Find bibliographic coupling
```

## Use Cases

### Literature Review
- Upload multiple papers
- Extract key concepts
- Identify research gaps
- Find seminal works
- Generate literature review

### Systematic Review
- Define inclusion/exclusion criteria
- Screen documents
- Extract data
- Assess quality
- Synthesize findings

### Meta-Analysis
- Extract statistical data
- Pool results
- Calculate effect sizes
- Assess heterogeneity
- Generate forest plots

### Knowledge Discovery
- Identify emerging trends
- Detect research clusters
- Find influential authors
- Track citation networks
- Discover interdisciplinary connections

### Academic Writing Support
- Find relevant sources
- Generate citations
- Create annotated bibliographies
- Summarize key findings
- Identify research opportunities

## Output Formats

### Structured Data
```json
{
  "metadata": {
    "title": "Document Title",
    "authors": ["Author 1", "Author 2"],
    "date": "2023-01-01",
    "publisher": "Publisher",
    "doi": "10.xxxx/xxxx"
  },
  "structure": {
    "toc": [
      {"level": 1, "title": "Introduction", "page": 1},
      {"level": 2, "title": "Background", "page": 2}
    ],
    "sections": [...]
  },
  "content": {
    "text": "Full text...",
    "entities": [...],
    "concepts": [...]
  },
  "references": [
    {"citation": "(Smith, 2020)", "reference": "Smith, J. (2020). ..."}
  ]
}
```

### Knowledge Graph
```json
{
  "nodes": [
    {"id": "concept1", "type": "Concept", "name": "Machine Learning"},
    {"id": "paper1", "type": "Paper", "title": "A Survey of ML"}
  ],
  "edges": [
    {"source": "paper1", "target": "concept1", "type": "discusses"},
    {"source": "paper1", "target": "author1", "type": "written_by"}
  ]
}
```

### Search Results
```json
{
  "query": "machine learning applications",
  "results": [
    {
      "document": "paper1.pdf",
      "score": 0.95,
      "matches": [
        {"text": "Machine learning has many applications...", "page": 5}
      ]
    }
  ]
}
```

## Advanced Features

### Citation Network Analysis
- Co-citation analysis
- Bibliographic coupling
- Citation path analysis
- Author collaboration networks
- Temporal citation patterns

### Trend Analysis
- Keyword frequency over time
- Research topic evolution
- Author influence tracking
- Journal impact analysis
- Field growth patterns

### Quality Assessment
- Document quality scoring
- Peer review status detection
- Journal impact factor lookup
- Author h-index calculation
- Citation count analysis

### Comparison & Analysis
- Document similarity
- Plagiarism detection
- Redundancy identification
- Gap analysis
- Coverage assessment

## Tools & Libraries

### EPUB Processing
- ebooklib (Python)
- epub.js (JavaScript)
- Sigil (Desktop)
- Calibre (Desktop)

### PDF Processing
- PyPDF2 (Python)
- pdfminer.six (Python)
- PDF.js (JavaScript)
- Apache PDFBox (Java)
- iText (Java/.NET)

### OCR
- Tesseract
- EasyOCR
- PaddleOCR
- Amazon Textract
- Google Vision

### NLP
- spaCy
- NLTK
- HuggingFace Transformers
- Stanford NLP
- AllenNLP

### Indexing & Search
- Elasticsearch
- Solr
- Meilisearch
- Typesense
- Whoosh (Python)

## Quality Metrics

### Extraction Quality
- **Accuracy**: Correctly extracted information
- **Completeness**: All relevant information extracted
- **Precision**: Extracted information is relevant
- **Recall**: All relevant information is extracted

### Indexing Quality
- **Coverage**: All documents indexed
- **Freshness**: Index up to date
- **Performance**: Query response time
- **Relevance**: Search results are relevant

### Query Quality
- **Precision**: Proportion of relevant results
- **Recall**: Proportion of relevant documents retrieved
- **F1 Score**: Harmonic mean of precision and recall
- **User Satisfaction**: User ratings of results

## Best Practices

### For Researchers
- Organize documents by project
- Use consistent naming conventions
- Maintain metadata
- Backup regularly
- Share with collaborators

### For Librarians
- Curate collections
- Ensure quality
- Maintain metadata standards
- Provide access controls
- Track usage

### For Developers
- Use robust parsing libraries
- Handle edge cases
- Optimize performance
- Ensure data privacy
- Maintain security

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- EPUB Specification: https://www.w3.org/publishing/epub3/
- PDF Specification: https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf

## Integration with Other Skills
- **Tapestry Knowledge Graphs**: For creating knowledge graphs from analyzed documents
- **Content Research Writer**: For generating research from analyzed content
- **YouTube & Article Extractor**: For extracting content to analyze
- **Deep Research**: For conducting research using analyzed documents
