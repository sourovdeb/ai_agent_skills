---
name: "tapestry-knowledge-graphs"
description: "Load this skill when you need to ingest large document dumps and structure them into interconnected, navigable knowledge graphs or wiki format."
---
# Tapestry Knowledge Graphs

Ingests large document dumps (e.g., hundreds of pages of API specs or manuals) and structures them into an interconnected, navigable knowledge graph or wiki format.

## Natural Triggers
- "create knowledge graph"
- "structure these documents"
- "build a wiki"
- "connect these concepts"
- "organize documentation"
- "map relationships"
- "navigable knowledge"
- "interconnected docs"
- "semantic indexing"
- "document network"

## Core Capabilities

### Document Ingestion
- Process large PDFs
- Parse Markdown files
- Extract from documentation sites
- Handle API specifications
- Process technical manuals
- Ingest research papers

### Knowledge Extraction
- Identify key concepts
- Extract entities and relationships
- Detect themes and topics
- Recognize patterns
- Extract metadata
- Identify cross-references

### Graph Construction
- Build node-link diagrams
- Create hierarchical structures
- Establish relationship types
- Define connection strengths
- Generate visual representations

### Navigation & Query
- Full-text search
- Concept-based search
- Relationship traversal
- Path finding
- Context-aware suggestions

## Workflow

### Step 1: Document Collection
- Gather all relevant documents
- Organize by source and type
- Remove duplicates
- Validate file formats
- Extract metadata

### Step 2: Preprocessing
- Clean text (remove boilerplate)
- Normalize formatting
- Extract structure (headings, lists)
- Identify code blocks
- Extract tables and figures

### Step 3: Concept Extraction
- Identify named entities
- Extract key terms
- Detect definitions
- Find examples
- Identify relationships

### Step 4: Relationship Mapping
- Connect related concepts
- Define relationship types:
  - "is a" (inheritance)
  - "has a" (composition)
  - "uses" (dependency)
  - "requires" (prerequisite)
  - "extends" (specialization)
  - "related to" (association)
- Weight relationships by relevance

### Step 5: Graph Construction
- Create nodes for concepts
- Create edges for relationships
- Add properties to nodes and edges
- Build hierarchical structures
- Create multiple views/perspectives

### Step 6: Validation
- Review extracted concepts
- Validate relationships
- Check for missing connections
- Resolve ambiguities
- Merge duplicates

### Step 7: Visualization & Navigation
- Generate interactive graphs
- Create wiki-style navigation
- Build search interfaces
- Enable filtering and faceting
- Provide context-aware suggestions

## Graph Types

### Concept Graph
- Nodes: Concepts, ideas, topics
- Edges: Semantic relationships
- Use: Understanding domain knowledge

### Dependency Graph
- Nodes: Components, modules, services
- Edges: Dependencies, requirements
- Use: Architecture analysis

### Flow Graph
- Nodes: Steps, processes, states
- Edges: Transitions, flows
- Use: Workflow analysis

### Hierarchy Graph
- Nodes: Categories, types
- Edges: Parent-child relationships
- Use: Taxonomy, classification

### Network Graph
- Nodes: Entities (people, orgs, systems)
- Edges: Connections, interactions
- Use: Social network analysis

## Output Formats

### Wiki Format
- Hierarchical page structure
- Cross-linked pages
- Navigation menus
- Search functionality
- Table of contents

### Graph Database
- Nodes with properties
- Relationships with types
- Query language support
- Indexes for performance

### Interactive Visualization
- Force-directed layouts
- Zoom and pan
- Tooltips and details
- Filtering and highlighting
- Export options

### Structured Data
- JSON-LD
- RDF
- CSV/TSV
- GraphML
- DOT format

## Use Cases

### API Documentation
- Ingest OpenAPI/Swagger specs
- Connect endpoints to data models
- Map authentication flows
- Visualize API architecture

### Technical Manuals
- Structure user guides
- Connect troubleshooting steps
- Map configuration options
- Link to API references

### Research Papers
- Extract key findings
- Connect citations
- Map methodology to results
- Visualize research landscape

### Codebases
- Extract architecture
- Map dependencies
- Connect modules to features
- Visualize call graphs

### Domain Knowledge
- Build domain ontologies
- Connect business concepts
- Map processes and workflows
- Create training materials

## Tools & Technologies

### Parsing
- PDF: pdf-lib, pdf.js, PyPDF2
- Markdown: marked, remark
- HTML: jsdom, cheerio
- Code: tree-sitter, Babel

### NLP
- NER: spaCy, Stanford NER
- Keyphrase extraction: RAKE, TextRank
- Embeddings: Sentence-BERT, Universal Sentence Encoder
- Topic modeling: LDA, BERTopic

### Graph
- Graph databases: Neo4j, ArangoDB
- Libraries: D3.js, vis.js, Cytoscape.js
- Frameworks: NetworkX, igraph

### Storage
- Vector databases: Pinecone, Weaviate
- Document stores: Elasticsearch, Meilisearch
- File systems: Local, S3, GitHub

## Quality Metrics

### Graph Quality
- **Density**: Number of connections per node
- **Coherence**: Related concepts are connected
- **Completeness**: Important concepts are included
- **Accuracy**: Relationships are correct
- **Usability**: Easy to navigate and understand

### Extraction Quality
- **Precision**: Extracted concepts are relevant
- **Recall**: Important concepts are extracted
- **F1 Score**: Balance of precision and recall
- **Diversity**: Range of concepts covered

## Best Practices

### Document Preparation
- Use clean, well-structured documents
- Include table of contents
- Use consistent terminology
- Define acronyms
- Include examples

### Graph Design
- Keep it focused (one domain per graph)
- Limit node types (5-10 max)
- Limit relationship types (10-15 max)
- Balance depth and breadth
- Optimize for navigation

### Validation
- Review with domain experts
- Test with real queries
- Iterate based on feedback
- Update regularly

## References
- Repository: https://github.com/travisvn/awesome-claude-skills
- Also found in: https://github.com/BehiSecc/awesome-claude-skills

## Integration with Other Skills
- **YouTube & Article Extractor**: For ingesting multimedia content
- **Content Research Writer**: For generating documentation from graphs
- **Superpowers**: For complex knowledge management workflows
