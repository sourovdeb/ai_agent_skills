# Evaluation

Tools and frameworks for testing, validating, and evaluating skill outputs.

## Available Tools

| Tool | Purpose |
|------|----------|
| Eval Review | Interactive interface for manual evaluation and feedback |
| Evaluate expectations against an execution transcript | Compares execution logs against expected outcomes |

## Workflow

1. **Run your skill** - Execute an agent or skill
2. **Collect outputs** - Gather results and execution transcript
3. **Evaluate** - Use tools in this folder to validate
4. **Feedback** - Document findings and improvements
5. **Iterate** - Refine skill based on evaluation results

## Integration with Other Tools

- Use `validators.py` from `/tools` for automated validation
- Use `generate_review.py` to create detailed review documents
- Use agents in `/agents` to perform blind comparisons

## Best Practices

- Always compare against documented expectations
- Use multiple evaluators for objective results
- Document all feedback for improvement tracking
- Iterate based on evaluation results

---
*Part of the ai_agent_skills repository*