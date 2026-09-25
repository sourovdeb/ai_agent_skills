---
name: audiobook
description: Use when preparing supplied prose for human narration with separated reading and pronunciation scripts, expressive cues and ASCII emotion maps.
metadata:
  version: "1.0.0"
---

# Audiobook performance adapter

This text-only adapter preserves the design of the existing audiobook-performance-coach v1.1.0. It assists the narrator; it does not create audio. It uses ELT-inspired attention to meaning and pronunciation; the performance notation is a project convention, not a Cambridge-certified method.

Read the source and necessary scene context. Preserve all source words, their order, punctuation, negation and attribution in the reading copy. Assign matching paragraph/sentence IDs such as P01-S01. Never combine adjacent source sentences into a paragraph. Leave blank lines between blocks. Keep narrator and character voices distinct. Do not make an ambiguous sound's cause explicit before the story reveals it.

Output Settings/key; READING SCRIPT; PRONUNCIATION SCRIPT; COACHING NOTES; COVERAGE. The complete reading script and complete pronunciation script are separate, not alternating sentence pairs. The user reads ONE script per take. All spoken words need a counterpart in the pronunciation view. Use one established accent and respelling key; ask or disclose a provisional key when absent. Approximate respelling is not IPA or verified audio. Check unfamiliar names when tools permit; mark unresolved words individually.

Phrase **emphasis** is not shouting. Lexical stress in WIN-doh is a different concept. Put added cues on their own lines. Use [PAUSE 0.5s], [PITCH fall], [MOUTH: say "tik...tik" softly; 1s; stop before speech], and [ATM: distant rain]. MOUTH is performed, not read aloud; ATM is written atmosphere unless separately activated. Preserve literal brackets already in the source. Additional spoken words need explicit permission and separate [ADD-SAY] blocks.

Use compact ASCII maps only where the emotion changes: relief[#..] -> joy[###]. Anchor the transition to exact words and describe a playable change in pace, pitch or articulation. Emotional intensity is not volume and the map is an interpretive choice, not a measurement. Suggest comfortable speech, not forced crying, gasping or strain. A single narrator uses sound -> stop -> speech, not an impossible independent mouth background track.

Compact route: 1-3 sentences, about 80 source words as a starting heuristic. Scene route: 4-12 sentences, about 350 words. Reduce the batch before dropping words, pronunciation coverage or spacing. End with completed/remaining IDs and a checkpoint. Without accessible recordings, label feedback script-based. Never invent measured timing, pitch or voice identity.
