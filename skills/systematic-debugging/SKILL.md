---
name: "systematic-debugging"
description: "Load this skill when debugging issues. Prevents shallow fixes by enforcing step-by-step root-cause analysis based on telemetry, logs, and engineering principles."
---
# Systematic Debugging

Prevents Claude from offering shallow, unverified quick fixes. Mandates step-by-step root-cause analysis based on telemetry, log traces, and rigorous engineering principles.

## Natural Triggers
- debug this issue
- find the root cause
- systematic debugging
- analyze the error
- troubleshoot
- investigate the problem
- why is this failing
- deep dive
- diagnose
- log analysis

## Core Principles

### Root-Cause First
- MANDATORY: List 3 possible root causes before suggesting any fix
- No quick fixes without analysis
- No guessing - verify through investigation
- Every suggestion must be backed by evidence

### Evidence-Based Debugging
- Use logs, metrics, and telemetry
- Reproduce the issue consistently
- Isolate variables
- Test hypotheses systematically

## Debugging Workflow

### Step 1: Reproduce the Issue
- Identify exact steps to reproduce
- Document environment details
- Capture error messages
- Note frequency and patterns

### Step 2: Gather Data
- Collect relevant logs
- Gather metrics and telemetry
- Review recent changes
- Check system status
- Interview stakeholders

### Step 3: Analyze Patterns
- Identify common factors
- Look for correlations
- Compare with baseline
- Check for similar past issues
- Analyze timing and sequence

### Step 4: Formulate Hypotheses
- REQUIRED: List at least 3 possible root causes
- Rank by likelihood
- Define tests for each hypothesis
- Predict outcomes

### Step 5: Test Hypotheses
- Design experiments
- Run targeted tests
- Validate or eliminate hypotheses
- Document findings

### Step 6: Identify Root Cause
- Confirm the actual cause
- Validate with evidence
- Rule out other possibilities
- Document the root cause

### Step 7: Implement Fix
- Address root cause, not symptoms
- Write tests to prevent regression
- Implement minimal, targeted fix
- Validate the fix

### Step 8: Verify Resolution
- Confirm issue is resolved
- Test edge cases
- Monitor for regressions
- Update documentation

## Debugging Techniques

### Log Analysis
- Search for error patterns
- Check timestamps and sequences
- Look for anomalies
- Correlate across services
- Use log aggregation tools

### Metrics Analysis
- Check dashboards and graphs
- Look for spikes or drops
- Compare with historical data
- Identify outliers
- Analyze trends

### Code Review
- Inspect recent changes
- Check for common mistakes
- Review dependencies
- Validate assumptions
- Look for edge cases

### System Analysis
- Check resource usage
- Review configuration
- Validate infrastructure
- Test dependencies
- Verify integrations

### User Interview
- Gather reproduction steps
- Understand user behavior
- Identify environment differences
- Collect additional context

## Common Root Causes

### Code Issues
- Null pointer exceptions
- Race conditions
- Incorrect assumptions
- Missing validation
- Off-by-one errors
- Resource leaks
- Concurrency issues

### Configuration Issues
- Misconfigured settings
- Environment mismatches
- Missing dependencies
- Version conflicts
- Permission problems

### Infrastructure Issues
- Network problems
- Resource exhaustion
- Service outages
- Storage issues
- Performance bottlenecks

### Data Issues
- Corrupted data
- Inconsistent state
- Missing data
- Invalid data
- Data format problems

### Integration Issues
- API changes
- Contract violations
- Version incompatibilities
- Authentication failures
- Rate limiting

## Debugging Tools

### Logging
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARN, ERROR)
- Correlation IDs
- Request tracing

### Monitoring
- Metrics dashboards
- Alerting systems
- Health checks
- Performance monitoring

### Tracing
- Distributed tracing
- Request flow visualization
- Latency analysis
- Dependency mapping

### Testing
- Unit tests
- Integration tests
- End-to-end tests
- Property-based tests

## Documentation Standards

### Debug Report Template

Issue Summary
[Brief description]

Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Behavior
[What should happen]

Actual Behavior
[What actually happens]

Environment
- OS: [version]
- Runtime: [version]
- Dependencies: [versions]

Data Collected
- Logs: [links/attachments]
- Metrics: [screenshots/data]
- Traces: [links]

Root Cause Analysis
### Hypothesis 1: [Description]
- Evidence: [Supporting data]
- Test: [How to validate]
- Result: [Pass/Fail]

### Hypothesis 2: [Description]
- Evidence: [Supporting data]
- Test: [How to validate]
- Result: [Pass/Fail]

### Hypothesis 3: [Description]
- Evidence: [Supporting data]
- Test: [How to validate]
- Result: [Pass/Fail]

Root Cause
[Confirmed root cause with evidence]

Fix
[Description of fix]

Verification
[How the fix was validated]

## References
- Repository: https://github.com/obra/superpowers
- Debugging Guide: [Add relevant links]

## Integration with Other Skills
- Test-Driven Development: Write tests to prevent regression
- Superpowers: Use for complex debugging workflows
- Code Quality Collection: Ensure code meets standards after fix