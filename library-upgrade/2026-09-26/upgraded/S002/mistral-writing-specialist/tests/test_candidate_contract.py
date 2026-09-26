from pathlib import Path
import json, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

def check(cond,msg):
    if not cond:
        raise AssertionError(msg)

# candidate identity
skill=(ROOT/"SKILL.md").read_text(encoding="utf-8")
check('version: "1.1.0"' in skill,"version")
check("FAITHFUL" in skill,"faithful missing")
check("same coherent document" in skill,"same-document rule")
check("No installation is required" in skill,"no-install route")
check("TypeSafe may orchestrate" in skill,"TypeSafe fallback")
check("Agnes may provide text" in skill,"Agnes fallback")
check("Illustrations are not evidence" in skill,"visual evidence boundary")

# compiled prompt assembly
director=(ROOT/"prompts/director.md").read_text(encoding="utf-8").rstrip()
compiled=(ROOT/"prompts/studio-agent.txt").read_text(encoding="utf-8")
check(compiled.startswith(director),"compiled prompt does not start with director")
for method in ["story-bible","scene-draft","editor","continuity","research","audiobook"]:
    raw=(ROOT/"writing-skills"/method/"SKILL.md").read_text(encoding="utf-8")
    body=raw.split("---",2)[2].strip()
    check(body in compiled,f"compiled missing {method}")

# audit IDs appear exactly once in table
audit=(ROOT/"AUDIT.md").read_text(encoding="utf-8")
ids=["A1","A2","A3","A4"]+[f"Q{i:02d}" for i in range(1,61)]+[f"X{i:02d}" for i in range(1,11)]
rows=re.findall(r'^\| (A[1-4]|Q\d{2}|X\d{2}) \|',audit,flags=re.M)
check(len(rows)==74,f"audit row count {len(rows)}")
check(set(rows)==set(ids),"audit ID set mismatch")
check(all(rows.count(i)==1 for i in ids),"duplicate audit ID")

# visual is actual parseable SVG with accessibility text
svg=ROOT/"examples/illumination-key-state.svg"
tree=ET.parse(svg)
root=tree.getroot()
ns="{http://www.w3.org/2000/svg}"
check(root.find(ns+"title") is not None,"SVG title")
check(root.find(ns+"desc") is not None,"SVG description")
check(root.attrib.get("role")=="img","SVG role")
check("aria-labelledby" in root.attrib,"SVG aria")

# faithful integrated sample preserves source text and order
sample=(ROOT/"examples/illumination-faithful.md").read_text(encoding="utf-8")
s1="Mara kept the lighthouse key."
s2="Ivo waited outside the lantern room."
check(sample.count(s1)>=2 and sample.count(s2)>=2,"source sentences missing")
same=sample.split("## Same document",1)[1].split("## Fidelity note",1)[0]
check(same.index(s1)<same.index(s2),"source order changed")
check("Any transfer stays unresolved." in sample,"uncertainty lost")

# config parses and preserves bounded provider behavior
cfg=json.loads((ROOT/"config.json").read_text(encoding="utf-8"))
check(cfg["version"]=="1.1.0","config version")
check(cfg["automatic_provider_fallback"] is False,"silent provider fallback")

print("PASS candidate_contract")
print("PASS compiled_prompt")
print("PASS audit_74")
print("PASS svg_parse")
print("PASS svg_accessibility")
print("PASS faithful_fixture")
print("PASS provider_fallback_boundary")
