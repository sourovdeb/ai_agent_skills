# SKILL_research_synthesis_pipeline

**Trigger phrases:** research synthesis pipeline, synthesize sources for blog post, YouTube script with citations, source-audited research, evidence-backed content creation, multi-source synthesis, deep research for writing

## Purpose

Provides a rigorous, token-efficient pipeline for turning raw research (web searches, page browses, X posts, PDFs) into polished, citation-rich content for blogs, research papers, or YouTube video scripts. Emphasizes source verification, conflict detection, explicit evidence tracking, and auditability to prevent hallucinations and support high-stakes topics (legal, regulatory, technical).

## When to Activate

- User requests a blog post, article, or briefing requiring depth and sources
- Creating YouTube script or video description with verifiable claims
- Research paper, whitepaper, or regulatory submission needing evidence chain
- Any synthesis task where traceability ("where did this fact come from?") is mandatory

## Core Workflow (Token-Efficient Order)

1. **Scope & Questions**: Define exact research questions, target format (blog/YouTube/paper), audience, length, and required rigor level.
2. **Parallel Multi-Source Research**: 
   - web_search for overviews and sources
   - browse_page with precise instructions for key pages
   - x_keyword_search or x_semantic_search for recent discussions
   - pdf_search / pdf_browse if documents attached
3. **Extraction & Triage**: Pull key facts, data, quotes with source tags (web:ID, post:ID). Flag contradictions, gaps, bias indicators.
4. **Synthesis Phase**: Structure output with proper heading hierarchy (H1 title, H2/H3 subsections). Use tables for comparisons/criteria/status (e.g. UPI-style match tables). Integrate inline citations via render component. Add KaTeX for technical content.
5. **Audit & Compliance Pass**: Self-review for unsupported claims. Run accuracy/compliance gate. Add Sources section with full links where possible.
6. **Delivery + Logging**: Provide final content + source log + confidence levels per section + recommended next steps table.

## Output Standards (Match Project Style)

- Tables for status, criteria match, next steps with Blocker? column
- Every factual claim traceable to cited source
- render_inline_citation used inline after relevant sentences
- Prioritized actions: strongest effective action first
- Uncertainty declaration for anything unconfirmed
- Cross-reference chat history or memory where relevant

## Integration Points

- Feeds into universal-upgrade for polishing drafts
- Pairs with investigative-writing-forensics-guidelines for legal/regulatory topics
- Outputs can be committed directly to GitHub or pushed to WordPress via deploy.php workflow
- Use with email campaign validator when research informs outreach content

## Prevention of Common Failures

- Never output synthesized claims without source IDs visible in reasoning
- Always declare uncertainty explicitly
- For politically or legally sensitive topics, add extra verification layer and present balanced perspectives
- Keep token footprint low: summarize long sources, quote only critical passages verbatim

## Example Trigger Response Structure

**Evidence Summary**  
**Root Cause / Key Findings** (with citations)  
**Prioritized Actions** (table)  
**Prevention Recommendations**  
**Uncertainty Declaration**