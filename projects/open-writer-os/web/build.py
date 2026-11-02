#!/usr/bin/env python3
"""Embed skills/*/SKILL.md into app/skills.js so the app also works from file://."""
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent
skills = {
    p.parent.name: p.read_text(encoding="utf-8")
    for p in sorted((root / "skills").glob("*/SKILL.md"))
}
out = root / "app" / "skills.js"
out.write_text(
    "const SKILLS=" + json.dumps(skills, ensure_ascii=False) + ";\n"
    "if(typeof module!=='undefined')module.exports=SKILLS;\n",
    encoding="utf-8",
)
print(f"embedded {len(skills)} skill(s) into {out.name}")
