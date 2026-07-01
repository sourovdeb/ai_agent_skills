---
name: "pypict-combinatorial-qa"
description: "Load this skill when you need to generate complex pairwise and combinatorial test matrices automatically for structural QA engineering."
---
# Pypict Combinatorial QA

Generates complex pairwise and combinatorial test matrices automatically. Ideal for structural QA engineering where hand-authoring hundreds of cases is inefficient.

## Natural Triggers
- "generate test combinations"
- "pairwise testing"
- "combinatorial testing"
- "test matrix"
- "test cases generation"
- "QA automation"
- "test coverage"
- "parameter combinations"
- "test data generation"

## Core Concepts

### Pairwise Testing
Instead of testing all possible combinations (which grows exponentially), pairwise testing ensures that every pair of parameter values is tested together at least once. This dramatically reduces the number of test cases while maintaining high fault detection.

### N-wise Testing
Generalization of pairwise testing where combinations of N parameters are covered:
- **Pairwise (2-wise)**: Every pair of parameters
- **3-wise**: Every triplet of parameters
- **N-wise**: Every combination of N parameters

### Full Combinatorial Testing
Testing all possible combinations. Only feasible for small parameter spaces.

## When to Use

### Use Pairwise/Pypict When:
- System has many configuration options
- Testing all combinations is impractical
- You need to find interaction bugs
- Manual test case creation is time-consuming
- You want to maximize fault detection with minimal tests

### Use Full Combinatorial When:
- Small number of parameters (3-4)
- Small number of values per parameter (2-3)
- Critical systems where 100% coverage is required
- Safety-critical applications

## Input Format

### Parameters File (CSV or JSON)

**CSV Format:**
```csv
Parameter,Value1,Value2,Value3
OS,Windows,Linux,Mac
Browser,Chrome,Firefox,Safari,Edge
Resolution,1920x1080,1366x768,1280x720
```

**JSON Format:**
```json
{
  "OS": ["Windows", "Linux", "Mac"],
  "Browser": ["Chrome", "Firefox", "Safari", "Edge"],
  "Resolution": ["1920x1080", "1366x768", "1280x720"]
}
```

### Constraints
Some parameter combinations may be invalid or impossible:
```json
{
  "constraints": [
    {"OS": "Mac", "Browser": "Edge", "valid": false},
    {"OS": "Linux", "Browser": "Safari", "valid": false}
  ]
}
```

## Generation Commands

### Using Pypict
```bash
# Install pypict
pip install pypict

# Generate pairwise test cases
pypict pairwise parameters.csv -o test_cases.csv

# Generate 3-wise test cases
pypict 3wise parameters.csv -o test_cases.csv

# Generate with constraints
pypict pairwise parameters.csv constraints.csv -o test_cases.csv
```

### Using ACTS (Microsoft)
```bash
# Download ACTS
# Generate test cases
acts.exe parameters.xml /generate /output:test_cases.xml
```

### Using Python (Manual)
```python
from itertools import product

# Full combinatorial
parameters = {
    'OS': ['Windows', 'Linux', 'Mac'],
    'Browser': ['Chrome', 'Firefox', 'Safari']
}

all_combinations = list(product(*parameters.values()))
```

## Output Examples

### Pairwise Test Cases (CSV)
```csv
TestCaseID,OS,Browser,Resolution
1,Windows,Chrome,1920x1080
2,Windows,Firefox,1366x768
3,Windows,Safari,1280x720
4,Windows,Edge,1920x1080
5,Linux,Chrome,1366x768
6,Linux,Firefox,1280x720
7,Linux,Safari,1920x1080
8,Linux,Edge,1366x768
9,Mac,Chrome,1280x720
10,Mac,Firefox,1920x1080
11,Mac,Safari,1366x768
12,Mac,Edge,1280x720
```

### Test Case with Metadata
```json
{
  "test_cases": [
    {
      "id": 1,
      "parameters": {
        "OS": "Windows",
        "Browser": "Chrome",
        "Resolution": "1920x1080"
      },
      "coverage": [
        ["OS", "Browser"],
        ["OS", "Resolution"],
        ["Browser", "Resolution"]
      ]
    }
  ]
}
```

## Real-World Examples

### Example 1: Web Application Testing
**Parameters:**
- OS: Windows, macOS, Linux
- Browser: Chrome, Firefox, Safari, Edge
- Screen Size: Desktop, Tablet, Mobile
- User Type: Admin, Editor, Viewer
- Language: English, French, Spanish

**Pairwise Result:** ~20 test cases instead of 3×4×3×3×3 = 324

### Example 2: Mobile App Testing
**Parameters:**
- Device: iPhone, iPad, Android Phone, Android Tablet
- OS Version: iOS 15, iOS 16, Android 11, Android 12, Android 13
- Network: WiFi, 4G, 5G, Offline
- Orientation: Portrait, Landscape

**Pairwise Result:** ~15 test cases instead of 4×5×4×2 = 160

### Example 3: API Testing
**Parameters:**
- HTTP Method: GET, POST, PUT, DELETE, PATCH
- Authentication: None, Basic, Bearer, OAuth
- Data Format: JSON, XML, Form
- Response Type: Success, Error, Empty

**3-wise Result:** ~30 test cases instead of 5×4×3×3 = 180

## Advanced Features

### Weighted Pairwise
Prioritize certain parameter pairs:
```json
{
  "weights": {
    ["OS", "Browser"]: 10,
    ["Browser", "Resolution"]: 5,
    ["OS", "Resolution"]: 1
  }
}
```

### Coverage Metrics
Calculate coverage percentage:
- Parameter coverage: Each value appears at least once
- Pair coverage: Each pair appears at least once
- N-wise coverage: Each N-tuple appears at least once

### Test Case Prioritization
Order test cases by:
- Likelihood of finding bugs
- Criticality of parameters
- Historical defect data
- Risk assessment

### Test Case Reduction
Remove redundant test cases while maintaining coverage:
```bash
pypict reduce existing_cases.csv -o optimized_cases.csv
```

## Integration with Testing Frameworks

### Selenium
```python
import csv
from selenium import webdriver

with open('test_cases.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        driver = webdriver.Chrome()
        # Configure based on row parameters
        # Run test
        driver.quit()
```

### pytest
```python
import pytest

@pytest.mark.parametrize("os,browser,resolution", [
    ("Windows", "Chrome", "1920x1080"),
    ("Windows", "Firefox", "1366x768"),
    # ... more test cases
])
def test_application(os, browser, resolution):
    # Setup
    # Test
    # Teardown
```

### JUnit
```java
@RunWith(Parameterized.class)
public class CombinatorialTest {
    @Parameters
    public static Collection<Object[]> testCases() {
        return Arrays.asList(new Object[][] {
            {"Windows", "Chrome", "1920x1080"},
            {"Windows", "Firefox", "1366x768"},
            // ... more test cases
        });
    }

    @Test
    public void testApplication(String os, String browser, String resolution) {
        // Test logic
    }
}
```

## Quality Metrics

### Coverage Analysis
- **Parameter Coverage**: % of parameter values covered
- **Pair Coverage**: % of parameter pairs covered
- **N-wise Coverage**: % of N-tuples covered

### Fault Detection Rate
- Historical data on bugs found by combinatorial testing
- Comparison with random testing
- ROI calculation

### Test Suite Efficiency
- Number of test cases
- Time to generate
- Time to execute
- Defects found per test case

## Best Practices

### Parameter Selection
- Include all critical parameters
- Limit to 5-10 parameters for pairwise
- Group related parameters
- Avoid redundant parameters

### Value Selection
- Include common values
- Include edge cases
- Include boundary values
- Limit to 3-10 values per parameter

### Constraint Definition
- Define invalid combinations
- Handle impossible scenarios
- Consider dependencies between parameters
- Update constraints as system evolves

### Test Case Management
- Store generated test cases in version control
- Document parameter meanings
- Track coverage over time
- Update when parameters change

## Tools Comparison

| Tool | Algorithm | Strengths | Weaknesses |
|------|-----------|-----------|------------|
| Pypict | IPOG-F | Fast, Python-based | Limited to pairwise |
| ACTS | Multiple | Microsoft-backed, flexible | Windows-only |
| PICT | Microsoft | Industry standard | No longer maintained |
| Jenny | Genetic | Optimizes for coverage | Slower |
| AllPairs | Simple | Easy to use | Limited features |

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- Pypict: https://pypi.org/project/pypict/
- ACTS: https://www.microsoft.com/en-us/download/details.aspx?id=19831
- PICT: https://github.com/microsoft/pict

## Integration with Other Skills
- **Webapp Testing via Playwright**: For executing combinatorial tests
- **Test-Driven Development**: For generating tests from combinatorial data
- **Systematic Debugging**: For analyzing test failures
