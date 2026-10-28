---
schema_version: "1.1"
name: not-a-lecture-request
description: Negative control. Tests that the skill does not turn a direct answer into lecture notes.
tags: [negative-control, trigger]
plugins: ["../.."]
runs: 1
expected_outcome: Answer directly without the lecture-notes template.
max_turns: 4
timeout_seconds: 120
---

What is 15% of 80? Just give me the answer, no explanation.
