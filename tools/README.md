# Tools

Reusable Python scripts, shell scripts, and utility programs.

## Python Utilities

| Script | Purpose |
|--------|----------|
| aggregate_benchmark.py | Aggregates and analyzes benchmark results |
| generate_report.py | Generates formatted reports from data |
| generate_review.py | Creates review summaries and feedback |
| gif-builder.py | Creates GIF animations from frames |
| gif_easing.py | Easing functions for smooth animations |
| improve_description.py | Enhances and refines text descriptions |
| frame_cmposer.py | Composes animation frames |
| package_skill.py | Packages skills for distribution |
| quick_validate.py | Quick validation of skill outputs |
| run_eval.py | Runs evaluation workflows |
| run_loop.py | Executes loop-based operations |
| utils.py | Shared utility functions |
| validators.py | Validation schemas and checkers |

## Shell Scripts

| Script | Purpose |
|--------|----------|
| bundle-artifact.sh | Bundles artifacts for packaging |
| init-artifact.sh | Initializes new artifacts |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Each script includes:
- Usage documentation at the top
- Configuration examples
- Integration examples with other tools

Example:
```python
from generate_report import generate_report
report = generate_report(data, format='markdown')
```

---
*Part of the ai_agent_skills repository*